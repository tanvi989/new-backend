import pymongo
import json
from bson import ObjectId
import sys
sys.path.append('/home/selfeey-india/Documents/AI_Projects/login_api')
import config

# Connect to MongoDB using the same config as the app
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.DATABASE_NAME]
users_collection = db[config.COLLECTION_NAME]

print("=" * 80)
print("CHECKING MONGODB FOR PRESCRIPTION DATA")
print("=" * 80)

# Count total users
total_users = users_collection.count_documents({})
print(f"\n📊 Total users in database: {total_users}")

# Count users with prescriptions
users_with_prescriptions = users_collection.count_documents({"prescriptions": {"$exists": True, "$ne": []}})
print(f"📊 Users with prescriptions: {users_with_prescriptions}")

if users_with_prescriptions > 0:
    print("\n" + "=" * 80)
    print("PRESCRIPTION DATA FOUND")
    print("=" * 80)
    
    # Find all users with prescriptions
    users = users_collection.find({"prescriptions": {"$exists": True, "$ne": []}})
    
    for user in users:
        print(f"\n👤 User: {user.get('email', 'N/A')}")
        print(f"   User ID: {user['_id']}")
        print(f"   Number of prescriptions: {len(user.get('prescriptions', []))}")
        
        for i, pres in enumerate(user.get('prescriptions', [])):
            print(f"\n   📋 Prescription {i+1}:")
            print(f"      Type: {pres.get('type', 'N/A')}")
            print(f"      Name: {pres.get('name', 'N/A')}")
            print(f"      Created: {pres.get('created_at', 'N/A')}")
            
            # Check for image_url field
            if 'image_url' in pres:
                print(f"      ✅ image_url: {pres['image_url'][:80]}..." if len(pres['image_url']) > 80 else f"      ✅ image_url: {pres['image_url']}")
            else:
                print(f"      ❌ image_url: NOT FOUND")
            
            # Check data field
            if 'data' in pres:
                print(f"      Data keys: {list(pres['data'].keys())}")
                if 'pd' in pres['data']:
                    print(f"      PD data: {pres['data']['pd']}")
            else:
                print(f"      ❌ data: NOT FOUND")
            
            # Show full prescription structure
            print(f"\n      Full prescription structure:")
            print(f"      {json.dumps(pres, indent=8, default=str)[:500]}...")
else:
    print("\n" + "=" * 80)
    print("NO PRESCRIPTIONS FOUND IN DATABASE")
    print("=" * 80)
    print("\n💡 This means:")
    print("   1. Prescriptions are only in localStorage (browser)")
    print("   2. Backend save API is not being called")
    print("   3. OR backend save is failing silently")
    print("\n🔍 Next steps:")
    print("   1. Clear localStorage in browser")
    print("   2. Upload/capture a NEW prescription")
    print("   3. Check browser console for backend API logs")
    print("   4. Run this script again to verify database save")

# Also check if there are any users at all
print("\n" + "=" * 80)
print("SAMPLE USER DATA (to verify DB connection)")
print("=" * 80)

sample_user = users_collection.find_one({})
if sample_user:
    print(f"\n✅ Database connection working")
    print(f"   Sample user email: {sample_user.get('email', 'N/A')}")
    print(f"   User has 'prescriptions' field: {'prescriptions' in sample_user}")
    if 'prescriptions' in sample_user:
        print(f"   Prescriptions value: {sample_user['prescriptions']}")
else:
    print("\n❌ No users found in database at all!")

client.close()
print("\n" + "=" * 80)
