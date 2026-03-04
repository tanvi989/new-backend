#!/usr/bin/env python3

import requests
import json
from pymongo import MongoClient

def test_pending_prescriptions():
    """Check what's in the user's pending prescriptions"""
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MTZlYWExNDVjMWE3ZjQ0IiwiZW1haWwiOiJwYXJhZGthcnRhbnZpaUBnbWFpbC5jb20iLCJleHAiOjE3NzI1NjU1MjMsImlhdCI6MTc3MjQ3OTEyM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    print("=== Checking Pending Prescriptions ===")
    
    try:
        # Connect to MongoDB directly
        client = MongoClient("mongodb://tanvi9891:tanvi2701@ac-jq2pulx-shard-00-00.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-01.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-02.ck8iin3.mongodb.net:27017/?replicaSet=atlas-29v1f8-shard-0&ssl=true&authSource=admin")
        db = client['gaMultilens']
        users_collection = db['accounts']
        
        # Find the user
        user_id = "694cfe35816eaa145c1a7f44"
        user = users_collection.find_one({"_id": user_id})
        
        if user:
            print(f"✅ User found: {user.get('email')}")
            pending_prescriptions = user.get('pending_prescriptions', {})
            print(f"Pending prescriptions: {pending_prescriptions}")
            
            # Check if there are any pending prescriptions
            if pending_prescriptions:
                print(f"Number of pending prescriptions: {len(pending_prescriptions)}")
                for product_id, prescription_data in pending_prescriptions.items():
                    print(f"\n--- Product ID: {product_id} ---")
                    print(f"Prescription data: {prescription_data}")
                    if isinstance(prescription_data, dict):
                        print(f"Lens index: {prescription_data.get('lensIndex', 'Not found')}")
                        print(f"Prescription keys: {list(prescription_data.keys())}")
            else:
                print("❌ No pending prescriptions found")
        else:
            print("❌ User not found")
            
    except Exception as e:
        print(f"Database check failed: {e}")

if __name__ == "__main__":
    test_pending_prescriptions()
