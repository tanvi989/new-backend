#!/usr/bin/env python3

import requests
import json

# Test the payment endpoint with the actual user token
def test_payment():
    url = "https://livebackend.multifolks.com/api/v1/payment/create-session"
    
    # Use the actual token from localStorage
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MTZlYWExNDVjMWE3ZjQ0IiwiZW1haWwiOiJwYXJhZGthcnRhbnZpaUBnbWFpbC5jb20iLCJleHAiOjE3NzI1NjU1MjMsImlhdCI6MTc3MjQ3OTEyM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    test_data = {
        "order_id": "test_order_123",
        "amount": 10.00,
        "currency": "GBP",
        "metadata": {
            "test": "payment_test"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        print(f"Testing payment with original flow")
        response = requests.post(url, json=test_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Payment works!")
        else:
            print("❌ Payment failed")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_payment()
