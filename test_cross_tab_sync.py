#!/usr/bin/env python3

import requests
import json
import time

def test_cross_tab_sync():
    """Test cross-tab prescription data sync"""
    
    print("=== Cross-Tab Prescription Sync Test ===")
    print("This test simulates opening cart in multiple tabs/browsers")
    
    # Test data - the prescription you mentioned
    expected_prescription = {
        "type": "manual",
        "mode": "manual", 
        "data": {
            "right_eye": {"sph": "0.00", "cyl": "0.00", "axis": "-"},
            "left_eye": {"sph": "0.00", "cyl": "0.00", "axis": "-"},
            "reading": {"right": "3.25", "left": "2.75"},
            "pd": {"right": "23.25", "left": "23.25"},
            "birth_year": "2000"
        }
    }
    
    print("\n📋 Expected prescription data:")
    print(f"   Right Eye SPH: {expected_prescription['data']['right_eye']['sph']}")
    print(f"   Left Eye SPH: {expected_prescription['data']['left_eye']['sph']}")
    print(f"   Reading R: {expected_prescription['data']['reading']['right']}")
    print(f"   Reading L: {expected_prescription['data']['reading']['left']}")
    print(f"   PD R: {expected_prescription['data']['pd']['right']}")
    print(f"   PD L: {expected_prescription['data']['pd']['left']}")
    print(f"   Birth Year: {expected_prescription['data']['birth_year']}")
    
    # Simulate multiple "tab" requests with different headers
    tabs = [
        ("Desktop Tab 1", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"),
        ("Desktop Tab 2", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"),
        ("Mobile Tab", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
    ]
    
    print("\n🔍 Testing cart data across multiple tabs:")
    
    for tab_name, user_agent in tabs:
        print(f"\n   📱 {tab_name}:")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M",
            "User-Agent": user_agent
        }
        
        try:
            # Get cart data
            cart_url = "http://localhost:5000/api/v1/cart"
            response = requests.get(cart_url, headers=headers)
            
            if response.status_code == 200:
                cart_data = response.json()
                items = cart_data.get('cart', [])
                
                if items:
                    item = items[0]  # Check first item
                    has_prescription = 'prescription' in item
                    
                    if has_prescription:
                        prescription = item.get('prescription')
                        mode = prescription.get('mode', 'unknown')
                        
                        if mode == 'manual':
                            data = prescription.get('data', {})
                            
                            # Check if it matches expected values
                            actual_values = {
                                'right_eye_sph': str(data.get('right_eye', {}).get('sph', 'NOT_SET')),
                                'left_eye_sph': str(data.get('left_eye', {}).get('sph', 'NOT_SET')),
                                'reading_right': str(data.get('reading', {}).get('right', 'NOT_SET')),
                                'reading_left': str(data.get('reading', {}).get('left', 'NOT_SET')),
                                'pd_right': str(data.get('pd', {}).get('right', 'NOT_SET')),
                                'pd_left': str(data.get('pd', {}).get('left', 'NOT_SET')),
                                'birth_year': str(data.get('birth_year', 'NOT_SET'))
                            }
                            
                            expected_values = {
                                'right_eye_sph': expected_prescription['data']['right_eye']['sph'],
                                'left_eye_sph': expected_prescription['data']['left_eye']['sph'],
                                'reading_right': expected_prescription['data']['reading']['right'],
                                'reading_left': expected_prescription['data']['reading']['left'],
                                'pd_right': expected_prescription['data']['pd']['right'],
                                'pd_left': expected_prescription['data']['pd']['left'],
                                'birth_year': expected_prescription['data']['birth_year']
                            }
                            
                            print(f"     ✅ MANUAL PRESCRIPTION FOUND")
                            print(f"     📊 Data comparison:")
                            
                            all_match = True
                            for key, expected in expected_values.items():
                                actual = actual_values.get(key, 'MISSING')
                                status = "✅" if actual == expected else "❌"
                                if actual != expected:
                                    all_match = False
                                print(f"       {status} {key}: {expected} vs {actual}")
                            
                            if all_match:
                                print(f"     🎉 {tab_name}: All prescription data matches!")
                            else:
                                print(f"     ⚠️ {tab_name}: Some prescription data mismatch")
                        else:
                            print(f"     📷 {tab_name}: UPLOADED PRESCRIPTION (mode: {mode})")
                    else:
                        print(f"     ❌ {tab_name}: NO PRESCRIPTION DATA")
                else:
                    print(f"     ⚠️ {tab_name}: NO ITEMS IN CART")
            else:
                print(f"     ❌ {tab_name}: Failed to get cart ({response.status_code})")
                
        except Exception as e:
            print(f"     ❌ {tab_name}: Error - {e}")
    
    print("\n=== Cross-Tab Sync Analysis ===")
    print("✅ If all tabs show the same prescription data, sync is working")
    print("❌ If tabs show different data, there's a sync issue")
    print("\n🔧 Possible causes of sync issues:")
    print("  1. Frontend caching (localStorage/sessionStorage)")
    print("  2. React Query cache not invalidated")
    print("  3. Backend prescription data not stored correctly")
    print("  4. Different user sessions/tokens")
    print("  5. Browser storage interference")
    
    print("\n🧪 Testing solutions:")
    print("  1. Clear browser localStorage/sessionStorage")
    print("  2. Hard refresh (Ctrl+F5) the cart page")
    print("  3. Open in incognito/private window")
    print("  4. Check browser developer tools for cache issues")

if __name__ == "__main__":
    test_cross_tab_sync()
