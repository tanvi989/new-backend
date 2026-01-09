import pymongo
import sys
sys.path.append('/home/selfeey-india/Documents/AI_Projects/login_api')
import config

# Connect to MongoDB
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.DATABASE_NAME]

print("=" * 80)
print(f"DATABASE: {config.DATABASE_NAME}")
print("=" * 80)

# List all collections
collections = db.list_collection_names()
print(f"\n📚 Collections in database '{config.DATABASE_NAME}':")
for i, coll_name in enumerate(collections, 1):
    count = db[coll_name].count_documents({})
    print(f"   {i}. {coll_name} ({count} documents)")

print("\n" + "=" * 80)
print(f"CHECKING CONFIG.COLLECTION_NAME: {config.COLLECTION_NAME}")
print("=" * 80)

# Check if the configured collection exists
if config.COLLECTION_NAME in collections:
    print(f"\n✅ Collection '{config.COLLECTION_NAME}' EXISTS")
    count = db[config.COLLECTION_NAME].count_documents({})
    print(f"   Total documents: {count}")
    
    # Show sample document structure
    sample = db[config.COLLECTION_NAME].find_one()
    if sample:
        print(f"\n   Sample document fields:")
        for key in sample.keys():
            print(f"      - {key}")
else:
    print(f"\n❌ Collection '{config.COLLECTION_NAME}' DOES NOT EXIST")
    print(f"\n💡 Available collections: {', '.join(collections)}")

# Check for prescriptions in any collection
print("\n" + "=" * 80)
print("SEARCHING FOR PRESCRIPTIONS IN ALL COLLECTIONS")
print("=" * 80)

for coll_name in collections:
    coll = db[coll_name]
    # Check if any document has a 'prescriptions' field
    doc_with_prescriptions = coll.find_one({"prescriptions": {"$exists": True}})
    if doc_with_prescriptions:
        count = coll.count_documents({"prescriptions": {"$exists": True}})
        print(f"\n✅ Found prescriptions in collection: {coll_name}")
        print(f"   Documents with prescriptions: {count}")
        
        # Check for image_url in prescriptions
        doc_with_image_url = coll.find_one({"prescriptions.image_url": {"$exists": True}})
        if doc_with_image_url:
            print(f"   ✅ Has prescriptions with image_url")
        else:
            print(f"   ❌ No prescriptions with image_url")

client.close()
print("\n" + "=" * 80)
