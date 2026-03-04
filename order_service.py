import datetime
from typing import Dict, Any, List, Optional
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

try:
    import config as _config
    USER_COLLECTION_NAME = getattr(_config, "COLLECTION_NAME", "accounts_login")
except Exception:
    USER_COLLECTION_NAME = "accounts_login"


def _safe_float(val: Any) -> float:
    """Safely convert value to float, stripping currency symbols."""
    if val is None: return 0.0
    if isinstance(val, (int, float)): return float(val)
    try:
        return float(str(val).replace("£", "").replace(",", "").strip())
    except (ValueError, TypeError):
        return 0.0

def _safe_int(val: Any, default: int = 1) -> int:
    """Safely convert value to int."""
    if val is None: return default
    if isinstance(val, int): return val
    try:
        return int(float(str(val).replace(",", "").strip()))
    except (ValueError, TypeError):
        return default

def _is_real_lens_index(v: Any) -> bool:
    """Check if value is a real lens index (1.50, 1.56, 1.61, etc) not a coating/tint id."""
    if v is None: return False
    s = str(v).lower().strip()
    if not s: return False
    coating_ids = ["solid", "mirror", "anti-reflective", "water-resistant", "oil-resistant"]
    if s in coating_ids: return False
    import re
    return bool(re.match(r"^1\.\d{2}", s) or re.match(r"^1\.50/1\.56$|^1\.59/1\.61$", s))


def _normalize_cart_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize cart item to match desired order document format.
    Ensures product_id, name, image, price, product.products, lens, flag, cart_id, added_at.
    Preserves lens_package, lens_index for display (so order-details shows "1.61 High Index" not "oil-resistant").
    """
    product_data = item.get("product", {}) or {}
    products = product_data.get("products", {}) or {}
    lens_data = dict(item.get("lens", {}) or {})

    # Use lens_package/lens_index for lensIndex when present (real index), else keep lens.id for coating/tint
    real_index = lens_data.get("lens_package") or lens_data.get("lens_index")
    if _is_real_lens_index(real_index):
        lens_data["lensIndex"] = lens_data.get("lens_index") or lens_data.get("lens_package") or lens_data.get("lensIndex")
        if "lens_package" not in lens_data and real_index:
            lens_data["lens_package"] = str(real_index)
        if "lens_index" not in lens_data and lens_data.get("lens_package"):
            lens_data["lens_index"] = lens_data.get("lens_package")

    # Extract base product_id (strip unique suffix like _1738765432000)
    raw_id = item.get("product_id", products.get("skuid", products.get("id", "")))
    if isinstance(raw_id, str) and "_" in raw_id:
        product_id = raw_id.split("_")[0]
    else:
        product_id = str(raw_id) if raw_id else ""

    # Frame/list price for top-level price field
    try:
        # Prefer stored frame_price so order-details shows frame-only
        raw_frame = item.get("frame_price")
        if raw_frame is not None:
             price = _safe_float(raw_frame)
        else:
            price = _safe_float(products.get("list_price") or products.get("price") or item.get("price"))
    except Exception:
        price = 0.0

    name = products.get("name", products.get("naming_system", item.get("name", "")))
    image = products.get("image", item.get("image", ""))
    quantity = _safe_int(item.get("quantity"), 1)
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
        # Optional price breakdown if provided by create_order
        "frame_price": item.get("frame_price"),
        "lens_price": item.get("lens_price"),
        "addon_price": item.get("addon_price"),
        # ✅ PRESERVE PRESCRIPTION DATA
        "prescription": item.get("prescription"),
        # Also preserve any other important fields
        "product_details": item.get("product_details"),
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
        metadata: Optional[Dict[str, Any]] = None,
        order_id_override: Optional[str] = None,  # Use frontend order_id so PATCH can find the order
        subtotal_override: Optional[float] = None,
        total_payable_override: Optional[float] = None,
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
            order_id_override: If set, use this order_id (from frontend) so payment-success PATCH finds the order
            subtotal_override: If set, use this subtotal instead of recalculating
            total_payable_override: If set, use this as order_total/total_payable
            
        Returns:
            Dictionary with order creation status and order_id
        """
        try:
            # Use frontend order_id when provided so PATCH /orders/:id can find the order after payment
            order_id = order_id_override if order_id_override else self._generate_order_id()
            
            # Calculate order totals
            subtotal = 0
            
            logger.info(f"\n{'='*80}")
            logger.info(f"[ORDER] ORDER CALCULATION DEBUG - Order ID will be: {self._generate_order_id()}")
            logger.info(f"{'='*80}")
            logger.info(f"[ORDER] Processing {len(cart_items)} cart items")
            logger.info(f"[ORDER] Input pricing - Discount: £{discount_amount}, Shipping: £{shipping_cost}")
            
            for item in cart_items:
                # Basic price calculation with safe string parsing
                products = item.get("product", {}).get("products", {}) or {}
                
                # Always use backend product price for calculation to ensure safety
                product_price = _safe_float(products.get("list_price") or products.get("price"))
                
                lens_data = item.get("lens", {}) or {}
                lens_price = _safe_float(lens_data.get("selling_price"))
                
                tint_price = _safe_float(lens_data.get("tint_price"))
                coating_price = _safe_float(lens_data.get("coating_price"))
                addon_price = tint_price if tint_price > 0 else coating_price
                
                quantity = _safe_int(item.get("quantity"), 1)
                item_total = (product_price + lens_price + addon_price) * quantity
                subtotal += item_total
                
                # Store calculated values (simple floats)
                item["frame_price"] = product_price
                item["lens_price"] = lens_price
                item["addon_price"] = addon_price

            # Use overrides from frontend when provided (so order shows correct totals even if cart fetch was empty)
            if subtotal_override is not None:
                subtotal = float(subtotal_override)
                logger.info(f"[ORDER] Using frontend subtotal override: £{subtotal}")
            if total_payable_override is not None:
                order_total = float(total_payable_override)
                logger.info(f"[ORDER] Using frontend total_payable override: £{order_total}")
            else:
                order_total = subtotal - discount_amount + shipping_cost
            
            logger.info(f"\n[ORDER] ORDER TOTALS:")
            logger.info(f"   Subtotal: £{subtotal}")
            logger.info(f"   Discount: £{discount_amount}")
            logger.info(f"   Shipping: £{shipping_cost}")
            logger.info(f"   Order Total: £{order_total}")
            logger.info(f"{'='*80}\n")

            # Normalize cart items to desired format (product_id, name, image, price, product.products, lens, etc.)
            normalized_cart = [_normalize_cart_item(item) for item in cart_items]

            # Persist prescriptions exactly as received (photo/manual with type, image_url, data). Do not replace with PD-only.
            if metadata and "prescriptions" in metadata:
                pres = metadata["prescriptions"]
                if isinstance(pres, str):
                    try:
                        import json
                        metadata = {**metadata, "prescriptions": json.loads(pres)}
                    except Exception:
                        pass
                elif not isinstance(pres, list):
                    metadata = {**metadata, "prescriptions": [pres] if pres is not None else []}
                # List is stored as-is so camera/upload prescription image_url is saved in DB

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
                
                # Save total payable to user document for easy retrieval (use accounts collection)
                try:
                    users_collection = self.db[USER_COLLECTION_NAME]
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
                
                # Cart will be cleared on thank you page after order is confirmed
                # DO NOT clear cart here - keep data until thank you page
                
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

    def create_order_from_cart(
        self,
        user_id: str,
        order_id: str,
        cart_service
    ) -> Dict[str, Any]:
        """
        Create order from cart data on thank you page
        
        Args:
            user_id: User ID
            order_id: Order ID
            cart_service: CartService instance
            
        Returns:
            Dictionary with order creation status
        """
        try:
            # Get cart data
            print(f"[ORDER_SERVICE] Creating order from cart for user {user_id}")
            cart_result = cart_service.get_cart_summary(user_id)
            
            if not cart_result.get('success'):
                return {
                    'success': False,
                    'error': 'Failed to retrieve cart data'
                }
            
            items = cart_result.get('cart', [])
            
            print(f"[ORDER_SERVICE] Cart items count: {len(items)}")
            
            if not items:
                return {
                    'success': False,
                    'error': 'Cart is empty'
                }
            
            # Check if prescription data is present in cart items
            for idx, item in enumerate(items):
                print(f"[ORDER_SERVICE] Item {idx + 1}:")
                print(f"   - Name: {item.get('name')}")
                print(f"   - Has prescription: {'prescription' in item}")
                if 'prescription' in item:
                    prescription = item.get('prescription')
                    print(f"   - Prescription keys: {list(prescription.keys()) if isinstance(prescription, dict) else 'NOT_DICT'}")
                    print(f"   - Prescription data: {str(prescription)[:200]}...")
                else:
                    print(f"   - ❌ NO PRESCRIPTION DATA FOUND")
            
            # Get user details
            accounts_coll_name = getattr(config, 'COLLECTION_NAME', 'accounts_login')
            users_collection = self.db[accounts_coll_name]
            try:
                user = users_collection.find_one({'_id': ObjectId(user_id)})
            except Exception:
                user = users_collection.find_one({'_id': user_id})
            
            user_email = user.get('email', '') if user else ''
            
            # Create order using existing create_order method
            order_result = self.create_order(
                user_id=user_id,
                user_email=user_email,
                cart_items=items,
                payment_data={'pay_mode': 'stripe', 'transaction_id': order_id},
                shipping_address='Default Address',  # You may want to get this from user profile
                billing_address='Default Address',   # You may want to get this from user profile
                discount_amount=cart_result.get('discount_amount', 0),
                shipping_cost=cart_result.get('shipping_cost', 0),
                metadata={'order_id': order_id, 'customer_email': user_email},
                order_id_override=order_id
            )
            
            if order_result.get('success'):
                print(f"[ORDER_SERVICE] Order {order_id} created successfully from cart")
                return {
                    'success': True,
                    'order_id': order_id,
                    'message': 'Order created from cart successfully'
                }
            else:
                print(f"[ORDER_SERVICE] Failed to create order from cart: {order_result.get('error')}")
                return {
                    'success': False,
                    'error': order_result.get('error', 'Failed to create order')
                }
                
        except Exception as e:
            print(f"[ORDER_SERVICE] Error creating order from cart: {str(e)}")
            return {
                'success': False,
                'error': f'Create order from cart failed: {str(e)}'
            }

    def update_order_with_cart(
        self,
        order_id: str,
        cart_items: Optional[List[Dict[str, Any]]] = None,
        subtotal: Optional[float] = None,
        discount_amount: Optional[float] = None,
        shipping_cost: Optional[float] = None,
        total_payable: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Update order with cart and totals (called from payment-success page to fix £0 order)."""
        try:
            update = {"updated": datetime.datetime.utcnow(), "updated_at": datetime.datetime.utcnow()}
            if cart_items is not None:
                normalized = [_normalize_cart_item(i) for i in cart_items]
                update["cart"] = normalized
            if subtotal is not None:
                update["subtotal"] = round(float(subtotal), 2)
            if discount_amount is not None:
                update["discount"] = round(float(discount_amount), 2)
                update["discount_amount"] = round(float(discount_amount), 2)
            if shipping_cost is not None:
                update["shipping_cost"] = round(float(shipping_cost), 2)
            if total_payable is not None:
                update["total_payable"] = round(float(total_payable), 2)
                update["order_total"] = round(float(total_payable), 2)
            if len(update) <= 2:
                return {"success": True, "message": "No updates"}
            result = self.collection.update_one(
                {"order_id": order_id},
                {"$set": update}
            )
            if result.matched_count:
                logger.info(f"[OK] Order {order_id} updated with cart/totals")
                return {"success": True, "message": "Order updated"}
            return {"success": False, "message": "Order not found"}
        except Exception as e:
            logger.error(f"[ERR] update_order_with_cart: {str(e)}")
            return {"success": False, "error": str(e)}
