#!/usr/bin/env python3
"""Verify MongoDB connection and collections used by the backend (accounts_login, cart, etc.)."""
import os
import sys
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env from script directory (same as backend)
_script_dir = Path(__file__).resolve().parent
load_dotenv(_script_dir / ".env")
load_dotenv()

mongo_uri = os.getenv("MONGO_URI", "").strip() or "mongodb+srv://gaMultilens:gaMultilens@cluster0.mongodb.net/"
db_name = os.getenv("DATABASE_NAME", "gaMultilens")

print("=== MongoDB connection ===")
print(f"  URI host: {mongo_uri.split('@')[-1].split('/')[0] if '@' in mongo_uri else '(check MONGO_URI)'}")
print(f"  Database: {db_name}")
print()

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.server_info()
    print("  Status: CONNECTED")
except Exception as e:
    print(f"  Status: FAILED - {e}")
    sys.exit(1)

db = client[db_name]

# Collections used by backend
print("\n=== Collections in", db_name, "===")
for c in ["accounts_login", "cart", "products", "orders"]:
    try:
        n = db[c].count_documents({})
        print(f"  {c}: {n} documents")
    except Exception as e:
        print(f"  {c}: error - {e}")

# Cart summary (cart is where /api/v1/cart reads from)
print("\n=== Cart collection (used by /cart page) ===")
cart_docs = list(db.cart.find().limit(5))
print(f"  Total cart documents (one per user/guest): {db.cart.count_documents({})}")
for doc in cart_docs:
    items = doc.get("items", [])
    print(f"  - user_id: {doc.get('user_id')}, items: {len(items)}")
print("\nIf cart is 0 and /cart fails, add an item first; backend creates the collection on first add.")
