#!/usr/bin/env python3
"""
Test request_otp_new template
"""
import requests
import json

# MSG91 Configuration
AUTH_KEY = "482085AD1VnJzkrUX6937ff86P1"
DOMAIN = "email.multifolks.com"
TEMPLATE_ID = "request_otp_new"

def test_template():
    print("=" * 80)
    print("TESTING REQUEST_OTP_NEW TEMPLATE")
    print("=" * 80)
    
    test_email = "paradkartanvii@gmail.com"
    url = "https://control.msg91.com/api/v5/email/send"
    
    headers = {
        "authkey": AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "recipients": [{
            "to": [{
                "name": "Test User",
                "email": test_email
            }],
            "variables": {
                "OTP": "123456"
            }
        }],
        "from": {
            "email": "support@multifolks.com",
            "name": "Multifolks"
        },
        "domain": DOMAIN,
        "template_id": TEMPLATE_ID
    }
    
    try:
        print(f"Sending test email to: {test_email}")
        print(f"Template ID: {TEMPLATE_ID}")
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Test email sent successfully!")
            print(f"Unique ID: {response_data.get('data', {}).get('unique_id', 'N/A')}")
        else:
            print(f"Failed to send test email")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_template()
    
    print("\n" + "=" * 80)
    print("MANUAL UPDATE INSTRUCTIONS")
    print("=" * 80)
    print("To update the template content:")
    print("1. Go to: https://control.msg91.com/")
    print("2. Navigate: Email -> Templates")
    print("3. Find template: request_otp_new")
    print("4. Click 'Edit' and paste your new HTML content")
    print("5. Save the template")
    print("\nBackend is now configured to use request_otp_new for reset PIN emails")
