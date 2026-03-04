#!/usr/bin/env python3

import requests
import json
from pymongo import MongoClient

def test_find_prescription():
    """Find prescription data for the cart item"""
    
    print("=== Finding Prescription Data ===")
    
    try:
        client = MongoClient("mongodb://tanvi9891:tanvi2701@ac-jq2pulx-shard-00-00.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-01.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-02.ck8iin3.mongodb.net:27017/?replicaSet=atlas-29v1f8-shard-0&ssl=true&authSource=admin")
        db = client['gaMultilens']
        users_collection = db['accounts']
        
        # Find user by email
        user_email = "paradkartanvi@gmail.com"
        user = users_collection.find_one({"email": user_email})
        
        if user:
            print(f"✅ User found: {user_email}")
            print(f"User ID: {user.get('_id')}")
            
            pending_prescriptions = user.get('pending_prescriptions', {})
            print(f"Pending prescriptions keys: {list(pending_prescriptions.keys())}")
            
            # Check for product ID E22C1216
            product_id = "E22C1216"
            prescription_data = pending_prescriptions.get(product_id)
            
            if prescription_data:
                print(f"\n✅ Found prescription for product {product_id}")
                print(f"Prescription data: {prescription_data}")
                if isinstance(prescription_data, dict):
                    print(f"Lens index: {prescription_data.get('lensIndex', 'Not found')}")
                    print(f"All keys: {list(prescription_data.keys())}")
            else:
                print(f"\n❌ No prescription found for product {product_id}")
                
                # Show all available prescriptions
                if pending_prescriptions:
                    print(f"\nAvailable prescriptions:")
                    for key, value in pending_prescriptions.items():
                        print(f"  {key}: {type(value)} - {str(value)[:100]}...")
        else:
            print(f"❌ User not found with email: {user_email}")
            
            # Try to find any user with pending prescriptions
            print(f"\n=== Searching for any user with pending prescriptions ===")
            users_with_prescriptions = users_collection.find({"pending_prescriptions": {"$exists": True, "$ne": {}}})
            
            for user in users_with_prescriptions:
                print(f"User: {user.get('email')} - Prescriptions: {list(user.get('pending_prescriptions', {}).keys())}")
                
    except Exception as e:
        print(f"Database check failed: {e}")

if __name__ == "__main__":
    test_find_prescription()
