# Quick Test: Create a test order manually to verify the thank you page works

import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['gaMultilens']

# Create a test order
test_order = {
    "order_id": "TEST-ORDER-12345",
    "user_id": "test_user",
    "user_email": "test@example.com",
    "user_name": "Test User",
    "items": [{
        "product_id": "TEST-PRODUCT",
        "name": "Test Glasses",
        "price": 100,
        "quantity": 1
    }],
    "subtotal": 100,
    "shipping_cost": 5,
    "discount": 0,
    "total": 105,
    "payment_status": "paid",
    "payment_method": "stripe",
    "payment_intent_id": "pi_test123",
    "order_status": "pending",
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

result = db.orders.insert_one(test_order)
print(f"Test order created with ID: {result.inserted_id}")
print(f"Order ID: TEST-ORDER-12345")
print("\nNow test: http://localhost:3000/thank-you?order_id=TEST-ORDER-12345")
