import sys
sys.path.append('/home/selfeey-india/Documents/AI_Projects/login_api')
import config
from notification_service import MSG91Service
import requests

print("=" * 80)
print("DEBUGGING MSG91 EMAIL DELIVERY")
print("=" * 80)

# Initialize MSG91 Service
msg91 = MSG91Service()

print("\n🔍 Checking MSG91 Configuration:")
print(f"   Auth Key: {config.MSG91_AUTH_KEY}")
print(f"   Domain: {config.MSG91_DOMAIN}")
print(f"   Sender Email: {config.MSG91_SENDER_EMAIL}")
print(f"   Sender Name: {config.MSG91_SENDER_NAME}")
print(f"   Base URL: {msg91.base_url}")

print("\n📋 Template IDs:")
print(f"   OTP Template: {config.MSG91_TEMPLATE_ID}")
print(f"   Reset Template: {config.MSG91_RESET_TEMPLATE_ID}")
print(f"   Welcome Template: {config.MSG91_WELCOME_TEMPLATE_ID}")
print(f"   Order Template: {config.MSG91_ORDER_TEMPLATE_ID}")

print("\n" + "=" * 80)
print("TESTING WITH DETAILED PAYLOAD")
print("=" * 80)

test_email = "paradkartanvii@gmail.com"
test_name = "Bharath"
test_pin = "123456"

# Test with detailed logging
print(f"\n📧 Sending test email to: {test_email}")

payload = {
    "recipients": [
        {
            "to": [
                {
                    "name": test_name,
                    "email": test_email
                }
            ],
            "variables": {
                "OTP": test_pin,
                "PIN": test_pin,
                "NAME": test_name,
                "name": test_name
            }
        }
    ],
    "from": {
        "email": msg91.sender_email,
        "name": msg91.sender_name
    },
    "domain": msg91.domain,
    "template_id": config.MSG91_TEMPLATE_ID
}

headers = {
    "authkey": msg91.auth_key,
    "Content-Type": "application/json"
}

print("\n📤 Request Payload:")
import json
print(json.dumps(payload, indent=2))

print("\n📤 Request Headers:")
print(f"   authkey: {msg91.auth_key[:10]}...{msg91.auth_key[-5:]}")
print(f"   Content-Type: application/json")

try:
    response = requests.post(msg91.base_url, json=payload, headers=headers)
    print(f"\n📥 Response Status: {response.status_code}")
    print(f"📥 Response Body:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code != 200:
        print("\n❌ ERROR: Non-200 status code")
        print(f"   This might indicate authentication or configuration issues")
    else:
        print("\n✅ Email queued successfully")
        print("\n⚠️  IMPORTANT CHECKS:")
        print("   1. Verify the domain 'email.multifolks.com' is verified in MSG91")
        print("   2. Check if sender email 'support@multifolks.com' is verified")
        print("   3. Verify template IDs exist in MSG91 dashboard")
        print("   4. Check MSG91 dashboard for delivery status")
        print("   5. Check spam folder in email inbox")
        
except Exception as e:
    print(f"\n❌ Exception: {e}")

print("\n" + "=" * 80)
print("POSSIBLE ISSUES:")
print("=" * 80)
print("1. Domain not verified: 'email.multifolks.com' must be verified in MSG91")
print("2. Sender email not verified: 'support@multifolks.com' must be verified")
print("3. Template doesn't exist: Template IDs must match MSG91 dashboard")
print("4. Auth key invalid: Check if auth key is correct")
print("5. Email in spam: Check spam/junk folder")
print("6. Delivery delay: MSG91 may take a few minutes to deliver")
print("\n" + "=" * 80)
