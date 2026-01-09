
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

def check_product():
    print("="*60)
    print("🔍 CHECK PRODUCT PRICE")
    print("="*60)
    
    try:
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.DATABASE_NAME]
        products_col = db["products"]
        
        # Search for SKU from screenshot
        sku = "M.1003.RE.I.6.A" 
        # Note: Screenshot says 'M.1003.RE.I.6.A'. The 'I' might be '1'.
        
        query = {
            "$or": [
                {"sku": sku},
                {"skuid": sku},
                {"name": sku},
                {"product_name": sku},
                # Try fuzzy regex
                 {"skuid": {"$regex": "M.1003", "$options": "i"}}
            ]
        }
        
        products = list(products_col.find(query))
        
        if not products:
            print(f"❌ Product not found for SKU: {sku}")
            return

        for p in products:
            print(f"\n👓 Product: {p.get('name') or p.get('product_name')}")
            print(f"   SKU: {p.get('skuid')}")
            print(f"   List Price: {p.get('list_price')}")
            print(f"   Price: {p.get('price')}")
            print(f"   Selling Price: {p.get('selling_price')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_product()
