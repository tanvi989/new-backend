#!/usr/bin/env python3
"""
Test script specifically for order_placed_23 MSG91 template
"""
import config
from notification_service import MSG91Service

print("=" * 80)
print("TESTING ORDER CONFIRMATION EMAIL TEMPLATE")
print("=" * 80)

# Initialize MSG91 Service
msg91 = MSG91Service()

# Test data
test_email = "paradkartanvii@gmail.com"
test_name = "Bharath Kumar"
test_order_id = "MF-2025-001"
test_total = "£149.99"

print(f"\nRecipient: {test_email}")
print(f"Customer Name: {test_name}")
print(f"Order ID: {test_order_id}")
print(f"Order Total: {test_total}")
print(f"\nTemplate ID: {config.MSG91_ORDER_TEMPLATE_ID}")
print(f"Sender: {msg91.sender_email}")
print(f"Domain: {msg91.domain}")

print("\n" + "=" * 80)
print("SENDING ORDER CONFIRMATION EMAIL...")
print("=" * 80)

result = msg91.send_order_confirmation(
    email=test_email,
    order_id=test_order_id,
    order_total=test_total,
    name=test_name
)

print("\nRESULT:")
print("-" * 80)
print(f"Success: {result.get('success')}")

if result.get('success'):
    print("Email sent successfully!")
    data = result.get('data', {})
    print(f"\nResponse Details:")
    print(f"   Status: {data.get('status', 'N/A')}")
    print(f"   Message: {data.get('message', 'N/A')}")
    if 'data' in data:
        print(f"   Unique ID: {data['data'].get('unique_id', 'N/A')}")
else:
    print("Email failed to send")
    print(f"   Error: {result.get('msg', 'Unknown error')}")

print("\n" + "=" * 80)
print("VARIABLES SENT TO TEMPLATE:")
print("=" * 80)
print(f"   NAME: {test_name}")
print(f"   name: {test_name}")
print(f"   order_id: {test_order_id}")
print(f"   ORDER_ID: {test_order_id}")
print(f"   email: {test_email}")
print(f"   order_total: {test_total}")
print(f"   ORDER_TOTAL: {test_total}")

print("\n" + "=" * 80)
print("Test complete! Check inbox: " + test_email)
print("=" * 80)
