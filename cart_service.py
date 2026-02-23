import datetime
from typing import Dict, Any, Optional
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.results import UpdateResult


class CartService:
    """
    Production-Ready Cart Service for Multifolks
    (Optimized for React Frontend + MongoDB)
    """

    def __init__(self, db_connection: Database):
        self.db: Database = db_connection
        self.collection: Collection = self.db["cart"]

    # ------------------------------
    # GET CART
    # ------------------------------
    def get_cart(self, user_id: str) -> Dict[str, Any]:
        try:
            print(f"\n{'='*80}")
            print(f"[GET_CART] User: {user_id}")
            print(f"{'='*80}")
            cart = self.collection.find_one({"user_id": str(user_id)})
            
            if cart:
                print(f"[OK] Cart document found")
                print(f"   - Cart document keys: {list(cart.keys())}")
            else:
                print(f"[WARN] No cart document found for user")

            items = cart.get("items", []) if cart else []
            print(f"[CART] Items in cart: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\n   Item {idx + 1}:")
                print(f"      - cart_id: {item.get('cart_id')}")
                print(f"      - product_id: {item.get('product_id')}")
                print(f"      - name: {item.get('name')}")
                print(f"      - price: {item.get('price')}")
                print(f"      - Has 'product': {'product' in item}")
                print(f"      - Has 'lens': {'lens' in item}")
                print(f"      - Has 'prescription': {'prescription' in item}")
                if 'product' in item:
                    print(f"      - product keys: {list(item.get('product', {}).keys())}")
                    if 'products' in item.get('product', {}):
                        print(f"      - product.products keys: {list(item['product']['products'].keys())}")
            print(f"{'='*80}\n")

            return {
                "success": True,
                "cart": items,
                "total_items": len(items)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to fetch cart: {str(e)}"
            }

    # ------------------------------
    # ADD TO CART (No duplicates)
    # ------------------------------
    def add_to_cart(self, user_id: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user_id = str(user_id)
            
            # DEBUG: Log received data
            print(f"\n{'='*80}")
            print(f"[ADD_CART] ADD_TO_CART DEBUG - User: {user_id}")
            print(f"{'='*80}")
            print(f"[ADD_CART] Received item_data keys: {list(item_data.keys())}")
            print(f"   - product_id: {item_data.get('product_id')}")
            print(f"   - name: {item_data.get('name')}")
            print(f"   - price: {item_data.get('price')}")
            print(f"   - quantity: {item_data.get('quantity')}")
            print(f"   - Has 'product' field: {('product' in item_data)}")
            print(f"   - Has 'lens' field: {('lens' in item_data)}")
            print(f"   - Has 'prescription' field: {('prescription' in item_data)}")
            print(f"   - Has 'product_details' field: {('product_details' in item_data)}")
            if 'product' in item_data:
                print(f"   - product.products keys: {list(item_data.get('product', {}).get('products', {}).keys())}")
            print(f"{'='*80}\n")

            # Required fields check
            if "product_id" not in item_data or "price" not in item_data:
                print(f"[ERR] Missing required fields!")
                return {
                    "success": False,
                    "message": "Missing required fields: product_id or price"
                }

            # Defaults
            item_data.setdefault("quantity", 1)
            item_data.setdefault("name", "")
            item_data.setdefault("image", "")

            now = datetime.datetime.utcnow()

            # Check if product ALREADY exists in cart with SAME options (lens, prescription)
            # We fetch the whole cart to compare complex objects (lens, etc)
            user_cart = self.collection.find_one({"user_id": user_id})
            
            existing_match = None
            if user_cart and "items" in user_cart:
                for item in user_cart["items"]:
                    # Compare Product ID
                    if str(item.get("product_id")) == str(item_data["product_id"]):
                        # Compare Lens Configuration (Deep Check)
                        # We treat None and {} as same
                        exist_lens = item.get("lens") or {}
                        new_lens = item_data.get("lens") or {}
                        
                        # Compare Prescription (Basic Check)
                        # exist_presc = item.get("prescription") or {}
                        # new_presc = item_data.get("prescription") or {}
                        
                        # Normalize lens for comparison (remove prices if needed? No, prices should match if package matches)
                        # For now, strict equality on lens is safer than merging incompatible lenses
                        if exist_lens == new_lens:
                            existing_match = item
                            break
            
            if existing_match:
                new_quantity = existing_match.get("quantity", 1) + item_data["quantity"]
                cart_id_to_update = existing_match.get("cart_id")

                self.collection.update_one(
                    {"user_id": user_id, "items.cart_id": cart_id_to_update},
                    {
                        "$set": {
                            "items.$.quantity": new_quantity,
                            "items.$.updated_at": now,
                            "updated_at": now
                        }
                    }
                )

                return {
                    "success": True,
                    "message": "Quantity updated in cart",
                    "product_id": item_data["product_id"],
                    "cart_id": cart_id_to_update,
                    "new_quantity": new_quantity
                }

            else:
                # Create new cart item
                item_data["cart_id"] = int(now.timestamp() * 1000)
                item_data["added_at"] = now
                
                # DEBUG: Log what we're about to save
                print(f"\n[SAVE] SAVING TO MONGODB:")
                print(f"   - cart_id: {item_data['cart_id']}")
                print(f"   - Fields being saved: {list(item_data.keys())}")
                print(f"   - product field present: {'product' in item_data}")
                print(f"   - lens field present: {'lens' in item_data}")
                print(f"   - prescription field present: {'prescription' in item_data}")
                if 'product' in item_data and 'products' in item_data.get('product', {}):
                    product_data = item_data['product']['products']
                    print(f"   - product.products.skuid: {product_data.get('skuid')}")
                    print(f"   - product.products.name: {product_data.get('name')}")
                    print(f"   - product.products.price: {product_data.get('price')}")
                    print(f"   - product.products.list_price: {product_data.get('list_price')}")

                result = self.collection.update_one(
                    {"user_id": user_id},
                    {
                        "$push": {"items": item_data},
                        "$setOnInsert": {
                            "user_id": user_id,
                            "created_at": now
                        },
                        "$set": {"updated_at": now}
                    },
                    upsert=True
                )
                
                print(f"   - MongoDB matched_count: {result.matched_count}")
                print(f"   - MongoDB modified_count: {result.modified_count}")
                print(f"   - MongoDB upserted_id: {result.upserted_id}")
                print(f"[OK] Item saved to cart!\n")

                return {
                    "success": True,
                    "message": "Added to cart",
                    "cart_id": item_data["cart_id"]
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Add to cart failed: {str(e)}"
            }

    # ------------------------------
    # UPDATE QUANTITY
    # ------------------------------
    def update_quantity(self, user_id: str, cart_id: int, quantity: int) -> Dict[str, Any]:
        if quantity < 1:
            return {"success": False, "message": "Quantity must be at least 1"}

        try:
            result: UpdateResult = self.collection.update_one(
                {"user_id": str(user_id), "items.cart_id": cart_id},
                {
                    "$set": {
                        "items.$.quantity": quantity,
                        "items.$.updated_at": datetime.datetime.utcnow(),
                        "updated_at": datetime.datetime.utcnow()
                    }
                }
            )

            if result.modified_count:
                return {"success": True, "message": "Quantity updated"}
            else:
                return {"success": False, "message": "Item not found in cart"}

        except Exception as e:
            return {"success": False, "error": f"Update failed: {str(e)}"}

    # ------------------------------
    # REMOVE ITEM
    # ------------------------------
    def remove_item(self, user_id: str, cart_id: int) -> Dict[str, Any]:
        try:
            result: UpdateResult = self.collection.update_one(
                {"user_id": str(user_id)},
                {
                    "$pull": {"items": {"cart_id": cart_id}},
                    "$set": {"updated_at": datetime.datetime.utcnow()}
                }
            )

            if result.modified_count:
                return {"success": True, "message": "Item removed from cart"}
            else:
                return {"success": False, "message": "Item not found"}

        except Exception as e:
            return {"success": False, "error": f"Remove failed: {str(e)}"}

    # ------------------------------
    # CLEAR CART
    # ------------------------------
    def clear_cart(self, user_id: str) -> Dict[str, Any]:
        try:
            result = self.collection.update_one(
                {"user_id": str(user_id)},
                {
                    "$set": {
                        "items": [],
                        "updated_at": datetime.datetime.utcnow()
                    }
                }
            )

            if result.matched_count:
                return {"success": True, "message": "Cart cleared successfully"}
            else:
                return {"success": True, "message": "Cart already empty or not found"}

        except Exception as e:
            return {"success": False, "error": f"Clear cart failed: {str(e)}"}

    # ------------------------------
    # COUPONS & SHIPPING
    # ------------------------------
    def apply_coupon(self, user_id: str, code: str) -> Dict[str, Any]:
        try:
            # Mock coupon validation
            valid_coupons = {
                "LAUNCH50": {"type": "percentage", "value": 50},
                "ANU50": {"type": "percentage", "value": 50},
                "SNEH50": {"type": "percentage", "value": 50},
                "WELCOME10": {"type": "percentage", "value": 10},
                "FLAT5": {"type": "fixed", "value": 5}
            }
            
            coupon = valid_coupons.get(code.upper())
            if not coupon:
                return {"success": False, "message": "Invalid coupon code"}
                
            self.collection.update_one(
                {"user_id": str(user_id)},
                {
                    "$set": {
                        "coupon": {"code": code.upper(), **coupon},
                        "updated_at": datetime.datetime.utcnow()
                    }
                }
            )
            return {"success": True, "message": "Coupon applied successfully"}
            
        except Exception as e:
            return {"success": False, "error": f"Apply coupon failed: {str(e)}"}

    def remove_coupon(self, user_id: str) -> Dict[str, Any]:
        try:
            self.collection.update_one(
                {"user_id": str(user_id)},
                {
                    "$unset": {"coupon": ""},
                    "$set": {"updated_at": datetime.datetime.utcnow()}
                }
            )
            return {"success": True, "message": "Coupon removed"}
        except Exception as e:
            return {"success": False, "error": f"Remove coupon failed: {str(e)}"}

    def update_shipping_method(self, user_id: str, method_id: str) -> Dict[str, Any]:
        try:
            shipping_methods = {
                "standard": {"id": "standard", "name": "Standard Shipping", "cost": 6, "free_threshold": 75},
                "express": {"id": "express", "name": "Express Shipping", "cost": 29, "free_threshold": None}
            }
            
            method = shipping_methods.get(method_id)
            if not method:
                return {"success": False, "message": "Invalid shipping method"}
                
            self.collection.update_one(
                {"user_id": str(user_id)},
                {
                    "$set": {
                        "shipping_method": method,
                        "updated_at": datetime.datetime.utcnow()
                    }
                }
            )
            return {"success": True, "message": "Shipping method updated"}
        except Exception as e:
            return {"success": False, "error": f"Update shipping failed: {str(e)}"}

    # ------------------------------
    # UPDATE LENS
    # ------------------------------
    # ------------------------------
    # UPDATE LENS
    # ------------------------------
    def update_lens(self, user_id: str, cart_id: int, lens_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            print(f"\n{'='*80}")
            print(f"[UPDATE_LENS] User: {user_id}, Cart ID: {cart_id}")
            print(f"[UPDATE_LENS] Received lens_data keys: {list(lens_data.keys())}")
            print(f"{'='*80}")
            
            # Find the item to get current frame price
            cart = self.collection.find_one(
                {"user_id": str(user_id), "items.cart_id": cart_id},
                {"items.$": 1}
            )
            
            if not cart or not cart.get("items"):
                return {"success": False, "message": "Item not found in cart"}
                
            item = cart["items"][0]
            
            # --- MAPPING FRONTEND DATA TO BACKEND SCHEMA ---
            # Frontend sends 'lensPackagePrice' -> Backend needs 'selling_price'
            if "selling_price" not in lens_data and "lensPackagePrice" in lens_data:
                lens_data["selling_price"] = lens_data["lensPackagePrice"]
                print(f"[OK] Mapped lensPackagePrice -> selling_price: {lens_data['selling_price']}")
            
            # Frontend sends 'priceValue' (for coating) -> Backend needs 'coating_price'
            if "coating_price" not in lens_data and "priceValue" in lens_data:
                lens_data["coating_price"] = lens_data["priceValue"]
                print(f"[OK] Mapped priceValue -> coating_price: {lens_data['coating_price']}")
            
            # Frontend sends 'tintPrice' (for sunglasses) -> Backend needs 'tint_price'
            if "tint_price" not in lens_data and "tintPrice" in lens_data:
                lens_data["tint_price"] = lens_data["tintPrice"]
                print(f"[OK] Mapped tintPrice -> tint_price: {lens_data['tint_price']}")
            
            # Ensure tint_price defaults to 0 if not present
            if "tint_price" not in lens_data:
                lens_data["tint_price"] = 0
            
            # Ensure coating_price defaults to 0 if not present  
            if "coating_price" not in lens_data:
                lens_data["coating_price"] = 0
            # -----------------------------------------------
            
            print(f"\n[PRICE] PRICE CALCULATION:")
            print(f"   Lens data after mapping:")
            print(f"   - selling_price: {lens_data.get('selling_price', 0)}")
            print(f"   - coating_price: {lens_data.get('coating_price', 0)}")
            print(f"   - tint_price: {lens_data.get('tint_price', 0)}")

            # Calculate new total price
            # Ensure we handle string/int/float correctly
            try:
                possible_price = item.get("product", {}).get("products", {}).get("list_price") or \
                                 item.get("product", {}).get("products", {}).get("price") or \
                                 item.get("price", 0)
                frame_price = float(str(possible_price).replace("£", ""))
            except:
                frame_price = 0
                
            try:
                lens_price = float(str(lens_data.get("selling_price", 0)).replace("£", ""))
            except:
                lens_price = 0
                
            try:
                tint_price = float(str(lens_data.get("tint_price", 0)).replace("£", ""))
            except:
                tint_price = 0
                
            try:
                coating_price = float(str(lens_data.get("coating_price", 0)).replace("£", ""))
            except:
                coating_price = 0
            
            # Use tint price if > 0, otherwise use coating price
            addon_price = tint_price if tint_price > 0 else coating_price

            new_total_price = frame_price + lens_price + addon_price
            
            print(f"   Frame Price: £{frame_price}")
            print(f"   Lens Price: £{lens_price}")
            print(f"   Tint Price: £{tint_price}")
            print(f"   Coating Price: £{coating_price}")
            print(f"   Addon Price (used): £{addon_price}")
            print(f"   New Total Price: £{new_total_price}")
            print(f"{'='*80}\n")
            
            result = self.collection.update_one(
                {"user_id": str(user_id), "items.cart_id": cart_id},
                {
                    "$set": {
                        "items.$.lens": lens_data,
                        "items.$.price": new_total_price,
                        "items.$.updated_at": datetime.datetime.utcnow(),
                        "updated_at": datetime.datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count:
                print(f"[OK] Lens updated successfully for cart_id {cart_id}")
                return {"success": True, "message": "Lens updated successfully"}
            else:
                print(f"[ERR] Failed to update lens for cart_id {cart_id}")
                return {"success": False, "message": "Failed to update lens"}
                
        except Exception as e:
            print(f"[ERR] UPDATE_LENS ERROR: {str(e)}")
            return {"success": False, "error": f"Update lens failed: {str(e)}"}

    # ------------------------------
    # UPDATE PRESCRIPTION
    # ------------------------------
    def update_prescription(self, user_id: str, cart_id: int, prescription_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = self.collection.update_one(
                {"user_id": str(user_id), "items.cart_id": cart_id},
                {
                    "$set": {
                        "items.$.prescription": prescription_data,
                        "items.$.updated_at": datetime.datetime.utcnow(),
                        "updated_at": datetime.datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count:
                return {"success": True, "message": "Prescription updated successfully"}
            else:
                return {"success": False, "message": "Item not found or no changes made"}
                
        except Exception as e:
            return {"success": False, "error": f"Update prescription failed: {str(e)}"}

    # ------------------------------
    # UPDATE ITEM EXTRAS (lens, prescription, product_details/PD) - for guest cart state save
    # ------------------------------
    def update_cart_item_extras(
        self,
        user_id: str,
        cart_id: int,
        lens: Optional[Dict[str, Any]] = None,
        prescription: Optional[Dict[str, Any]] = None,
        product_details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update lens, prescription and/or product_details (PD) for one cart item. Used to persist guest data before merge."""
        try:
            set_fields = {"items.$.updated_at": datetime.datetime.utcnow(), "updated_at": datetime.datetime.utcnow()}
            if lens is not None:
                set_fields["items.$.lens"] = lens
            if prescription is not None:
                set_fields["items.$.prescription"] = prescription
            if product_details is not None:
                set_fields["items.$.product_details"] = product_details
            result = self.collection.update_one(
                {"user_id": str(user_id), "items.cart_id": cart_id},
                {"$set": set_fields}
            )
            if result.matched_count:
                return {"success": True, "message": "Item extras updated"}
            return {"success": False, "message": "Item not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ------------------------------
    # HELPERS
    # ------------------------------
    def _get_lens_coating_price(self, item: Dict[str, Any]) -> float:
        """
        Calculate lens coating price based on frontend logic.
        Matches logic in Cart.tsx:getLensCoating
        """
        try:
            lens = item.get("lens", {})
            
            # 1. Direct coating_price field (Standardized)
            if "coating_price" in lens:
                return float(str(lens["coating_price"]).replace("£", ""))
                
            # 2. Frontend 'priceValue' field (Raw from SelectLensCoatings)
            if "priceValue" in lens:
                 return float(str(lens["priceValue"]).replace("£", ""))

            # 3. Parse from 'coating' text (Matches UI text)
            # The UI displays 'Lens Coating: Water Resistant', derived from lens.coating or lens.sub_category
            coating_text = lens.get("coating", "")
            if not coating_text:
                 coating_text = lens.get("sub_category", "")
            
            if "Water Resistant" in coating_text:
                return 10.0
            elif "Oil Resistant" in coating_text:
                return 15.0
            elif "Anti Reflective" in coating_text:
                return 0.0
                
            # Default
            return 0.0
        except:
            return 0.0
    
    def _get_tint_price(self, item: Dict[str, Any]) -> float:
        """
        Calculate tint price for sunglasses.
        Matches logic in priceUtils.ts:getTintInfo
        Returns 0 if no tint (not sunglasses)
        """
        try:
            lens = item.get("lens", {})
            
            # Check if this is a sunglasses item (has tint)
            # Backend fields: tint_type, tint_price, lens_category === "sun"
            if lens.get("tint_type") or lens.get("lens_category") == "sun" or "tint_price" in lens:
                tint_price = lens.get("tint_price", 0)
                return float(str(tint_price).replace("£", ""))
            
            return 0.0
        except:
            return 0.0


    # ------------------------------
    # CART SUMMARY
    # ------------------------------
    def get_cart_summary(self, user_id: str) -> Dict[str, Any]:
        cart_data = self.get_cart(user_id)

        if not cart_data["success"]:
            return cart_data

        items = cart_data["cart"]
        
        # Fetch cart document for coupon/shipping info
        cart_doc = self.collection.find_one({"user_id": str(user_id)}) or {}
        coupon = cart_doc.get("coupon")
        shipping_method = cart_doc.get("shipping_method", {"id": "standard", "name": "Standard Shipping", "cost": 6, "free_threshold": 75})

        subtotal = 0.0
        for item in items:
            # Calculate logic exactly like Cart.tsx
            
            # 1. Frame Price
            # Try product.products.list_price first, then product.products.price, then item.price
            frame_price = 0.0
            is_fallback_price = False
            
            try:
                products_data = item.get("product", {}).get("products", {})
                if "list_price" in products_data and products_data["list_price"]:
                    frame_price = float(str(products_data["list_price"]).replace("£", ""))
                elif "price" in products_data and products_data["price"]:
                    frame_price = float(str(products_data["price"]).replace("£", ""))
                else:
                    # Fallback if product structure is flat or diff
                    # note: item["price"] is updated to be the TOTAL price in update_lens
                    frame_price = float(str(item.get("price", 0)).replace("£", ""))
                    is_fallback_price = True
            except:
                frame_price = 0.0
                is_fallback_price = True

            # 2. Lens Price
            lens_price = 0.0
            try:
                lens = item.get("lens", {})
                if "selling_price" in lens:
                    lens_price = float(str(lens["selling_price"]).replace("£", ""))
                elif "lensPackagePrice" in lens:
                     lens_price = float(str(lens["lensPackagePrice"]).replace("£", ""))
                else:
                     lens_price = 0.0
            except:
                lens_price = 0.0
            
            # 3. Add-on Price (Tint OR Coating)
            # CRITICAL: Match frontend logic from priceUtils.ts:calculateItemTotal
            # Frontend: addOnPrice = tintInfo ? tintInfo.price : getLensCoating(item).price
            tint_price = self._get_tint_price(item)
            addon_price = tint_price if tint_price > 0 else self._get_lens_coating_price(item)
            
            # Debugging Price logic
            print(f"DEBUG CART CALC: Item {item.get('cart_id')}")
            print(f"  Frame Parsed: {frame_price} (Fallback: {is_fallback_price})")
            print(f"  Lens Parsed: {lens_price}")
            print(f"  Tint Price: {tint_price}")
            print(f"  Coating Price: {self._get_lens_coating_price(item)}")
            print(f"  Add-on Price (Tint OR Coating): {addon_price}")
            
            if is_fallback_price:
                # If we used item['price'], it is already the Total (Frame + Lens + Coating)
                # So we do not add them again
                item_total = frame_price
            else:
                # We have separate frame price, so add components
                # MATCH FRONTEND: framePrice + lensPrice + addOnPrice
                item_total = frame_price + lens_price + addon_price
                
            print(f"  Item Total: {item_total}")
            
            quantity = int(item.get("quantity", 1))
            
            subtotal += item_total * quantity
            
        print(f"DEBUG CART CALC: Final Subtotal: {subtotal}")
        
        # Calculate Discount
        discount_amount = 0
        if coupon:
            if coupon["type"] == "percentage":
                discount_amount = (subtotal * coupon["value"]) / 100
            else:
                discount_amount = coupon["value"]
                
        # Calculate Shipping
        shipping_cost = shipping_method["cost"]
        if shipping_method.get("free_threshold") and subtotal > shipping_method["free_threshold"]:
            shipping_cost = 0
            
        total_payable = subtotal - discount_amount + shipping_cost

        return {
            "success": True,
            "total_items": len(items),
            "subtotal": round(subtotal, 2),
            "discount_amount": round(discount_amount, 2),
            "shipping_cost": round(shipping_cost, 2),
            "total_payable": round(total_payable, 2),
            "coupon": coupon,
            "shipping_method": shipping_method,
            "cart": items
        }
