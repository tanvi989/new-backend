
import logging
from typing import Dict, Any, List, Optional

# Mock logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _safe_float(val):
    if val is None: return 0.0
    if isinstance(val, (int, float)): return float(val)
    try:
        return float(str(val).replace("£", "").replace(",", "").strip())
    except (ValueError, TypeError):
        return 0.0

def _normalize_cart_item(item: Dict[str, Any]) -> Dict[str, Any]:
    # Mock implementation of _normalize_cart_item for testing
    # Frame/list price for top-level price field
    try:
        # Prefer stored frame_price so order-details shows frame-only
        raw_frame = item.get("frame_price")
        if raw_frame is not None:
             price = float(raw_frame)
        else:
            product_data = item.get("product", {}) or {}
            products = product_data.get("products", {}) or {}
            price = products.get("list_price", products.get("price", item.get("price", 0)))
            if price is None:
                price = 0.0
            elif isinstance(price, str):
                price = float(str(price).replace("£", "").replace(",", "")) if price else 0.0
            else:
                price = float(price)
    except (ValueError, TypeError) as e:
        print(f"Error in _normalize_cart_item price calc: {e}")
        price = 0.0
    
    return {"price": price, "frame_price": item.get("frame_price")}

def test_create_order_logic():
    cart_items = [
        {
            "product": {"products": {"list_price": "£228.00"}},
            "lens": {"selling_price": 79.0, "coating_price": 0},
            "quantity": 1,
            "addon_price": 0 # Simulating frontend sending this
        }
    ]
    
    subtotal = 0
    
    print("Starting loop...")
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
        
        quantity = int(item.get("quantity", 1))
        item_total = (product_price + lens_price + addon_price) * quantity
        subtotal += item_total
        
        # Store calculated values (simple floats)
        item["frame_price"] = product_price
        item["lens_price"] = lens_price
        item["addon_price"] = addon_price
        
        print(f"Processed item: {item}")

    print(f"Subtotal: {subtotal}")
    
    # Test normalization
    normalized = [_normalize_cart_item(item) for item in cart_items]
    print(f"Normalized: {normalized}")

if __name__ == "__main__":
    try:
        test_create_order_logic()
        print("Test passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
