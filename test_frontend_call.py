#!/usr/bin/env python3
"""
Test if frontend is calling the confirmation endpoint correctly
"""
import requests
import json

def test_frontend_call():
    """
    Test the confirmation endpoint with a real order ID
    """
    print("=" * 80)
    print("TESTING FRONTEND CALL TO CONFIRMATION ENDPOINT")
    print("=" * 80)
    
    backend_url = "http://localhost:5000"
    
    # Test with a real order ID (you need to replace this with your actual order ID)
    test_order_id = "TEST-ORDER-FRONTEND-001"
    
    print(f"Testing with Order ID: {test_order_id}")
    print("Note: Replace TEST-ORDER-FRONTEND-001 with your actual order ID")
    
    try:
        # First, let's check if the order exists
        print(f"\n1. Checking if order exists...")
        response = requests.get(f"{backend_url}/api/v1/orders/{test_order_id}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 404:
            print("   Order not found - this is expected for test order")
            print("   The endpoint should still work and send fallback email")
        elif response.status_code == 200:
            print("   Order found - will send email with real order data")
        else:
            print(f"   Unexpected response: {response.text}")
            return
        
        # Now test the confirmation endpoint
        print(f"\n2. Testing confirmation endpoint...")
        response = requests.post(
            f"{backend_url}/api/v1/orders/{test_order_id}/send-confirmation-email",
            json={},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("   ✅ Confirmation email sent successfully!")
                print("   Check your email at paradkartanvii@gmail.com")
            else:
                print("   ❌ Confirmation email failed")
        else:
            print(f"   ❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 80)
    print("FRONTEND DEBUGGING STEPS")
    print("=" * 80)
    print("1. Open browser developer tools (F12)")
    print("2. Go to Console tab")
    print("3. Complete a payment in your frontend")
    print("4. Look for these console messages:")
    print("   - [PaymentSuccess] Attempting to send confirmation email...")
    print("   - [PaymentSuccess] Order ID: YOUR-ORDER-ID")
    print("   - [PaymentSuccess] Auth Token: Present/Missing")
    print("   - [PaymentSuccess] Response status: 200")
    print("   - [PaymentSuccess] Order confirmation email sent successfully")
    print("\n5. If you see errors, check:")
    print("   - Order ID is missing")
    print("   - Auth Token is missing")
    print("   - Response status is not 200")
    print("   - Response data shows error message")

if __name__ == "__main__":
    test_frontend_call()
