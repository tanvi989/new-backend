#!/usr/bin/env python3
"""
Test script to simulate a Stripe webhook for testing order creation
"""
import requests
import json

# Simulate a checkout.session.completed event
webhook_data = {
    "type": "checkout.session.completed",
    "data": {
        "object": {
            "id": "cs_test_123",
            "payment_status": "paid",
            "amount_total": 10500,  # £105.00 in pence
            "currency": "gbp",
            "payment_intent": "pi_test_123",
            "metadata": {
                "order_id": "ORD-TEST-WEBHOOK",
                "user_id": "test_user_123",
                "customer_id": "test_customer"
            }
        }
    }
}

# Note: This won't work without proper Stripe signature
# But we can test the endpoint directly
print("Testing webhook endpoint...")
print(f"Payload: {json.dumps(webhook_data, indent=2)}")

# For testing, you would need to:
# 1. Use Stripe CLI: stripe trigger checkout.session.completed
# 2. Or complete an actual test payment
print("\nTo test properly:")
print("1. Complete a test payment with card 4242 4242 4242 4242")
print("2. Check backend logs for webhook activity")
print("3. Run: python3 check_db.py to verify order creation")
