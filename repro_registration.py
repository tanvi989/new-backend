import requests
import json
import time

url = "http://localhost:5000/api/v1/auth/simple-register"
headers = {
    "Content-Type": "application/json"
}

# Generate a random email to avoid duplicate user error
timestamp = int(time.time())
email = f"test_user_{timestamp}@example.com"
mobile = f"071234{str(timestamp)[-5:]}" # Mock UK mobile

payload = {
    "first_name": "Test",
    "last_name": "",
    "email": email,
    "mobile": mobile,
    "password": "password123",
    "country_code": "44"
}

print(f"Sending request to {url} with payload:")
print(json.dumps(payload, indent=2))

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"\nResponse Status: {response.status_code}")
    print("Response Body:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Request failed: {e}")
