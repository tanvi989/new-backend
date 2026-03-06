#!/usr/bin/env python3

import requests
import json

def check_cart_prescription():
    """Check what prescription data is actually in the cart item"""
    
    print("=== Cart Prescription Check ===")
    print("Checking: What prescription data is in the cart item from API")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    }
    
    print("\n🔍 Step 1: Get cart from API...")
    try:
        cart_url = "https://testbackend.multifolks.com/api/v1/cart"
        response = requests.get(cart_url, headers=headers)
        
        if response.status_code == 200:
            cart_data = response.json()
            items = cart_data.get('cart', [])
            
            print(f"   ✅ Cart items: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\n   📦 Item {idx + 1}:")
                print(f"      - Cart ID: {item.get('cart_id')}")
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
                        
                        # Check if this matches your M.1563.RE item
                        if 'M.1563.RE' in str(item.get('name', '')):
                            print(f"      🎯 FOUND YOUR M.1563.RE ITEM!")
                            print(f"      ✅ PRESCRIPTION DATA IS IN CART ITEM")
                    elif prescription.get('mode') == 'upload':
                        print(f"         File: {prescription.get('fileName', 'NOT_SET')}")
                        print(f"         Image URL: {prescription.get('image_url', 'NOT_SET')}")
                    else:
                        print(f"         Unknown prescription type")
                        
                    print(f"      📋 Full prescription object:")
                    print(f"         {json.dumps(prescription, indent=6)}")
                else:
                    print(f"      ❌ NO PRESCRIPTION IN CART ITEM")
                    
                    # Check if this is your M.1563.RE item
                    if 'M.1563.RE' in str(item.get('name', '')):
                        print(f"      🎯 FOUND YOUR M.1563.RE ITEM!")
                        print(f"      ❌ CART ITEM MISSING PRESCRIPTION DATA")
                        print(f"      🔍 This is the root cause!")
                        
                        # Check if this is the cart ID from the logs
                        if item.get('cart_id') == 1772503574681:
                            print(f"      🎯 MATCHES CART ID FROM LOGS!")
                            print(f"      ❌ This cart item should have prescription but doesn't")
        else:
            print(f"   ❌ Failed to get cart: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🔍 Step 2: Check pending_prescriptions in database...")
    try:
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        db = client.test_db
        users_collection = db.users
        
        user_doc = users_collection.find_one({"_id": ObjectId("694cfe35835763")})
        
        if user_doc:
            pending_prescriptions = user_doc.get('pending_prescriptions', {})
            print(f"   ✅ Pending prescriptions: {len(pending_prescriptions)}")
            
            if pending_prescriptions:
                for product_id, prescription_data in pending_prescriptions.items():
                    print(f"\n   📋 Pending prescription for {product_id}:")
                    print(f"      Type: {prescription_data.get('type', 'UNKNOWN')}")
                    print(f"      Mode: {prescription_data.get('mode', 'UNKNOWN')}")
                    
                    if prescription_data.get('mode') == 'manual':
                        data = prescription_data.get('data', {})
                        print(f"      Right Eye SPH: {data.get('right_eye', {}).get('sph', 'NOT_SET')}")
                        print(f"      Left Eye SPH: {data.get('left_eye', {}).get('sph', 'NOT_SET')}")
                        print(f"      Reading R: {data.get('reading', {}).get('right', 'NOT_SET')}")
                        print(f"      Reading L: {data.get('reading', {}).get('left', 'NOT_SET')}")
                        print(f"      PD R: {data.get('pd', {}).get('right', 'NOT_SET')}")
                        print(f"      PD L: {data.get('pd', {}).get('left', 'NOT_SET')}")
                        print(f"      Birth Year: {data.get('birth_year', 'NOT_SET')}")
            else:
                print(f"   ❌ No pending prescriptions found")
        else:
            print(f"   ❌ User document not found")
            
        client.close()
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    print("\n🔍 Step 3: Check guest_prescriptions collection...")
    try:
        from pymongo import MongoClient
        
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        db = client.test_db
        guest_prescriptions_collection = db["guest_prescriptions"]
        
        user_doc = guest_prescriptions_collection.find_one({"_id": "694cfe35835763"})
        
        if user_doc:
            prescriptions = user_doc.get('prescriptions', [])
            print(f"   ✅ Guest prescriptions: {len(prescriptions)}")
            
            for idx, prescription in enumerate(prescriptions):
                print(f"\n   📋 Guest prescription {idx + 1}:")
                print(f"      Type: {prescription.get('type', 'UNKNOWN')}")
                print(f"      Created: {prescription.get('created_at', 'UNKNOWN')}")
                
                if prescription.get('type') == 'photo':
                    print(f"      File: {prescription.get('data', {}).get('fileName', 'NOT_SET')}")
                elif prescription.get('type') == 'manual':
                    print(f"      Manual prescription data")
                    
                print(f"      Associated Product: {prescription.get('associatedProduct', {})}")
        else:
            print(f"   ❌ No guest prescriptions found")
            
        client.close()
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    print("\n🔍 Step 4: Analysis...")
    print("   📋 What this tells us:")
    print("   1. If cart item has prescription:")
    print("      - Frontend should use it immediately")
    print("      - Should NOT check userPrescriptions")
    print("   2. If cart item has no prescription:")
    print("      - Frontend falls back to userPrescriptions")
    print("      - Shows 'Add Prescription'")
    print("   3. If pending_prescriptions exists but cart item doesn't:")
    print("      - Backend cart addition not working")
    print("      - Prescription not transferred to cart item")
    
    print("\n🔧 Next steps:")
    print("   1. Check if cart item has prescription data")
    print("   2. If not, check pending_prescriptions")
    print("   3. If pending_prescriptions exists, fix cart addition logic")
    print("   4. If cart item has prescription, fix frontend logic")

if __name__ == "__main__":
    check_cart_prescription()
