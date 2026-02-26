#!/usr/bin/env python3
"""
Test real password reset functionality
"""
import requests
import json

def test_password_reset():
    print("=" * 80)
    print("TESTING REAL PASSWORD RESET FUNCTIONALITY")
    print("=" * 80)
    
    # Backend URL
    backend_url = "http://localhost:5000"
    
    # Test email
    test_email = "paradkartanvii@gmail.com"
    
    # Trigger password reset
    reset_url = f"{backend_url}/api/v1/auth/forgot-password"
    
    payload = {
        "email": test_email
    }
    
    try:
        print(f"Sending password reset request for: {test_email}")
        print(f"URL: {reset_url}")
        
        response = requests.post(reset_url, json=payload)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Password reset request successful!")
            print(f"Response: {json.dumps(response_data, indent=2)}")
            
            # Check if MSG91 is configured
            print(f"\nCheck the backend console for:")
            print(f"- Generated PIN for {test_email}")
            print(f"- MSG91 send confirmation")
            
        else:
            print(f"Password reset request failed")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_password_reset()
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("1. Check your email for the actual OTP")
    print("2. The OTP should be a random 6-digit number (not 123456)")
    print("3. If you still see 123456, check the backend console logs")
    print("4. The template should use {{OTP}} variable to display the actual PIN")
