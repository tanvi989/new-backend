#!/usr/bin/env python3

import requests
import json

def check_payment_session():
    """Check if the payment session exists in the database"""
    
    order_id = "ORD-1772509249485"
    session_id = "cs_test_a1RZo1tCVtLnN0IralFVmrbVGbMVNFDYHr6bJ7SqYQjNAQ76WZ79o16eCU"
    
    print(f"=== Checking Payment Session ===")
    print(f"Order ID: {order_id}")
    print(f"Session ID: {session_id}")
    
    # Check if payment session exists in database
    try:
        # This would require a direct database connection, but let's try a simple endpoint first
        health_url = "https://testbackend.multifolks.com/api/health"
        response = requests.get(health_url)
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Backend is running: {health_data.get('message')}")
            print(f"MongoDB: {health_data.get('mongodb')}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Try to create a simple test session first
    print(f"\n=== Creating Test Payment Session ===")
    session_url = "https://testbackend.multifolks.com/api/v1/payment/create-session"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MTZlYWExNDVjMWE3ZjQ0IiwiZW1haWwiOiJwYXJhZGthcnRhbnZpaUBnbWFpbC5jb20iLCJleHAiOjE3NzI1NjU1MjMsImlhdCI6MTc3MjQ3OTEyM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    test_data = {
        "order_id": "TEST_ORDER_123",
        "amount": 10.00,
        "currency": "GBP",
        "metadata": {
            "test": "simple_test"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(session_url, json=test_data, headers=headers)
        print(f"Test Session Status: {response.status_code}")
        print(f"Test Session Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            test_session_id = result.get('session_id')
            print(f"✅ Test session created: {test_session_id}")
            
            # Now try to create order from this test session
            print(f"\n=== Creating Order from Test Session ===")
            order_url = f"https://testbackend.multifolks.com/api/v1/orders/create-from-payment/TEST_ORDER_123"
            
            try:
                order_response = requests.post(order_url, headers=headers)
                print(f"Order Creation Status: {order_response.status_code}")
                print(f"Order Creation Response: {order_response.text}")
                
            except Exception as e:
                print(f"Order creation failed: {e}")
                
    except Exception as e:
        print(f"Test session creation failed: {e}")

if __name__ == "__main__":
    check_payment_session()
