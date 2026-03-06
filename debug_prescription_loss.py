#!/usr/bin/env python3

import requests
import json
import time
from pymongo import MongoClient

def debug_prescription_loss():
    """Debug when and why prescription data is being lost"""
    
    print("=== Prescription Data Loss Debug ===")
    print("Investigating why prescription data disappears over time")
    
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
                        
                        # Check if this is your LEON M.1795.SQ item
                        if 'LEON' in item.get('name', '') and 'M.1795.SQ' in item.get('name', ''):
                            print(f"      🎯 FOUND YOUR LEON ITEM!")
                            print(f"      📊 This item should have prescription data")
                            
                            # Check if prescription data is complete
                            required_fields = ['right_eye', 'left_eye', 'reading', 'pd', 'birth_year']
                            missing_fields = []
                            
                            for field in required_fields:
                                if field not in data or not data[field]:
                                    missing_fields.append(field)
                            
                            if missing_fields:
                                print(f"      ⚠️  MISSING PRESCRIPTION FIELDS: {missing_fields}")
                            else:
                                print(f"      ✅ ALL PRESCRIPTION FIELDS PRESENT")
                    else:
                        print(f"      📷 UPLOADED PRESCRIPTION")
                        print(f"         File: {prescription.get('fileName', 'NOT_SET')}")
                else:
                    print(f"      ❌ NO PRESCRIPTION DATA")
                    
                    # Check if this is your LEON item
                    if 'LEON' in item.get('name', '') and 'M.1795.SQ' in item.get('name', ''):
                        print(f"      🎯 FOUND YOUR LEON ITEM!")
                        print(f"      ❌ THIS ITEM SHOULD HAVE PRESCRIPTION DATA")
        else:
            print(f"   ❌ Failed to get cart: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🔍 Step 2: Check database directly...")
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client.test_db
        collection = db.carts
        
        # Get user's cart from database
        user_cart = collection.find_one({"user_id": "694cfe35835763"})
        
        if user_cart and "items" in user_cart:
            items = user_cart["items"]
            print(f"   ✅ Database items: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\n   🗄️  Database Item {idx + 1}:")
                print(f"      - Name: {item.get('name')}")
                print(f"      - Cart ID: {item.get('cart_id')}")
                print(f"      - Product ID: {item.get('product_id')}")
                print(f"      - Has prescription: {'prescription' in item}")
                print(f"      - Updated at: {item.get('updated_at')}")
                
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
                            print(f"      📊 Database has prescription data")
                            
                            # Check if prescription data is complete
                            required_fields = ['right_eye', 'left_eye', 'reading', 'pd', 'birth_year']
                            missing_fields = []
                            
                            for field in required_fields:
                                if field not in data or not data[field]:
                                    missing_fields.append(field)
                            
                            if missing_fields:
                                print(f"      ⚠️  MISSING PRESCRIPTION FIELDS: {missing_fields}")
                            else:
                                print(f"      ✅ ALL PRESCRIPTION FIELDS PRESENT")
                    else:
                        print(f"      📷 UPLOADED PRESCRIPTION")
                        print(f"         File: {prescription.get('fileName', 'NOT_SET')}")
                else:
                    print(f"      ❌ NO PRESCRIPTION IN DATABASE")
                    
                    # Check if this is your LEON item
                    if 'LEON' in item.get('name', '') and 'M.1795.SQ' in item.get('name', ''):
                        print(f"      🎯 FOUND YOUR LEON ITEM IN DATABASE!")
                        print(f"      ❌ DATABASE MISSING PRESCRIPTION DATA")
        else:
            print(f"   ❌ No cart found in database")
            
        client.close()
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    print("\n🔍 Step 3: Analysis...")
    print("   📋 Possible causes of prescription data loss:")
    print("   1. Prescription update failed (backend error)")
    print("   2. Cart item was updated/modified without preserving prescription")
    print("   3. Cart was cleared and recreated without prescription")
    print("   4. Prescription data was overwritten by empty data")
    print("   5. Database connection issue during update")
    
    print("\n📋 Expected behavior:")
    print("   ✅ If prescription is in database:")
    print("      - All devices should show 'View Prescription'")
    print("      - Data should persist over time")
    print("      - Cross-device sync should work")
    
    print("   ❌ If prescription is NOT in database:")
    print("      - Backend update failed")
    print("      - Data was lost during cart operations")
    print("      - Need to re-enter prescription")
    
    print("\n🔧 Next steps:")
    print("   1. Check backend logs for prescription update errors")
    print("   2. Verify prescription data is being sent correctly")
    print("   3. Check if cart operations are preserving prescription data")
    print("   4. Monitor database changes over time")

if __name__ == "__main__":
    debug_prescription_loss()
