#!/usr/bin/env python3

import requests
import json

def test_minimal_session():
    """Test with minimal metadata to isolate the datetime issue"""
    
    session_url = "https://testbackend.multifolks.com/api/v1/payment/create-session"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjk0Y2ZlMzU4MTZlYWExNDVjMWE3ZjQ0IiwiZW1haWwiOiJwYXJhZGthcnRhbnZpaUBnbWFpbC5jb20iLCJleHAiOjE3NzI1NjU1MjMsImlhdCI6MTc3MjQ3OTEyM30.Hyl2rCGwO5-R5FvRPnMvcqcSU_R91oOnIxc9K48ch6M"
    
    # Test with absolutely minimal metadata
    minimal_data = {
        "order_id": "MINIMAL_TEST_123",
        "amount": 5.00,
        "currency": "GBP"
        # NO METADATA - this should work if datetime is in metadata
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    print("=== Testing Minimal Session (No Metadata) ===")
    
    try:
        response = requests.post(session_url, json=minimal_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Minimal session works!")
        else:
            print("❌ Even minimal session fails - datetime issue is elsewhere")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_minimal_session()
