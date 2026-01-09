import requests
import pymongo
import time
import config

# Connect to DB to check state
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.DATABASE_NAME]
users_col = db[config.COLLECTION_NAME]

email = "vacanzidev@gmail.com" # User from screenshot

print(f"Checking user {email} before request...")
user = users_col.find_one({"email": email})
if user:
    print(f"User found. reset_pin: {user.get('reset_pin')}, expiry: {user.get('reset_pin_expiry')}")
else:
    print("User NOT found!")

# Trigger Forgot Password
url = "http://localhost:5000/api/v1/auth/forgot-password"
print(f"\nRequesting PIN from {url}...")
try:
    resp = requests.post(url, json={"email": email, "type": "reset"})
    print(f"Response: {resp.status_code} - {resp.text}")
except Exception as e:
    print(f"Request failed: {e}")

time.sleep(2)

print(f"\nChecking user {email} AFTER request...")
user = users_col.find_one({"email": email})
if user:
    print(f"User found. reset_pin: {user.get('reset_pin')}, expiry: {user.get('reset_pin_expiry')}")
else:
    print("User NOT found!")
