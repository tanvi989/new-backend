#!/usr/bin/env python3
import requests
import json

print("=" * 80)
print("TESTING REGISTRATION WITH ENHANCED LOGGING")
print("=" * 80)

# Test registration
url = "http://localhost:5000/api/v1/auth/simple-register"

payload = {
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser999@example.com",
    "mobile": "07987654321",
    "password": "Test123!",
    "country_code": "44",
    "is_subscribed_whatsapp": True
}

print(f"\n📝 Registering new user:")
print(f"   Email: {payload['email']}")
print(f"   Name: {payload['first_name']} {payload['last_name']}")
print(f"   Mobile: {payload['mobile']}")

try:
    response = requests.post(url, json=payload)
    print(f"\n📥 Response Status: {response.status_code}")
    print(f"📥 Response Body:")
    print(json.dumps(response.json(), indent=2))
    
    print(f"\n{'='*80}")
    print("✅ Check backend.log for detailed MSG91 logging")
    print("Run: tail -f /home/selfeey-india/Documents/AI_Projects/login_api/backend.log")
    print(f"{'='*80}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
