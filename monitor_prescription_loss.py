#!/usr/bin/env python3

import requests
import json
import time
from pymongo import MongoClient

def monitor_prescription_loss():
    """Monitor prescription data over time to identify when it gets lost"""
    
    print("=== Prescription Loss Monitor ===")
    print("Monitoring prescription data every 10 seconds for 2 minutes")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    }
    
    # Track prescription state over time
    prescription_history = []
    
    for i in range(12):  # 12 iterations * 10 seconds = 2 minutes
        timestamp = time.strftime("%H:%M:%S")
        print(f"\n{'='*60}")
        print(f"🕐 Check {i+1}/12 - {timestamp}")
        print(f"{'='*60}")
        
        # Check API response
        try:
            cart_url = "https://testbackend.multifolks.com/api/v1/cart"
            response = requests.get(cart_url, headers=headers)
            
            if response.status_code == 200:
                cart_data = response.json()
                items = cart_data.get('cart', [])
                
                print(f"📊 API Response - Cart items: {len(items)}")
                
                current_prescriptions = []
                for idx, item in enumerate(items):
                    item_name = item.get('name', 'Unknown')
                    has_prescription = 'prescription' in item
                    
                    print(f"   📦 Item {idx + 1}: {item_name}")
                    print(f"      Has prescription: {has_prescription}")
                    
                    if has_prescription:
                        prescription = item.get('prescription')
                        prescription_type = prescription.get('type', 'UNKNOWN')
                        prescription_mode = prescription.get('mode', 'UNKNOWN')
                        
                        print(f"      Type: {prescription_type}")
                        print(f"      Mode: {prescription_mode}")
                        
                        if prescription_mode == 'manual':
                            data = prescription.get('data', {})
                            right_sph = data.get('right_eye', {}).get('sph', 'NOT_SET')
                            left_sph = data.get('left_eye', {}).get('sph', 'NOT_SET')
                            reading_r = data.get('reading', {}).get('right', 'NOT_SET')
                            reading_l = data.get('reading', {}).get('left', 'NOT_SET')
                            pd_r = data.get('pd', {}).get('right', 'NOT_SET')
                            pd_l = data.get('pd', {}).get('left', 'NOT_SET')
                            birth_year = data.get('birth_year', 'NOT_SET')
                            
                            print(f"      Right SPH: {right_sph}")
                            print(f"      Left SPH: {left_sph}")
                            print(f"      Reading R: {reading_r}")
                            print(f"      Reading L: {reading_l}")
                            print(f"      PD R: {pd_r}")
                            print(f"      PD L: {pd_l}")
                            print(f"      Birth Year: {birth_year}")
                            
                            current_prescriptions.append({
                                'item_name': item_name,
                                'cart_id': item.get('cart_id'),
                                'product_id': item.get('product_id'),
                                'type': prescription_type,
                                'mode': prescription_mode,
                                'right_sph': right_sph,
                                'left_sph': left_sph,
                                'reading_r': reading_r,
                                'reading_l': reading_l,
                                'pd_r': pd_r,
                                'pd_l': pd_l,
                                'birth_year': birth_year
                            })
                        elif prescription_mode == 'upload':
                            print(f"      File: {prescription.get('fileName', 'NOT_SET')}")
                            current_prescriptions.append({
                                'item_name': item_name,
                                'cart_id': item.get('cart_id'),
                                'product_id': item.get('product_id'),
                                'type': prescription_type,
                                'mode': prescription_mode,
                                'file': prescription.get('fileName', 'NOT_SET')
                            })
                    else:
                        print(f"      ❌ NO PRESCRIPTION")
                        
                        # Check if this is your LEON item
                        if 'LEON' in item_name and 'M.1795.SQ' in item_name:
                            print(f"      🎯 FOUND YOUR LEON ITEM - MISSING PRESCRIPTION!")
                
                # Record this check
                prescription_history.append({
                    'timestamp': timestamp,
                    'check_number': i+1,
                    'prescriptions': current_prescriptions,
                    'total_items': len(items),
                    'items_with_prescription': len(current_prescriptions)
                })
                
                # Check for changes
                if i > 0:
                    prev_prescriptions = prescription_history[i-1]['prescriptions']
                    current_count = len(current_prescriptions)
                    prev_count = len(prev_prescriptions)
                    
                    if current_count < prev_count:
                        print(f"   ⚠️  PRESCRIPTION COUNT DECREASED!")
                        print(f"      Before: {prev_count} prescriptions")
                        print(f"      After: {current_count} prescriptions")
                        print(f"      Lost: {prev_count - current_count} prescriptions")
                        
                        # Find which prescription was lost
                        lost_prescriptions = []
                        for prev in prev_prescriptions:
                            found = False
                            for curr in current_prescriptions:
                                if (curr.get('cart_id') == prev.get('cart_id') and 
                                    curr.get('product_id') == prev.get('product_id')):
                                    found = True
                                    break
                            if not found:
                                lost_prescriptions.append(prev)
                        
                        for lost in lost_prescriptions:
                            print(f"      📋 Lost prescription: {lost.get('item_name')} ({lost.get('mode')})")
                    elif current_count > prev_count:
                        print(f"   ✅ PRESCRIPTION COUNT INCREASED!")
                        print(f"      Before: {prev_count} prescriptions")
                        print(f"      After: {current_count} prescriptions")
                    else:
                        print(f"   ✅ PRESCRIPTION COUNT STABLE: {current_count}")
                
            else:
                print(f"   ❌ API request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Check database directly
        try:
            client = MongoClient("mongodb://localhost:27017")
            db = client.test_db
            collection = db.cart
            
            user_cart = collection.find_one({"user_id": "694cfe35835763"})
            
            if user_cart and "items" in user_cart:
                items = user_cart["items"]
                db_prescriptions = 0
                
                for item in items:
                    if 'prescription' in item:
                        db_prescriptions += 1
                
                print(f"   🗄️  Database - Items with prescription: {db_prescriptions}/{len(items)}")
                
                # Compare with API
                if i > 0:
                    api_count = prescription_history[i]['items_with_prescription']
                    if db_prescriptions != api_count:
                        print(f"      ⚠️  DATABASE/API MISMATCH!")
                        print(f"         Database: {db_prescriptions}")
                        print(f"         API: {api_count}")
                    else:
                        print(f"      ✅ Database/API match: {db_prescriptions}")
            else:
                print(f"   🗄️  Database - No cart found")
            
            client.close()
            
        except Exception as e:
            print(f"   ❌ Database error: {e}")
        
        # Wait for next check
        if i < 11:  # Don't wait after the last check
            print(f"⏳ Waiting 10 seconds...")
            time.sleep(10)
    
    # Final analysis
    print(f"\n{'='*60}")
    print("📊 FINAL ANALYSIS")
    print(f"{'='*60}")
    
    if len(prescription_history) > 0:
        initial_count = prescription_history[0]['items_with_prescription']
        final_count = prescription_history[-1]['items_with_prescription']
        
        print(f"📈 Prescription count over time:")
        for i, record in enumerate(prescription_history):
            count = record['items_with_prescription']
            timestamp = record['timestamp']
            status = "✅" if count > 0 else "❌"
            print(f"   {status} {timestamp}: {count} prescriptions")
        
        print(f"\n📋 Summary:")
        print(f"   Initial prescriptions: {initial_count}")
        print(f"   Final prescriptions: {final_count}")
        
        if final_count < initial_count:
            print(f"   ⚠️  PRESCRIPTIONS LOST: {initial_count - final_count}")
            print(f"   🔍 Issue: Something is removing prescription data")
        elif final_count == 0:
            print(f"   ❌ ALL PRESCRIPTIONS LOST!")
            print(f"   🔍 Issue: Complete prescription data loss")
        else:
            print(f"   ✅ PRESCRIPTIONS PRESERVED")
            print(f"   🔍 Issue might be elsewhere (frontend caching)")
        
        print(f"\n🔧 Possible causes:")
        print(f"   1. Cart update operations clearing prescription data")
        print(f"   2. Backend processes removing prescription data")
        print(f"   3. Database operations overwriting prescription data")
        print(f"   4. Frontend cache issues (if database has data)")
        print(f"   5. Session/authentication issues")

if __name__ == "__main__":
    monitor_prescription_loss()
