import requests
import json

# Test the merge-guest-cart endpoint
url = "https://mvp.multifolks.com/http://localhost:5000/api/v1/cart/merge-guest-cart"

# You'll need to replace this with a real token from your browser's localStorage
token = "YOUR_TOKEN_HERE"  # Get from localStorage.getItem('token')
guest_id = "guest_test123"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

data = {
    "guest_id": guest_id
}

print(f"Testing endpoint: {url}")
print(f"Headers: {headers}")
print(f"Data: {data}")
print("-" * 50)

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
