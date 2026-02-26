#!/usr/bin/env python3
"""
Test the live confirmation email endpoint
"""
import requests
import json

def test_live_endpoint():
    """
    Test the live backend confirmation email endpoint
    """
    print("=" * 80)
    print("TESTING LIVE BACKEND CONFIRMATION EMAIL ENDPOINT")
    print("=" * 80)
    
    live_url = "https://testbackend.multifolks.com"
    order_id = "TEST-ORDER-LIVE"
    
    print(f"Testing endpoint: {live_url}/api/v1/orders/{order_id}/send-confirmation-email")
    
    try:
        # Test the endpoint
        response = requests.post(
            f"{live_url}/api/v1/orders/{order_id}/send-confirmation-email",
            json={},
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer test-token',
            },
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response JSON: {response_data}")
        except:
            print(f"Response Text: {response.text[:500]}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Endpoint is working!")
        elif response.status_code == 401:
            print("✅ EXPECTED: 401 (Invalid token) - Endpoint exists and working")
        elif response.status_code == 405:
            print("❌ ERROR: 405 (Method Not Allowed) - Endpoint missing")
        else:
            print(f"⚠️  UNEXPECTED: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("1. If you see 401 or 200, the endpoint is working!")
    print("2. Complete a real payment on the live frontend")
    print("3. Check browser console for:")
    print("   - [PaymentSuccess] Response status: 200")
    print("   - [PaymentSuccess] Order confirmation email sent successfully")
    print("4. Check your email for the confirmation")

if __name__ == "__main__":
    test_live_endpoint()
