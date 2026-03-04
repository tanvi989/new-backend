#!/usr/bin/env python3

import requests
import json
from pymongo import MongoClient

def check_prescription_flow():
    """Check prescription data flow from cart to order"""
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    print("=== Checking Prescription Data Flow ===")
    
    # Step 1: Check current cart data
    print("\n1. Checking Cart Data:")
    cart_url = "http://localhost:5000/api/v1/cart"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(cart_url, headers=headers)
        if response.status_code == 200:
            cart_data = response.json()
            items = cart_data.get('cart', [])
            
            print(f"   Cart items: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\n   Item {idx + 1}:")
                print(f"     Name: {item.get('name')}")
                print(f"     Product ID: {item.get('product_id')}")
                print(f"     Has prescription: {'prescription' in item}")
                
                if 'prescription' in item:
                    prescription = item.get('prescription')
                    print(f"     ✅ Prescription found:")
                    print(f"       Keys: {list(prescription.keys()) if isinstance(prescription, dict) else 'NOT_DICT'}")
                    print(f"       Data: {str(prescription)[:300]}...")
                else:
                    print(f"     ❌ NO PRESCRIPTION DATA")
                
                # Check lens data
                if 'lens' in item:
                    lens = item.get('lens', {})
                    print(f"     Lens keys: {list(lens.keys())}")
                    print(f"     Has tint_price: {'tint_price' in lens}")
                    print(f"     Has coating_price: {'coating_price' in lens}")
        else:
            print(f"   Failed to get cart: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 2: Check database directly
    print("\n2. Checking Database Directly:")
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client['gaMultilens']
        cart_collection = db['cart']
        
        # Find user's cart
        user_cart = cart_collection.find_one({"user_id": "694cfe35816eaa145c1a7f44"})
        
        if user_cart:
            items = user_cart.get('items', [])
            print(f"   Database cart items: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\n   DB Item {idx + 1}:")
                print(f"     Name: {item.get('name')}")
                print(f"     Product ID: {item.get('product_id')}")
                print(f"     Has prescription: {'prescription' in item}")
                
                if 'prescription' in item:
                    prescription = item.get('prescription')
                    print(f"     ✅ DB Prescription found:")
                    print(f"       Keys: {list(prescription.keys()) if isinstance(prescription, dict) else 'NOT_DICT'}")
                    print(f"       Data: {str(prescription)[:300]}...")
                else:
                    print(f"     ❌ NO PRESCRIPTION IN DATABASE")
        else:
            print("   No cart found in database")
            
        client.close()
        
    except Exception as e:
        print(f"   Database error: {e}")

if __name__ == "__main__":
    check_prescription_flow()
