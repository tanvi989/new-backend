#!/usr/bin/env python3

import requests
import json
from pymongo import MongoClient

def test_cart_persistence():
    """Test if cart data persists correctly"""
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    print("=== Testing Cart Data Persistence ===")
    
    # Test 1: Get current cart
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
            
            print(f"Current cart items: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\nItem {idx + 1}:")
                print(f"  cart_id: {item.get('cart_id')}")
                print(f"  product_id: {item.get('product_id')}")
                print(f"  name: {item.get('name')}")
                print(f"  price: {item.get('price')}")
                print(f"  Has lens: {'lens' in item}")
                
                if 'lens' in item:
                    lens = item.get('lens', {})
                    print(f"  Lens keys: {list(lens.keys())}")
                    print(f"  Has tint_price: {'tint_price' in lens}")
                    print(f"  Has coating_price: {'coating_price' in lens}")
                    print(f"  Has tint_type: {'tint_type' in lens}")
                    print(f"  Has tint_color: {'tint_color' in lens}")
                    
                    if 'tint_price' in lens:
                        print(f"  Tint Price: £{lens.get('tint_price', 0)}")
                    if 'tint_type' in lens:
                        print(f"  Tint Type: {lens.get('tint_type', 'NONE')}")
                    if 'tint_color' in lens:
                        print(f"  Tint Color: {lens.get('tint_color', 'NONE')}")
                
                print(f"  Has prescription: {'prescription' in item}")
                if 'prescription' in item:
                    prescription = item.get('prescription')
                    print(f"  Prescription keys: {list(prescription.keys()) if isinstance(prescription, dict) else 'NOT_DICT'}")
                    print(f"  Prescription data: {str(prescription)[:200]}...")
            
            print(f"\n{'='*60}")
        else:
            print(f"Failed to get cart: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_cart_persistence()
