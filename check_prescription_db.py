#!/usr/bin/env python3

import requests
import json
from pymongo import MongoClient

def check_prescription_in_db():
    """Check what prescription data is actually stored in database"""
    
    print("=== Prescription Database Check ===")
    print("Checking what prescription data is stored vs what should be stored")
    
    # Headers for API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    }
    
    print("\n🔍 Step 1: Getting cart data via API...")
    try:
        cart_url = "https://livebackend.multifolks.com/api/v1/cart"
        response = requests.get(cart_url, headers=headers)
        
        if response.status_code == 200:
            cart_data = response.json()
            items = cart_data.get('cart', [])
            
            print(f"   ✅ API Response - Cart items: {len(items)}")
            
            if items:
                for idx, item in enumerate(items):
                    print(f"\n   📦 API Item {idx + 1}:")
                    print(f"      - Name: {item.get('name')}")
                    print(f"      - Cart ID: {item.get('cart_id')}")
                    print(f"      - Product ID: {item.get('product_id')}")
                    print(f"      - Has prescription: {'prescription' in item}")
                    
                    # Check lens data
                    if 'lens' in item:
                        lens = item.get('lens', {})
                        print(f"      - Lens Type: {lens.get('main_category', 'NOT_SET')}")
                        print(f"      - Lens Index: {lens.get('lens_package', 'NOT_SET')}")
                        print(f"      - Tint Type: {lens.get('tint_type', 'NOT_SET')}")
                        print(f"      - Tint Color: {lens.get('tint_color', 'NOT_SET')}")
                    
                    # Check prescription data
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
                        elif prescription.get('mode') == 'upload':
                            print(f"         📷 UPLOADED PRESCRIPTION")
                            print(f"         File: {prescription.get('fileName', 'NOT_SET')}")
                            print(f"         GCS URL: {prescription.get('gcs_url', 'NOT_SET')}")
                        else:
                            print(f"         ❓ UNKNOWN MODE: {prescription.get('mode')}")
                    else:
                        print(f"      ❌ NO PRESCRIPTION DATA")
            else:
                print(f"      ⚠️  NO ITEMS IN CART")
        else:
            print(f"   ❌ API request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ API request error: {e}")
    
    print("\n🔍 Step 2: Checking database directly...")
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client.test_db
        collection = db.carts
        
        # Get user's cart from database
        user_cart = collection.find_one({"user_id": "694cfe35835763"})
        
        if user_cart and "items" in user_cart:
            items = user_cart["items"]
            print(f"   ✅ Database - Cart items: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\n   🗄️  Database Item {idx + 1}:")
                print(f"      - Name: {item.get('name')}")
                print(f"      - Cart ID: {item.get('cart_id')}")
                print(f"      - Product ID: {item.get('product_id')}")
                print(f"      - Has prescription: {'prescription' in item}")
                
                # Check lens data
                if 'lens' in item:
                    lens = item.get('lens', {})
                    print(f"      - Lens Type: {lens.get('main_category', 'NOT_SET')}")
                    print(f"      - Lens Index: {lens.get('lens_package', 'NOT_SET')}")
                    print(f"      - Tint Type: {lens.get('tint_type', 'NOT_SET')}")
                    print(f"      - Tint Color: {lens.get('tint_color', 'NOT_SET')}")
                
                # Check prescription data
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
                    elif prescription.get('mode') == 'upload':
                        print(f"         📷 UPLOADED PRESCRIPTION")
                        print(f"         File: {prescription.get('fileName', 'NOT_SET')}")
                        print(f"         GCS URL: {prescription.get('gcs_url', 'NOT_SET')}")
                    else:
                        print(f"         ❓ UNKNOWN MODE: {prescription.get('mode')}")
                else:
                    print(f"      ❌ NO PRESCRIPTION DATA IN DATABASE")
        else:
            print(f"   ❌ No cart found in database for user")
            
        client.close()
        
    except Exception as e:
        print(f"   ❌ Database connection error: {e}")
    
    print("\n🔍 Step 3: Analysis...")
    print("   📋 What this tells us:")
    print("   ✅ If prescription is in database but not in API response:")
    print("      - Backend storage is working")
    print("      - Frontend is not reading it correctly")
    print("   ❌ If prescription is NOT in database:")
    print("      - Backend storage is failing")
    print("      - Prescription update didn't work")
    
    print("\n📋 Expected behavior:")
    print("   - PC 1: Shows 'View Prescription' (has prescription)")
    print("   - PC 2: Should also show 'View Prescription' (same prescription)")
    print("   - If PC 2 shows 'Add Prescription', prescription data is missing")

if __name__ == "__main__":
    check_prescription_in_db()
