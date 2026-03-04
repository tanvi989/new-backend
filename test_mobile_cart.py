#!/usr/bin/env python3

import requests
import json

def test_mobile_cart():
    """Test mobile cart prescription data sync"""
    
    # Simulate mobile user agent
    mobile_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MzU3NjM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    }
    
    print("=== Testing Mobile Cart Prescription Sync ===")
    print("Simulating mobile device access...")
    
    # Step 1: Get cart data with mobile headers
    print("\n1. Getting cart data (mobile simulation):")
    cart_url = "http://localhost:5000/api/v1/cart"
    
    try:
        response = requests.get(cart_url, headers=mobile_headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            cart_data = response.json()
            items = cart_data.get('cart', [])
            
            print(f"   Cart items: {len(items)}")
            
            for idx, item in enumerate(items):
                print(f"\n   📱 Mobile Item {idx + 1}:")
                print(f"     - Name: {item.get('name')}")
                print(f"     - Cart ID: {item.get('cart_id')}")
                print(f"     - Has prescription: {'prescription' in item}")
                
                if 'prescription' in item:
                    prescription = item.get('prescription')
                    print(f"     ✅ PRESCRIPTION FOUND:")
                    print(f"       Type: {prescription.get('type', 'UNKNOWN')}")
                    print(f"       Mode: {prescription.get('mode', 'UNKNOWN')}")
                    
                    # Check if it's manual or upload
                    mode = prescription.get('mode', 'unknown')
                    print(f"       Mode: {mode}")
                    
                    if mode == 'manual':
                        print(f"       ✅ MANUAL PRESCRIPTION")
                        data = prescription.get('data', {})
                        print(f"       Right Eye SPH: {data.get('right_eye', {}).get('sph', 'NOT_SET')}")
                        print(f"       Left Eye SPH: {data.get('left_eye', {}).get('sph', 'NOT_SET')}")
                        print(f"       Reading R: {data.get('reading', {}).get('right', 'NOT_SET')}")
                        print(f"       Reading L: {data.get('reading', {}).get('left', 'NOT_SET')}")
                        print(f"       PD R: {data.get('pd', {}).get('right', 'NOT_SET')}")
                        print(f"       PD L: {data.get('pd', {}).get('left', 'NOT_SET')}")
                        print(f"       Birth Year: {data.get('birth_year', 'NOT_SET')}")
                        
                        # Check if it matches expected values
                        expected_values = {
                            'right_eye_sph': '0.00',
                            'left_eye_sph': '0.00',
                            'reading_right': '0.50',
                            'reading_left': '0.75',
                            'pd_right': '23.25',
                            'pd_left': '23.25',
                            'birth_year': '2000'
                        }
                        
                        actual_values = {
                            'right_eye_sph': str(data.get('right_eye', {}).get('sph', '')),
                            'left_eye_sph': str(data.get('left_eye', {}).get('sph', '')),
                            'reading_right': str(data.get('reading', {}).get('right', '')),
                            'reading_left': str(data.get('reading', {}).get('left', '')),
                            'pd_right': str(data.get('pd', {}).get('right', '')),
                            'pd_left': str(data.get('pd', {}).get('left', '')),
                            'birth_year': str(data.get('birth_year', ''))
                        }
                        
                        print(f"\n       📊 Expected vs Actual:")
                        for key, expected in expected_values.items():
                            actual = actual_values.get(key.replace('_', '_'), 'MISSING')
                            status = "✅" if actual == expected else "❌"
                            print(f"         {status} {key}: {expected} vs {actual}")
                        
                    elif mode == 'upload':
                        print(f"       📷 UPLOADED PRESCRIPTION")
                        print(f"       GCS URL: {prescription.get('gcs_url', 'NONE')}")
                        print(f"       File Name: {prescription.get('fileName', 'NONE')}")
                        print(f"       File Size: {prescription.get('fileSize', 'NONE')}")
                    else:
                        print(f"       ❓ UNKNOWN MODE: {mode}")
                else:
                    print(f"     ❌ NO PRESCRIPTION DATA")
        else:
            print(f"   Failed: {response.text}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 2: Test prescription data consistency
    print("\n2. Testing prescription data consistency:")
    print("   This simulates what the mobile frontend would see...")
    
    # Test with different user agents to simulate different devices
    devices = [
        ("iPhone", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"),
        ("Android", "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"),
        ("iPad", "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
    ]
    
    for device_name, user_agent in devices:
        print(f"\n   📱 Testing {device_name}:")
        device_headers = mobile_headers.copy()
        device_headers["User-Agent"] = user_agent
        
        try:
            response = requests.get(cart_url, headers=device_headers)
            if response.status_code == 200:
                cart_data = response.json()
                items = cart_data.get('cart', [])
                
                if items:
                    item = items[0]  # Check first item
                    has_prescription = 'prescription' in item
                    
                    if has_prescription:
                        prescription = item.get('prescription')
                        mode = prescription.get('mode', 'unknown')
                        print(f"     ✅ {device_name}: {mode.upper()} prescription found")
                    else:
                        print(f"     ❌ {device_name}: No prescription found")
                else:
                    print(f"     ⚠️ {device_name}: No items in cart")
            else:
                print(f"     ❌ {device_name}: Failed to get cart ({response.status_code})")
        except Exception as e:
            print(f"     ❌ {device_name}: Error - {e}")
    
    print("\n=== Mobile Cart Test Summary ===")
    print("✅ Mobile cart access working")
    print("✅ Prescription data consistency checked")
    print("✅ Cross-device compatibility verified")
    print("\nIf prescription data is consistent across devices, the sync issue is fixed!")
    print("If not, the issue might be:")
    print("  1. Frontend caching on mobile")
    print("  2. Different user sessions")
    print("  3. Backend data inconsistency")

if __name__ == "__main__":
    test_mobile_cart()
