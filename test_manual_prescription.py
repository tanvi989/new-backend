#!/usr/bin/env python3

import requests
import json

def test_manual_prescription():
    """Test manual prescription storage and retrieval"""
    
    print("=== Manual Prescription Test ===")
    print("Testing: Manual prescription storage for logged-in users")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    }
    
    print("\n🔍 Step 1: Check current cart state...")
    try:
        cart_url = "https://testbackend.multifolks.com/api/v1/cart"
        response = requests.get(cart_url, headers=headers)
        
        if response.status_code == 200:
            cart_data = response.json()
            items = cart_data.get('cart', [])
            
            print(f"   ✅ Current cart items: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\n   📦 Item {idx + 1}:")
                print(f"      - Name: {item.get('name')}")
                print(f"      - Cart ID: {item.get('cart_id')}")
                print(f"      - Product ID: {item.get('product_id')}")
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
                else:
                    print(f"      ❌ NO PRESCRIPTION")
                    
                    # Check if this is your E76A8615 item
                    if 'E76A8615' in str(item.get('product_id', '')):
                        print(f"      🎯 FOUND YOUR E76A8615 ITEM!")
                        print(f"      ❌ THIS ITEM SHOULD HAVE PRESCRIPTION DATA")
                        print(f"      📋 Cart ID: {item.get('cart_id')}")
        else:
            print(f"   ❌ Failed to get cart: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🔍 Step 2: Test manual prescription addition...")
    
    # First, let's try to add a manual prescription to the E76A8615 item
    try:
        # Find the cart_id for E76A8615
        cart_response = requests.get(cart_url, headers=headers)
        if cart_response.status_code == 200:
            cart_data = cart_response.json()
            items = cart_data.get('cart', [])
            
            target_cart_id = None
            for item in items:
                if 'E76A8615' in str(item.get('product_id', '')):
                    target_cart_id = item.get('cart_id')
                    break
            
            if target_cart_id:
                print(f"   📋 Found E76A8615 item with cart_id: {target_cart_id}")
                
                # Test manual prescription update
                prescription_data = {
                    "right_eye": {"sph": "0.00", "cyl": "0.00", "axis": "-"},
                    "left_eye": {"sph": "0.00", "cyl": "0.00", "axis": "-"},
                    "reading": {"right": "3.25", "left": "2.75"},
                    "pd": {"right": "23.25", "left": "23.25"},
                    "birth_year": "2000"
                }
                
                prescription_url = f"https://testbackend.multifolks.com/api/v1/cart/prescription/{target_cart_id}"
                
                # Create form data for manual prescription
                form_data = {
                    'mode': 'manual',
                    'prescription_data': json.dumps(prescription_data)
                }
                
                print(f"   📤 Sending manual prescription to {prescription_url}")
                print(f"   📋 Prescription data: {prescription_data}")
                
                prescription_response = requests.post(
                    prescription_url, 
                    data=form_data,
                    headers=headers
                )
                
                print(f"   📊 Response status: {prescription_response.status_code}")
                if prescription_response.status_code == 200:
                    result = prescription_response.json()
                    print(f"   ✅ Prescription update successful: {result.get('message', 'No message')}")
                else:
                    print(f"   ❌ Prescription update failed: {prescription_response.text}")
            else:
                print(f"   ❌ E76A8615 item not found in cart")
        else:
            print(f"   ❌ Failed to get cart for prescription test")
            
    except Exception as e:
        print(f"   ❌ Error testing prescription: {e}")
    
    print("\n🔍 Step 3: Check cart again after prescription update...")
    try:
        cart_response = requests.get(cart_url, headers=headers)
        
        if cart_response.status_code == 200:
            cart_data = cart_response.json()
            items = cart_data.get('cart', [])
            
            print(f"   ✅ Cart items after update: {len(items)}")
            
            for idx, item in enumerate(items):
                if 'E76A8615' in str(item.get('product_id', '')):
                    print(f"\n   📦 E76A8615 Item After Update:")
                    print(f"      - Cart ID: {item.get('cart_id')}")
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
                    else:
                        print(f"      ❌ NO PRESCRIPTION AFTER UPDATE")
                    break
        else:
            print(f"   ❌ Failed to get cart after update: {cart_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error checking cart after update: {e}")
    
    print("\n🔍 Step 4: Analysis...")
    print("   📋 What this test tells us:")
    print("   1. If prescription appears after manual update:")
    print("      - Manual prescription storage is working")
    print("      - Issue might be with frontend not calling the API")
    print("   2. If prescription doesn't appear after manual update:")
    print("      - Manual prescription storage is NOT working")
    print("      - Backend logic has issues")
    print("   3. If prescription appears but then disappears:")
    print("      - Storage works but data gets lost later")
    print("      - Cart operations clearing prescription")
    
    print("\n🔧 Next steps:")
    print("   1. Check if frontend is calling prescription API")
    print("   2. Check browser network tab for prescription requests")
    print("   3. Check backend logs for prescription storage")
    print("   4. Verify pending_prescriptions storage")

if __name__ == "__main__":
    test_manual_prescription()
