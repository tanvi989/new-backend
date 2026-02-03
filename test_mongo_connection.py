"""Run this to see the exact MongoDB Atlas connection error: python test_mongo_connection.py"""
import os
import sys

# Same as app - load .env from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

MONGO_URI = os.getenv("MONGO_URI", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "gaMultilens")

if not MONGO_URI:
    print("ERROR: MONGO_URI is empty. Check your .env file.")
    sys.exit(1)

# Mask password in print
_display_uri = MONGO_URI
if "@" in _display_uri:
    parts = _display_uri.split("@")
    _display_uri = parts[0].split(":")[0] + ":****@" + parts[1]
print("Using MONGO_URI:", _display_uri)
print("Connecting...")

try:
    from pymongo import MongoClient
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )
    client.server_info()
    db = client[DATABASE_NAME]
    print("SUCCESS: Connected to Atlas. Database:", DATABASE_NAME)
except Exception as e:
    print("FAILED:", type(e).__name__, "-", str(e))
    if "IP" in str(e) or "whitelist" in str(e).lower() or "10061" in str(e):
        print("\n--> Add your IP in Atlas: Network Access -> Add IP Address (or 0.0.0.0/0 for testing)")
    elif "auth" in str(e).lower() or "Authentication" in str(e):
        print("\n--> Check username/password in MONGO_URI. URL-encode special chars in password.")
    sys.exit(1)
