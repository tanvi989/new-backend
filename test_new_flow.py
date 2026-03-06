#!/usr/bin/env python3

import requests
import json

def test_new_payment_flow():
    """Test the new payment flow: create session -> webhook -> create order on thank you page"""
    
    # Step 1: Create payment session (should work without creating order)
    print("=== Step 1: Create Payment Session ===")
    session_url = "https://testbackend.multifolks.com/api/v1/payment/create-session"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MTZlYWExNDVjMWE3ZjQ0IiwiZW1haWwiOiJwYXJhZGthcnRhbnZpaUBnbWFpbC5jb20iLCJleHAiOjE3NzI1NjU1MjMsImlhdCI6MTc3MjQ3OTEyM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    session_data = {
        "order_id": "test_new_flow_123",
        "amount": 25.00,
        "currency": "GBP",
        "metadata": {
            "test": "new_flow",
            "customer_email": "paradkartanvii@gmail.com"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(session_url, json=session_data, headers=headers)
        print(f"Session Creation Status: {response.status_code}")
        session_result = response.json()
        print(f"Session Response: {json.dumps(session_result, indent=2)}")
        
        if response.status_code == 200 and session_result.get('success'):
            session_id = session_result.get('session_id')
            order_id = session_result.get('order_id')
            print(f"✅ Session created: {session_id}")
            
            # Step 2: Test thank you page order creation
            print(f"\n=== Step 2: Create Order from Thank You Page ===")
            thank_you_url = f"https://testbackend.multifolks.com/api/v1/orders/create-from-payment/{order_id}"
            
            try:
                response = requests.post(thank_you_url, headers=headers)
                print(f"Order Creation Status: {response.status_code}")
                order_result = response.json()
                print(f"Order Response: {json.dumps(order_result, indent=2)}")
                
                if response.status_code == 200 and order_result.get('success'):
                    print(f"✅ Order created successfully: {order_id}")
                    print("✅ New payment flow working correctly!")
                else:
                    print("❌ Order creation failed")
                    
            except Exception as e:
                print(f"Order creation request failed: {e}")
                
        else:
            print("❌ Session creation failed")
            
    except Exception as e:
        print(f"Session creation request failed: {e}")

if __name__ == "__main__":
    test_new_payment_flow()
