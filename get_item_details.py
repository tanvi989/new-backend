
import pymongo
import sys
import os
import json

# Add current directory to path
sys.path.append(os.getcwd())

try:
    import config
    print(f"✅ Loaded config. Database: {config.DATABASE_NAME}")
except ImportError:
    print("❌ Could not import config.py")
    sys.exit(1)

def get_item_details():
    try:
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.DATABASE_NAME]
        cart_col = db["cart"]
        
        # Find carts with items, sorted by updated_at
        carts = cart_col.find({"items": {"$ne": []}}).sort("updated_at", -1).limit(3)
        
        print("\n" + "="*60)
        print("🛒 RECENT CART ITEMS")
        print("="*60)
        
        for cart in carts:
            print(f"User ID: {cart.get('user_id')}")
            for item in cart.get('items', []):
                product = item.get('product', {})
                p_products = product.get('products', {})
                
                name = item.get('name') or p_products.get('name') or p_products.get('product_name')
                sku = p_products.get('skuid') or p_products.get('sku')
                list_price = p_products.get('list_price')
                price = p_products.get('price')
                
                print(f"- Name: {name}")
                print(f"  SKU: {sku}")
                print(f"  DB List Price: {list_price}")
                print(f"  DB Price: {price}")
                print("-" * 30)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_item_details()
