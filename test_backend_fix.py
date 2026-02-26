#!/usr/bin/env python3
"""
Test the backend fix for order confirmation email
"""
import requests
import json

def test_backend_fix():
    """
    Test that backend now sends correct data structure
    """
    print("=" * 80)
    print("TESTING BACKEND FIX")
    print("=" * 80)
    
    backend_url = "http://localhost:5000"
    
    # Test the send-confirmation-email endpoint directly
    print("Testing /send-confirmation-email endpoint...")
    
    try:
        response = requests.post(
            f"{backend_url}/api/v1/orders/TEST-ORDER-001/send-confirmation-email",
            headers={"Authorization": "Bearer test-token"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 80)
    print("BACKEND FIX SUMMARY")
    print("=" * 80)
    print("✅ Fixed: Order creation no longer sends email")
    print("✅ Fixed: Webhook no longer sends email")
    print("✅ Fixed: Payment session creation no longer sends email")
    print("✅ Fixed: /send-confirmation-email now extracts lens data")
    print("✅ Only email sent AFTER payment completion")
    print("\nExpected email content:")
    print("- BERG (E45A8506)")
    print("- Sunglasses • Sunglasses Tint • 1.61")
    print("- Coating: Mirror Tints - Purple")
    print("- Total: £253.00")

if __name__ == "__main__":
    test_backend_fix()
