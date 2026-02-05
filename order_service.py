import datetime
from typing import Dict, Any, List, Optional
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


def _normalize_cart_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize cart item to match desired order document format.
    Ensures product_id, name, image, price, product.products, lens, flag, cart_id, added_at.
    """
    product_data = item.get("product", {}) or {}
    products = product_data.get("products", {}) or {}
    lens_data = item.get("lens", {}) or {}

    # Extract base product_id (strip unique suffix like _1738765432000)
    raw_id = item.get("product_id", products.get("skuid", products.get("id", "")))
    if isinstance(raw_id, str) and "_" in raw_id:
        product_id = raw_id.split("_")[0]
    else:
        product_id = str(raw_id) if raw_id else ""

    # Frame/list price for top-level price field
    try:
        price = products.get("list_price", products.get("price", item.get("price", 0)))
        if price is None:
            price = 0.0
        elif isinstance(price, str):
            price = float(str(price).replace("£", "").replace(",", "")) if price else 0.0
        else:
            price = float(price)
    except (ValueError, TypeError):
        price = 0.0

    name = products.get("name", products.get("naming_system", item.get("name", "")))
    image = products.get("image", item.get("image", ""))
    quantity = int(item.get("quantity", 1))
    cart_id = item.get("cart_id")
    added_at = item.get("added_at")
    flag = item.get("flag", "instant")

    # Ensure product.products has string _id for JSON compatibility
    products_copy = dict(products)
    if "_id" in products_copy and products_copy["_id"]:
        products_copy["_id"] = str(products_copy["_id"])

    return {
        "product_id": product_id,
        "name": str(name) if name else "Unknown",
        "image": str(image) if image else "",
        "price": round(price, 2),
        "quantity": quantity,
        "product": {"products": products_copy},
        "lens": lens_data,
        "flag": flag,
        "cart_id": cart_id,
        "added_at": added_at,
    }


class OrderService:
    """
    Order Service for Multifolks
    Handles order creation, retrieval, and management
    """

    def __init__(self, db_connection: Database):
        self.db: Database = db_connection
        self.collection: Collection = self.db["orders"]
        self.cart_collection: Collection = self.db["cart"]
        
        # Create index on order_id for faster lookups
        self.collection.create_index("order_id", unique=True)
        self.collection.create_index("user_id")
        
        logger.info("[OK] OrderService initialized")

    def _generate_order_id(self) -> str:
        """
        Generate unique order ID in format: ORD-{TIMESTAMP}
        Example: ORD-1765891114486
        """
        import time
        timestamp = int(time.time() * 1000)
        return f"ORD-{timestamp}"

    def create_order(
        self,
        user_id: str,
        user_email: str,
        cart_items: List[Dict[str, Any]],
        payment_data: Dict[str, Any],
        shipping_address: str,
        billing_address: str,
        discount_amount: float = 0.0,  # Discount amount from cart (coupon discount)
        shipping_cost: float = 0.0,  # Shipping cost from cart
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new order
        
        Args:
            user_id: User ID
            user_email: User email
            cart_items: List of cart items
            payment_data: Payment information (pay_mode, transaction_id, etc.)
            shipping_address: Shipping address
            billing_address: Billing address
            discount_amount: Discount amount from cart (coupon discount)
            shipping_cost: Shipping cost from cart
            metadata: Additional metadata
            
        Returns:
            Dictionary with order creation status and order_id
        """
        try:
            # Generate unique order ID
            order_id = self._generate_order_id()
            
            # Calculate order totals
            subtotal = 0
            
            logger.info(f"\n{'='*80}")
            logger.info(f"[ORDER] ORDER CALCULATION DEBUG - Order ID will be: {self._generate_order_id()}")
            logger.info(f"{'='*80}")
            logger.info(f"[ORDER] Processing {len(cart_items)} cart items")
            logger.info(f"[ORDER] Input pricing - Discount: £{discount_amount}, Shipping: £{shipping_cost}")
            
            for item in cart_items:
                product_price = float(item.get("product", {}).get("products", {}).get("list_price", 0))
                lens_price = float(item.get("lens", {}).get("selling_price", 0))
                quantity = int(item.get("quantity", 1))
                
                # CRITICAL: Include coating/tint price (matches cart_service.py calculation)
                # Get tint price for sunglasses, coating price for regular glasses
                lens_data = item.get("lens", {})
                tint_price = float(lens_data.get("tint_price", 0))
                coating_price = float(lens_data.get("coating_price", 0))
                addon_price = tint_price if tint_price > 0 else coating_price
                
                # DEBUG LOGGING
                logger.info(f"\n[ORDER] Item: {item.get('product', {}).get('products', {}).get('name', 'Unknown')}")
                logger.info(f"   Frame Price: £{product_price}")
                logger.info(f"   Lens Price: £{lens_price}")
                logger.info(f"   Tint Price: £{tint_price}")
                logger.info(f"   Coating Price: £{coating_price}")
                logger.info(f"   Addon Price (used): £{addon_price}")
                logger.info(f"   Quantity: {quantity}")
                
                if tint_price == 0 and coating_price == 0:
                    logger.warning(f"   [WARN] Both tint_price and coating_price are 0! Addon will be missing from total.")
                    logger.warning(f"   [WARN] Lens data: {lens_data}")
                
                # Match frontend and cart_service calculation: frame + lens + addon
                item_total = (product_price + lens_price + addon_price) * quantity
                logger.info(f"   Item Total: £{item_total}")
                subtotal += item_total
            
            logger.info(f"\n[ORDER] ORDER TOTALS:")
            logger.info(f"   Subtotal: £{subtotal}")
            logger.info(f"   Discount: £{discount_amount}")
            logger.info(f"   Shipping: £{shipping_cost}")
            
            # Calculate order total: subtotal - discount + shipping (matches cart_service.py)
            order_total = subtotal - discount_amount + shipping_cost
            logger.info(f"   Order Total: £{order_total}")
            logger.info(f"{'='*80}\n")

            # Normalize cart items to desired format (product_id, name, image, price, product.products, lens, etc.)
            normalized_cart = [_normalize_cart_item(item) for item in cart_items]

            # Create order document (matches desired DB format)
            now = datetime.datetime.utcnow()
            pay_mode = payment_data.get("pay_mode", "Stripe / Online")
            payment_status = payment_data.get("payment_status", "Pending")
            order_doc = {
                "order_id": order_id,
                "user_id": str(user_id),
                "customer_email": user_email,
                "created": now,
                "updated": now,
                "updated_at": now,

                # Payment info
                "pay_mode": pay_mode,
                "payment_status": payment_status,
                "transaction_id": payment_data.get("transaction_id") or None,
                "payment_intent_id": payment_data.get("payment_intent_id") or None,

                # Order status (Processing when pending payment)
                "order_status": "Processing" if payment_status == "Pending" else "Confirmed",
                "is_partial": bool(payment_data.get("is_partial", False)),

                # Pricing
                "order_total": round(order_total, 2),
                "total_payable": round(order_total, 2),
                "subtotal": round(subtotal, 2),
                "discount": round(discount_amount, 2),
                "discount_amount": round(discount_amount, 2),
                "shipping_cost": round(shipping_cost, 2),
                "lens_discount": 0,
                "retailer_lens_discount": 0,

                # Cart items (normalized format)
                "cart": normalized_cart,

                # Addresses
                "shipping_address": shipping_address or "",
                "billing_address": billing_address or "",

                # Metadata
                "metadata": metadata or {}
            }
            
            # Insert order into database
            result = self.collection.insert_one(order_doc)
            
            if result.inserted_id:
                logger.info(f"[OK] Order created: {order_id} for user {user_id}")
                
                # Save total payable to user document for easy retrieval
                try:
                    users_collection = self.db['users']
                    try:
                        uid = ObjectId(user_id)
                    except Exception:
                        uid = user_id
                    users_collection.update_one(
                        {'_id': uid},
                        {'$set': {
                            'last_order_total_payable': round(order_total, 2),
                            'last_order_id': order_id,
                            'last_order_date': now
                        }}
                    )
                    logger.info(f"[OK] Saved total payable £{order_total} to user {user_id}")
                except Exception as e:
                    logger.warning(f"[WARN] Failed to update user document with total payable: {str(e)}")
                
                # Clear user's cart after successful order
                try:
                    self.cart_collection.update_one(
                        {"user_id": str(user_id)},
                        {"$set": {"items": [], "updated_at": now}}
                    )
                    logger.info(f"[OK] Cart cleared for user {user_id}")
                except Exception as e:
                    logger.warning(f"Failed to clear cart: {str(e)}")
                
                return {
                    "success": True,
                    "order_id": order_id,
                    "message": "Order created successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to insert order into database"
                }
                
        except Exception as e:
            logger.error(f"[ERR] Error creating order: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to create order: {str(e)}"
            }

    def get_user_orders(self, user_id: str) -> Dict[str, Any]:
        """
        Get all orders for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with orders list
        """
        try:
            orders = list(
                self.collection.find(
                    {"user_id": str(user_id)},
                    {"_id": 0}  # Exclude MongoDB _id
                ).sort("created", -1)  # Newest first
            )
            
            return {
                "success": True,
                "status": True,
                "orders": orders,
                "total_orders": len(orders)
            }
            
        except Exception as e:
            logger.error(f"[ERR] Error fetching orders: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to fetch orders: {str(e)}"
            }

    def get_order_by_id(self, order_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get order details by order ID
        
        Args:
            order_id: Order ID
            user_id: Optional user ID for authorization check
            
        Returns:
            Dictionary with order details
        """
        try:
            query = {"order_id": order_id}
            
            # Add user_id to query if provided (for authorization)
            if user_id:
                query["user_id"] = str(user_id)
            
            order = self.collection.find_one(query, {"_id": 0})
            
            if order:
                return {
                    "success": True,
                    "status": True,
                    "order": order
                }
            else:
                return {
                    "success": False,
                    "status": False,
                    "message": "Order not found"
                }
                
        except Exception as e:
            logger.error(f"[ERR] Error fetching order {order_id}: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to fetch order: {str(e)}"
            }

    def update_order_status(
        self,
        order_id: str,
        status: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update order status
        
        Args:
            order_id: Order ID
            status: New status (e.g., "Processing", "Shipped", "Delivered", "Cancelled")
            user_id: Optional user ID for authorization
            
        Returns:
            Dictionary with update status
        """
        try:
            query = {"order_id": order_id}
            if user_id:
                query["user_id"] = str(user_id)
            
            result = self.collection.update_one(
                query,
                {
                    "$set": {
                        "order_status": status,
                        "updated": datetime.datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count:
                return {
                    "success": True,
                    "message": f"Order status updated to {status}"
                }
            else:
                return {
                    "success": False,
                    "message": "Order not found or no changes made"
                }
                
        except Exception as e:
            logger.error(f"[ERR] Error updating order status: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to update order: {str(e)}"
            }

    def update_payment_status(
        self,
        order_id: str,
        payment_status: str,
        payment_intent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update payment status for an order
        
        Args:
            order_id: Order ID
            payment_status: New payment status
            payment_intent_id: Optional Stripe payment intent ID
            
        Returns:
            Dictionary with update status
        """
        try:
            update_data = {
                "payment_status": payment_status,
                "updated": datetime.datetime.utcnow()
            }
            
            if payment_intent_id:
                update_data["payment_intent_id"] = payment_intent_id
            
            result = self.collection.update_one(
                {"order_id": order_id},
                {"$set": update_data}
            )
            
            if result.modified_count:
                logger.info(f"[OK] Payment status updated for order {order_id}: {payment_status}")
                return {
                    "success": True,
                    "message": "Payment status updated"
                }
            else:
                return {
                    "success": False,
                    "message": "Order not found"
                }
                
        except Exception as e:
            logger.error(f"[ERR] Error updating payment status: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to update payment status: {str(e)}"
            }
