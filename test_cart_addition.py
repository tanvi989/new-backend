#!/usr/bin/env python3

import requests
import json

def test_cart_addition():
    """Test cart addition with prescription data"""
    
    print("=== Cart Addition Test ===")
    print("Testing: Cart addition with prescription data")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    }
    
    # Test data - E76A8615 item with prescription
    test_item_data = {
        "product_id": "E76A8615",
        "name": "Test Product",
        "image": "test.jpg",
        "price": 149.00,
        "quantity": 1,
        "product": {
            "products": {
                "skuid": "E76A8615",
                "name": "Test Product",
                "price": 149.00,
                "list_price": 149.00
            }
        },
        "lens": {
            "main_category": "Single Vision",
            "lens_package": "1.61",
            "lens_category": "clear",
            "selling_price": 39.00,
            "coating_price": 10.00
        },
        "prescription": {
            "type": "manual",
            "mode": "manual",
            "data": {
                "right_eye": {"sph": "0.00", "cyl": "0.00", "axis": "-"},
                "left_eye": {"sph": "0.00", "cyl": "0.00", "axis": "-"},
                "reading": {"right": "3.25", "left": "2.75"},
                "pd": {"right": "23.25", "left": "23.25"},
                "birth_year": "2000"
            }
        },
        "flag": "normal"
    }
    
    print(f"\n📤 Test Data:")
    print(f"   Product ID: {test_item_data['product_id']}")
    print(f"   Has prescription: {'prescription' in test_item_data}")
    if 'prescription' in test_item_data:
        prescription = test_item_data['prescription']
        print(f"   Prescription type: {prescription.get('type', 'UNKNOWN')}")
        print(f"   Prescription mode: {prescription.get('mode', 'UNKNOWN')}")
        if prescription.get('mode') == 'manual':
            data = prescription.get('data', {})
            print(f"   Right Eye SPH: {data.get('right_eye', {}).get('sph', 'NOT_SET')}")
            print(f"   Left Eye SPH: {data.get('left_eye', {}).get('sph', 'NOT_SET')}")
            print(f"   Reading R: {data.get('reading', {}).get('right', 'NOT_SET')}")
            print(f"   Reading L: {data.get('reading', {}).get('left', 'NOT_SET')}")
            print(f"   PD R: {data.get('pd', {}).get('right', 'NOT_SET')}")
            print(f"   PD L: {data.get('pd', {}).get('left', 'NOT_SET')}")
            print(f"   Birth Year: {data.get('birth_year', 'NOT_SET')}")
    
    print(f"\n🔍 Step 1: Add item to cart with prescription...")
    try:
        cart_url = "http://localhost:5000/api/v1/cart/add"
        response = requests.post(cart_url, json=test_item_data, headers=headers)
        
        print(f"   📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Cart addition successful: {result.get('message', 'No message')}")
            if 'cart_id' in result:
                print(f"   📋 Cart ID: {result['cart_id']}")
        else:
            print(f"   ❌ Cart addition failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error adding to cart: {e}")
    
    print(f"\n🔍 Step 2: Check cart after addition...")
    try:
        cart_url = "http://localhost:5000/api/v1/cart"
        response = requests.get(cart_url, headers=headers)
        
        if response.status_code == 200:
            cart_data = response.json()
            items = cart_data.get('cart', [])
            
            print(f"   ✅ Cart items: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\n   📦 Item {idx + 1}:")
                print(f"      - Product ID: {item.get('product_id')}")
                print(f"      - Name: {item.get('name')}")
                print(f"      - Has prescription: {'prescription' in item}")
                
                if 'prescription' in item:
                    prescription = item.get('prescription')
                    print(f"      ✅ PRESCRIPTION FOUND:")
                    print(f"         Type: {prescription.get('type', 'UNKNOWN')}")
                    print(f"         Mode: {prescription.get('mode', 'UNKNOWN')}")
                    
                    if prescription.get('mode') == 'manual':
                        data = prescription.get('data', {})
                        print(f"         Right Eye SPH: {data.get('right_eye', {}).get('sph', 'NOT_SET')}")
                        print(f"         Left Eye SPH: {data.get('left_eye', {}).get('sph', 'NOT_SET')}")
                        print(f"         Reading R: {data.get('reading', {}).get('right', 'NOT_SET')}")
                        print(f"         Reading L: {data.get('reading', {}).get('left', 'NOT_SET')}")
                        print(f"         PD R: {data.get('pd', {}).get('right', 'NOT_SET')}")
                        print(f"         PD L: {data.get('pd', {}).get('left', 'NOT_SET')}")
                        print(f"         Birth Year: {data.get('birth_year', 'NOT_SET')}")
                        
                        # Check if this matches our test data
                        if (data.get('right_eye', {}).get('sph') == '0.00' and 
                            data.get('reading', {}).get('right') == '3.25' and
                            data.get('pd', {}).get('right') == '23.25'):
                            print(f"      🎯 PRESCRIPTION DATA MATCHES TEST DATA!")
                        else:
                            print(f"      ⚠️  PRESCRIPTION DATA DOES NOT MATCH")
                    else:
                        print(f"      ❓ UNKNOWN PRESCRIPTION TYPE")
                else:
                    print(f"      ❌ NO PRESCRIPTION")
                    
                    # Check if this is our test item
                    if item.get('product_id') == 'E76A8615':
                        print(f"      🎯 FOUND OUR TEST ITEM!")
                        print(f"      ❌ PRESCRIPTION MISSING FROM CART")
        else:
            print(f"   ❌ Failed to get cart: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error checking cart: {e}")
    
    print(f"\n🔍 Step 3: Wait 30 seconds and check again...")
    import time
    time.sleep(30)
    
    print(f"\n🔍 Step 4: Check cart after 30 seconds...")
    try:
        response = requests.get(cart_url, headers=headers)
        
        if response.status_code == 200:
            cart_data = response.json()
            items = cart_data.get('cart', [])
            
            print(f"   ✅ Cart items after 30s: {len(items)}")
            
            for idx, item in enumerate(items):
                if item.get('product_id') == 'E76A8615':
                    print(f"\n   📦 E76A8615 Item After 30s:")
                    print(f"      - Has prescription: {'prescription' in item}")
                    
                    if 'prescription' in item:
                        prescription = item.get('prescription')
                        print(f"      ✅ PRESCRIPTION STILL PRESENT!")
                        print(f"         Type: {prescription.get('type', 'UNKNOWN')}")
                        print(f"         Mode: {prescription.get('mode', 'UNKNOWN')}")
                    else:
                        print(f"      ❌ PRESCRIPTION DISAPPEARED!")
                        print(f"      🔍 This indicates the data loss issue")
                    break
        else:
            print(f"   ❌ Failed to get cart after 30s: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error checking cart after 30s: {e}")
    
    print(f"\n🔍 Step 5: Analysis...")
    print(f"   📋 What this test tells us:")
    print(f"   1. If prescription appears immediately but disappears after 30s:")
    print(f"      - Cart addition works but data gets lost")
    print(f"      - Issue is with data persistence")
    print(f"   2. If prescription never appears:")
    print(f"      - Cart addition not working")
    print(f"      - Backend logic issues")
    print(f"   3. If prescription persists after 30s:")
    print(f"      - Issue is fixed!")
    
    print(f"\n🔧 Next steps:")
    print(f"   1. Check backend logs for cart addition")
    print(f"   " + "2. Check if prescription is stored in guest_prescriptions")
    print(f"   3. Check if prescription is stored in pending_prescriptions")
    print(f"   4. Check if frontend is clearing localStorage")

if __name__ == "__main__":
    test_cart_addition()
