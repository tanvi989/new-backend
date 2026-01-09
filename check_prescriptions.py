import pymongo
import json
from bson import ObjectId

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["multifolks"]
users_collection = db["users"]

# Find a user with prescriptions
user = users_collection.find_one({"prescriptions": {"$exists": True, "$ne": []}})

if user:
    print("Found user with prescriptions:")
    print(f"Email: {user.get('email', 'N/A')}")
    print(f"\nNumber of prescriptions: {len(user.get('prescriptions', []))}")
    print("\nPrescription data:")
    for i, pres in enumerate(user.get('prescriptions', [])[:3]):  # Show first 3
        print(f"\n--- Prescription {i+1} ---")
        print(f"Type: {pres.get('type')}")
        print(f"Name: {pres.get('name')}")
        print(f"Has image_url: {'image_url' in pres}")
        print(f"image_url value: {pres.get('image_url', 'NOT FOUND')}")
        print(f"Created: {pres.get('created_at')}")
        if 'data' in pres:
            print(f"Data keys: {list(pres['data'].keys())}")
else:
    print("No users with prescriptions found")

client.close()
