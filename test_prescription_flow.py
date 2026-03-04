#!/usr/bin/env python3

import requests
import json
from pymongo import MongoClient

def test_prescription_flow():
    """Test the complete prescription storage and retrieval flow"""
    
    print("=== Prescription Flow Test ===")
    print("Testing: Prescription → pending_prescriptions → cart item")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    }
    
    print("\n🔍 Step 1: Check current cart state...")
    try:
        cart_url = "https://livebackend.multifolks.com/api/v1/cart"
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
                    print(f"      ✅ PRESCRIPTION FOUND IN CART:")
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
                    print(f"      ❌ NO PRESCRIPTION IN CART")
                    
                    # Check if this is your LEON item
                    if 'LEON' in item.get('name', '') and 'M.1795.SQ' in item.get('name', ''):
                        print(f"      🎯 FOUND YOUR LEON ITEM!")
                        print(f"      ❌ THIS ITEM SHOULD HAVE PRESCRIPTION DATA")
                        print(f"      🔍 Checking if prescription is in pending_prescriptions...")
                        
                        # Check pending_prescriptions for this product
                        product_id = item.get('product_id')
                        if product_id:
                            print(f"      📋 Product ID: {product_id}")
        else:
            print(f"   ❌ Failed to get cart: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🔍 Step 2: Check pending_prescriptions in database...")
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client.test_db
        users_collection = db.users
        
        # Get user document
        user_doc = users_collection.find_one({"_id": ObjectId("694cfe35835763")})
        
        if user_doc:
            pending_prescriptions = user_doc.get('pending_prescriptions', {})
            print(f"   ✅ Found user document")
            print(f"   📋 Pending prescriptions count: {len(pending_prescriptions)}")
            
            if pending_prescriptions:
                for product_id, prescription_data in pending_prescriptions.items():
                    print(f"\n   📋 Pending prescription for product {product_id}:")
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
                        
                        # Check if this matches your LEON item
                        if 'LEON' in str(prescription_data) or 'M.1795.SQ' in str(prescription_data):
                            print(f"      🎯 FOUND YOUR LEON PRESCRIPTION IN PENDING!")
                            print(f"      ✅ Prescription exists in pending_prescriptions")
                            print(f"      ❌ But not transferred to cart item")
                            print(f"      🔧 Issue: Cart update not transferring prescription")
                    else:
                        print(f"      📷 Uploaded prescription")
                        print(f"      File: {prescription_data.get('fileName', 'NOT_SET')}")
            else:
                print(f"   ❌ NO PENDING PRESCRIPTIONS FOUND")
                print(f"      This means prescription was never stored in pending_prescriptions")
        else:
            print(f"   ❌ User document not found")
            
        client.close()
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    print("\n🔍 Step 3: Check cart items in database...")
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client.test_db
        cart_collection = db.cart
        
        # Get user's cart from database
        user_cart = cart_collection.find_one({"user_id": "694cfe35835763"})
        
        if user_cart and "items" in user_cart:
            items = user_cart["items"]
            print(f"   ✅ Database cart items: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\n   🗄️  Database Item {idx + 1}:")
                print(f"      - Name: {item.get('name')}")
                print(f"      - Cart ID: {item.get('cart_id')}")
                print(f"      - Product ID: {item.get('product_id')}")
                print(f"      - Has prescription: {'prescription' in item}")
                
                if 'prescription' in item:
                    prescription = item.get('prescription')
                    print(f"      ✅ PRESCRIPTION FOUND IN DATABASE:")
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
                        
                        # Check if this is your LEON item
                        if 'LEON' in item.get('name', '') and 'M.1795.SQ' in item.get('name', ''):
                            print(f"      🎯 FOUND YOUR LEON ITEM IN DATABASE!")
                            print(f"      ✅ PRESCRIPTION IS STORED IN DATABASE")
                            print(f"      🔍 Issue might be frontend not reading it correctly")
                    else:
                        print(f"      📷 UPLOADED PRESCRIPTION")
                        print(f"         File: {prescription.get('fileName', 'NOT_SET')}")
                else:
                    print(f"      ❌ NO PRESCRIPTION IN DATABASE")
                    
                    # Check if this is your LEON item
                    if 'LEON' in item.get('name', '') and 'M.1795.SQ' in item.get('name', ''):
                        print(f"      🎯 FOUND YOUR LEON ITEM IN DATABASE!")
                        print(f"      ❌ DATABASE MISSING PRESCRIPTION DATA")
                        print(f"      🔍 This means prescription was never transferred from pending_prescriptions")
        else:
            print(f"   ❌ No cart found in database")
            
        client.close()
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    print("\n🔍 Step 4: Analysis...")
    print("   📋 Possible scenarios:")
    print("   1. ✅ Prescription in pending_prescriptions + ✅ Prescription in cart:")
    print("      - Data is stored correctly")
    print("      - Issue is frontend reading the data")
    print("   2. ✅ Prescription in pending_prescriptions + ❌ Prescription in cart:")
    print("      - Data is stored in pending_prescriptions")
    print("      - Cart update is not transferring prescription")
    print("   3. ❌ Prescription in pending_prescriptions + ❌ Prescription in cart:")
    print("      - Prescription was never stored in pending_prescriptions")
    print("      - Issue is prescription upload/save process")
    
    print("\n🔧 Next steps:")
    print("   1. Check if prescription is in pending_prescriptions")
    print("   2. Check if prescription is in cart items")
    print("   3. Identify where the flow is breaking")
    print("   4. Fix the specific issue in the flow")

if __name__ == "__main__":
    test_prescription_flow()
