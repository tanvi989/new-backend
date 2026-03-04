#!/usr/bin/env python3

import requests
import json

def test_payment_success_flow():
    """
    Test the payment success flow - this simulates what the frontend would do
    when the user lands on the payment success page
    """
    
    # This is the data from the URL you provided
    order_id = "ORD-1772509249485"
    session_id = "cs_test_a1RZo1tCVtLnN0IralFVmrbVGbMVNFDYHr6bJ7SqYQjNAQ76WZ79o16eCU"
    
    # User token (you would get this from localStorage)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MTZlYWExNDVjMWE3ZjQ0IiwiZW1haWwiOiJwYXJhZGthcnRhbnZpaUBnbWFpbC5jb20iLCJleHAiOjE3NzI1NjU1MjMsImlhdCI6MTc3MjQ3OTEyM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    print(f"=== Payment Success Flow ===")
    print(f"Order ID: {order_id}")
    print(f"Session ID: {session_id}")
    
    # Step 1: Call the new endpoint to create order from payment
    print(f"\n=== Step 1: Create Order from Payment ===")
    create_order_url = f"http://localhost:5000/api/v1/orders/create-from-payment/{order_id}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(create_order_url, headers=headers)
        print(f"Order Creation Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Order created successfully!")
            print(f"Order ID: {result.get('order_id')}")
            print(f"Message: {result.get('message')}")
            
            # Step 2: Send confirmation email (optional)
            print(f"\n=== Step 2: Send Confirmation Email ===")
            email_url = f"http://localhost:5000/api/v1/orders/{order_id}/send-confirmation-email"
            
            try:
                email_response = requests.post(email_url, headers=headers)
                print(f"Email Status: {email_response.status_code}")
                
                if email_response.status_code == 200:
                    email_result = email_response.json()
                    print(f"✅ Confirmation email sent: {email_result.get('message')}")
                else:
                    print(f"❌ Email failed: {email_response.text}")
                    
            except Exception as e:
                print(f"Email request failed: {e}")
                
        else:
            print(f"❌ Order creation failed: {response.text}")
            
    except Exception as e:
        print(f"Order creation request failed: {e}")
    
    print(f"\n=== Flow Complete ===")

if __name__ == "__main__":
    test_payment_success_flow()
