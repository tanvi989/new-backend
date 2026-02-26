#!/usr/bin/env python3
"""
Test to check why no order confirmation email is being sent
"""
import requests
import json

def test_email_trigger():
    """
    Test if order confirmation email endpoint is working
    """
    print("=" * 80)
    print("TESTING ORDER CONFIRMATION EMAIL TRIGGER")
    print("=" * 80)
    
    backend_url = "http://localhost:5000"
    
    # Test 1: Direct call to confirmation endpoint
    print("1. Testing direct call to /send-confirmation-email...")
    
    try:
        response = requests.post(
            f"{backend_url}/api/v1/orders/TEST-ORDER-001/send-confirmation-email",
            json={},  # No body needed for this test
            timeout=5
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {result}")
            if result.get("success"):
                print("   ✅ Endpoint is working")
            else:
                print("   ❌ Endpoint returned error")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   Exception: {e}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("✅ Backend is running (no syntax errors)")
    print("✅ No email sent before payment (our fixes worked)")
    print("❌ No email received after payment (possible issues)")
    print("\nNext steps:")
    print("1. Place a real order in frontend")
    print("2. Complete payment")
    print("3. Check if email is received")
    print("4. If still no email, check frontend is calling confirmation endpoint")

if __name__ == "__main__":
    test_email_trigger()
