#!/usr/bin/env python3

import requests
import json
from pymongo import MongoClient

def test_cart_details():
    """Check cart details and find corresponding pending prescriptions"""
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MTZlYWExNDVjMWE3ZjQ0IiwiZW1haWwiOiJwYXJhZGthcnRhbnZpaUBnbWFpbC5jb20iLCJleHAiOjE3NzI1NjU1MjMsImlhdCI6MTc3MjQ3OTEyM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    print("=== Checking Cart Details ===")
    
    # Get cart first
    cart_url = "https://testbackend.multifolks.com/api/v1/cart"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(cart_url, headers=headers)
        
        if response.status_code == 200:
            cart_data = response.json()
            items = cart_data.get('cart', [])
            
            for idx, item in enumerate(items):
                print(f"\n--- Item {idx + 1} ---")
                product_id = item.get('product_id')
                print(f"Product ID: {product_id}")
                print(f"Name: {item.get('name', 'Unknown')}")
                print(f"Price: {item.get('price', 0)}")
                
                # Now check if there's a pending prescription for this product
                if product_id:
                    try:
                        client = MongoClient("mongodb://tanvi9891:tanvi2701@ac-jq2pulx-shard-00-00.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-01.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-02.ck8iin3.mongodb.net:27017/?replicaSet=atlas-29v1f8-shard-0&ssl=true&authSource=admin")
                        db = client['gaMultilens']
                        users_collection = db['accounts']
                        
                        # Try to find user by email from token
                        user_email = "paradkartanvi@gmail.com"
                        user = users_collection.find_one({"email": user_email})
                        
                        if user:
                            print(f"✅ User found: {user_email}")
                            pending_prescriptions = user.get('pending_prescriptions', {})
                            
                            # Check for this product_id (as string and ObjectId)
                            prescription_data = pending_prescriptions.get(str(product_id)) or pending_prescriptions.get(product_id)
                            
                            if prescription_data:
                                print(f"✅ Found prescription for product {product_id}")
                                print(f"Prescription data: {prescription_data}")
                                if isinstance(prescription_data, dict):
                                    print(f"Lens index: {prescription_data.get('lensIndex', 'Not found')}")
                                    print(f"Prescription keys: {list(prescription_data.keys())}")
                            else:
                                print(f"❌ No prescription found for product {product_id}")
                                print(f"Available prescription keys: {list(pending_prescriptions.keys())}")
                        else:
                            print(f"❌ User not found with email: {user_email}")
                            
                    except Exception as e:
                        print(f"Database check failed: {e}")
        else:
            print(f"❌ Cart retrieval failed: {response.text}")
            
    except Exception as e:
        print(f"Cart request failed: {e}")

if __name__ == "__main__":
    test_cart_details()
