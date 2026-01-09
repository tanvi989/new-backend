import requests
import json

print("=" * 80)
print("VERIFYING MSG91 CREDENTIALS AND TEMPLATES")
print("=" * 80)

auth_key = "482085AD1VnJzkrUX6937ff86P1"
templates = [
    "welcome_emailer",
    "forgot_password_46592",
    "request_for_otp",
    "order_placed_23"
]

print(f"\n🔑 Auth Key: {auth_key}")
print(f"\n📋 Templates to verify:")
for t in templates:
    print(f"   - {t}")

# Test each template
print("\n" + "=" * 80)
print("TESTING EACH TEMPLATE")
print("=" * 80)

test_email = "bharath@softreey.com"
base_url = "https://control.msg91.com/api/v5/email/send"

for template_id in templates:
    print(f"\n📧 Testing template: {template_id}")
    print("-" * 60)
    
    payload = {
        "recipients": [{
            "to": [{
                "name": "Bharath",
                "email": test_email
            }],
            "variables": {
                "name": "Bharath",
                "NAME": "Bharath",
                "OTP": "123456",
                "PIN": "123456",
                "order_id": "TEST-001",
                "ORDER_ID": "TEST-001",
                "order_total": "£99.99",
                "ORDER_TOTAL": "£99.99"
            }
        }],
        "from": {
            "email": "support@multifolks.com",
            "name": "Multifolks"
        },
        "domain": "email.multifolks.com",
        "template_id": template_id
    }
    
    headers = {
        "authkey": auth_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(base_url, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
        
        if response.status_code == 200:
            if response_data.get('status') == 'success':
                print(f"✅ Template '{template_id}' works!")
                unique_id = response_data.get('data', {}).get('unique_id', 'N/A')
                print(f"   Unique ID: {unique_id}")
            else:
                print(f"⚠️  Template queued but check for errors")
        else:
            print(f"❌ Failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("CHECKING MSG91 ACCOUNT STATUS")
print("=" * 80)

# Try to get account info (if API supports it)
print("\n💡 To check why emails aren't arriving:")
print("   1. Log into: https://control.msg91.com/")
print("   2. Go to: Email → Reports")
print("   3. Search for: bharath@softreey.com")
print("   4. Check delivery status and error messages")
print("\n   Common issues:")
print("   - Domain 'email.multifolks.com' not verified")
print("   - Sender 'support@multifolks.com' not verified")
print("   - Templates exist but have different variable names")
print("   - Account in test mode (only sends to verified emails)")

print("\n" + "=" * 80)
