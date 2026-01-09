
import pymongo
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    import config
    print(f"✅ Loaded config. Database: {config.DATABASE_NAME}")
except ImportError:
    print("❌ Could not import config.py")
    sys.exit(1)

def update_prices():
    print("="*60)
    print("🔧 UPDATING PRODUCT PRICES")
    print("="*60)
    
    try:
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.DATABASE_NAME]
        products_col = db["products"]
        cart_col = db["cart"]
        
        # 1. Update Products with list_price 139 to 149
        result = products_col.update_many(
            {"list_price": 139},
            {"$set": {"list_price": 149, "price": 149}}
        )
        print(f"✅ Updated {result.modified_count} products from £139 to £149")
        
        # 2. Update Products with list_price 99 to 109 (assuming similar gap?)
        # Only doing 139 as that's the one we confirmed
        
        # 3. Force update carts to trigger recalculation?
        # Actually, get_cart pulls from products_col via lookup, so next fetch will use 149.
        # But we need to update the cached 'price' in cart items if used
        
        # We can't easily update valid cached prices without full recalculation logic.
        # But since get_cart re-calculates, it should be fine.
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_prices()
