#!/usr/bin/env python3

import requests
import json

def test_cart_prescription():
    """Test if prescription data is in the cart"""
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MTZlYWExNDVjMWE3ZjQ0IiwiZW1haWwiOiJwYXJhZGthcnRhbnZpaUBnbWFpbC5jb20iLCJleHAiOjE3NzI1NjU1MjMsImlhdCI6MTc3MjQ3OTEyM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    print("=== Testing Cart Prescription Data ===")
    
    # Get cart
    cart_url = "https://livebackend.multifolks.com/api/v1/cart"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(cart_url, headers=headers)
        print(f"Cart Status: {response.status_code}")
        
        if response.status_code == 200:
            cart_data = response.json()
            print(f"✅ Cart retrieved successfully")
            print(f"Number of items: {cart_data.get('total_items', 0)}")
            
            items = cart_data.get('cart', [])
            for idx, item in enumerate(items):
                print(f"\n--- Item {idx + 1} ---")
                print(f"Name: {item.get('name', 'Unknown')}")
                print(f"Price: {item.get('price', 0)}")
                print(f"Has prescription: {'prescription' in item}")
                
                if 'prescription' in item:
                    prescription = item.get('prescription')
                    print(f"Prescription data: {prescription}")
                    
                    # Check for lens index specifically
                    if isinstance(prescription, dict):
                        print(f"Lens index: {prescription.get('lensIndex', 'Not found')}")
                        print(f"Prescription keys: {list(prescription.keys())}")
                
                # Check lens data
                if 'lens' in item:
                    lens = item.get('lens', {})
                    print(f"Lens selling price: {lens.get('selling_price', 'Not found')}")
                    print(f"Lens keys: {list(lens.keys())}")
        else:
            print(f"❌ Cart retrieval failed: {response.text}")
            
    except Exception as e:
        print(f"Cart request failed: {e}")

if __name__ == "__main__":
    test_cart_prescription()
