#!/usr/bin/env python3

import requests
import json

def test_prescription_sync():
    """Test prescription data sync across devices"""
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    print("=== Testing Prescription Data Sync ===")
    
    # Step 1: Get current cart data
    print("\n1. Getting current cart data:")
    cart_url = "https://livebackend.multifolks.com/api/v1/cart"
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
                print(f"     - Name: {item.get('name')}")
                print(f"     - Cart ID: {item.get('cart_id')}")
                print(f"     - Has prescription: {'prescription' in item}")
                
                if 'prescription' in item:
                    prescription = item.get('prescription')
                    print(f"     ✅ Prescription found:")
                    print(f"       Type: {prescription.get('type', 'UNKNOWN')}")
                    print(f"       Mode: {prescription.get('mode', 'UNKNOWN')}")
                    print(f"       Data keys: {list(prescription.get('data', {}).keys()) if prescription.get('data') else 'NONE'}")
                    
                    # Check specific prescription data
                    data = prescription.get('data', {})
                    print(f"       Right Eye SPH: {data.get('right_eye', {}).get('sph', 'NOT_SET')}")
                    print(f"       Left Eye SPH: {data.get('left_eye', {}).get('sph', 'NOT_SET')}")
                    print(f"       Reading R: {data.get('reading', {}).get('right', 'NOT_SET')}")
                    print(f"       Reading L: {data.get('reading', {}).get('left', 'NOT_SET')}")
                    print(f"       PD R: {data.get('pd', {}).get('right', 'NOT_SET')}")
                    print(f"       PD L: {data.get('pd', {}).get('left', 'NOT_SET')}")
                    print(f"       Birth Year: {data.get('birth_year', 'NOT_SET')}")
                else:
                    print(f"     ❌ NO PRESCRIPTION DATA")
        else:
            print(f"   Failed to get cart: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Expected vs Actual ===")
    print("Expected prescription data:")
    print("  - Right Eye SPH: 0.00")
    print("  - Left Eye SPH: 0.00") 
    print("  - Reading R: 0.50")
    print("  - Reading L: 0.75")
    print("  - PD R: 23.25")
    print("  - PD L: 23.25")
    print("  - Birth Year: 2000")
    
    print("\nIf the actual data doesn't match, then:")
    print("1. The prescription wasn't saved correctly to the cart")
    print("2. There's a caching issue in the frontend")
    print("3. The mobile device is getting old data from somewhere")

if __name__ == "__main__":
    test_prescription_sync()
