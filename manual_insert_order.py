
import pymongo
import datetime
import sys
import os

# Add current directory to path to import config
sys.path.append(os.getcwd())

try:
    import config
    print(f"✅ Loaded config. Database: {config.DATABASE_NAME}")
except ImportError:
    print("❌ Could not import config.py. Please run this script from the backend_multifolks directory.")
    sys.exit(1)

def manual_insert_order():
    print("="*60)
    print("🛠️  MANUAL ORDER INSERTION TOOL")
    print("="*60)
    
    # 1. Connect to MongoDB
    print(f"📦 Connecting to MongoDB...")
    try:
        client = pymongo.MongoClient(config.MONGO_URI)
        db = client[config.DATABASE_NAME]
        orders_col = db["orders"]
        print("✅ Connected successfully!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # 2. Create Test Order Data
    order_id = f"TEST{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    test_order = {
        "order_id": order_id,
        "user_id": "MANUAL_TEST_USER",
        "customer_email": "test@example.com",
        "created": datetime.datetime.utcnow(),
        "pay_mode": "Manual Test",
        "payment_status": "Success",
        "order_status": "Test",
        "order_total": 100.00,
        "shipping_address": "Test Address, London, UK",
        "billing_address": "Test Address, London, UK",
        "cart": [
            {
                "product_name": "Test Product",
                "price": 50.00,
                "quantity": 2
            }
        ],
        "metadata": {
            "source": "manual_script"
        }
    }
    
    # 3. Insert into Database
    print(f"\n📝 Inserting test order: {order_id}...")
    try:
        result = orders_col.insert_one(test_order)
        print(f"✅ Order saved! MongoDB ID: {result.inserted_id}")
        
        # 4. Verify Insertion
        print("\n🔍 Verifying insertion...")
        saved_order = orders_col.find_one({"order_id": order_id})
        if saved_order:
            print("✅ SUCCCESS: Retrieved order from database:")
            print(f"   Order ID: {saved_order['order_id']}")
            print(f"   Status: {saved_order['order_status']}")
            print(f"   Total: {saved_order['order_total']}")
        else:
            print("❌ FAILURE: Could not retrieve order immediately after saving.")
            
    except Exception as e:
        print(f"❌ Error inserting order: {e}")

if __name__ == "__main__":
    manual_insert_order()
