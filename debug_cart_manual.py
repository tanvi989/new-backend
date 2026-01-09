
import pymongo
import sys
import os
import json
from bson import json_util

# Add current directory to path
sys.path.append(os.getcwd())

try:
    import config
    print(f"✅ Loaded config. Database: {config.DATABASE_NAME}")
except ImportError:
    print("❌ Could not import config.py")
    sys.exit(1)

def debug_cart_items():
    print("="*60)
    print("🔍 DEBUG CART ITEMS")
    print("="*60)
    
    try:
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.DATABASE_NAME]
        cart_col = db["cart"]
        
        # Find carts with items
        carts = cart_col.find({"items": {"$ne": []}}).sort("updated_at", -1).limit(5)
        
        found_coating = False
        
        for cart in carts:
            print(f"\n🛒 Cart User ID: {cart.get('user_id')}")
            for item in cart.get('items', []):
                lens = item.get('lens', {})
                product = item.get('product', {})
                name = item.get('name') or product.get('name') or "Unknown Product"
                
                if True: # Dump all lens data for checking
                    print(f"  👓 Item: {name}")
                    print(f"     Lens Object: {json.dumps(lens, default=str, indent=4)}")
                    print(f"     Calculated Coating Price: {item.get('coating_price')}") # If flattened
                    
                    # Check extraction logic manually
                    c_price = 0
                    if "coating_price" in lens:
                         c_price = lens["coating_price"]
                    print(f"     Lens['coating_price']: {c_price}")
                    
                    coating_text = lens.get("coating", "") or lens.get("sub_category", "")
                    print(f"     Coating Text: {coating_text}")
                    print("-" * 30)
                    
        if not found_coating:
            print("\n❌ No items with 'Water'/'Resistant'/'Coating' found in recent carts.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Redirect stdout to file
    with open("cart_dump.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        debug_cart_items()
    sys.stdout = sys.__stdout__
    print("Dump completed to cart_dump.txt")
