#!/usr/bin/env python3
"""
Test to verify exact template content being sent
"""
import requests
import json

def test_template_content():
    print("=" * 80)
    print("TESTING TEMPLATE CONTENT VERIFICATION")
    print("=" * 80)
    
    # MSG91 API to get template details
    AUTH_KEY = "482085AD1VnJzkrUX6937ff86P1"
    TEMPLATE_ID = "request_otp_new"
    
    # Try to get template info (if API supports it)
    try:
        url = f"https://control.msg91.com/api/v5/email/template/{TEMPLATE_ID}"
        headers = {
            "authkey": AUTH_KEY,
            "Content-Type": "application/json"
        }
        
        print(f"Trying to get template info for: {TEMPLATE_ID}")
        response = requests.get(url, headers=headers)
        
        print(f"Template info response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Template data: {json.dumps(data, indent=2)}")
        else:
            print(f"Failed to get template info: {response.text}")
            
    except Exception as e:
        print(f"Error getting template info: {e}")
    
    # Send a test email and check what variables are actually sent
    print("\n" + "=" * 60)
    print("SENDING TEST EMAIL TO CHECK VARIABLES")
    print("=" * 60)
    
    test_email = "paradkartanvii@gmail.com"
    url = "https://control.msg91.com/api/v5/email/send"
    
    # Use a unique test OTP to identify this specific email
    test_otp = "987654"
    
    payload = {
        "recipients": [{
            "to": [{
                "name": "Template Test",
                "email": test_email
            }],
            "variables": {
                "OTP": test_otp,
                "oneTimePin": test_otp,
                "name": "Template Test",
                "firstName": "Template Test"
            }
        }],
        "from": {
            "email": "support@multifolks.com",
            "name": "Multifolks"
        },
        "domain": "email.multifolks.com",
        "template_id": TEMPLATE_ID
    }
    
    try:
        print(f"Sending test email with OTP: {test_otp}")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Email sent successfully!")
            print(f"Unique ID: {data.get('data', {}).get('unique_id', 'N/A')}")
            print(f"\nCheck your email for:")
            print(f"- Subject line")
            print(f"- Email content")
            print(f"- The OTP should be: {test_otp}")
            print(f"- If you see old template, MSG91 is using cached version")
        else:
            print(f"Failed to send email: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_template_content()
    
    print("\n" + "=" * 80)
    print("TROUBLESHOOTING STEPS")
    print("=" * 80)
    print("If you still see old template:")
    print("1. Go to MSG91 Dashboard")
    print("2. Find template: request_otp_new")
    print("3. Click 'Edit' -> 'Source' tab")
    print("4. Verify HTML content is updated")
    print("5. Click 'Save' and wait 2-3 minutes")
    print("6. Try clearing browser cache and refreshing MSG91 dashboard")
    print("7. Contact MSG91 support if template cache issue persists")
