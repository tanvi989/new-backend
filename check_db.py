#!/usr/bin/env python3
import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MongoDB
mongo_uri = os.getenv('MONGO_URI', 'mongodb+srv://gaMultilens:gaMultilens@cluster0.mongodb.net/')
client = MongoClient(mongo_uri)
db = client['gaMultilens']

# Check orders collection
print("=== ORDERS IN DATABASE ===")
orders = list(db.orders.find().limit(10))
print(f"Total orders: {db.orders.count_documents({})}")
print("\nRecent orders:")
for order in orders:
    print(f"  - Order ID: {order.get('order_id')}, Status: {order.get('payment_status')}, Total: {order.get('total')}")

# Check payments collection
print("\n=== PAYMENTS IN DATABASE ===")
payments = list(db.payments.find().limit(10))
print(f"Total payments: {db.payments.count_documents({})}")
print("\nRecent payments:")
for payment in payments:
    print(f"  - Order ID: {payment.get('order_id')}, Status: {payment.get('status')}, Amount: {payment.get('amount')}")
