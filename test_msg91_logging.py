#!/usr/bin/env python3
import sys
sys.path.append('/home/selfeey-india/Documents/AI_Projects/login_api')

from notification_service import MSG91Service

print("=" * 80)
print("TESTING MSG91 WITH ENHANCED LOGGING")
print("=" * 80)

# Initialize service
msg91 = MSG91Service()

test_email = "bharat.n@softreey.com"
test_name = "Bharath"
test_pin = "654321"

print("\n" + "=" * 80)
print("TEST 1: LOGIN PIN EMAIL")
print("=" * 80)
result = msg91.send_login_pin(test_email, test_pin, test_name)
print(f"\nResult: {result}")

print("\n" + "=" * 80)
print("TEST 2: WELCOME EMAIL")
print("=" * 80)
result = msg91.send_welcome_email(test_email, test_name)
print(f"\nResult: {result}")

print("\n" + "=" * 80)
print("TESTS COMPLETE")
print("=" * 80)
print(f"\n✅ Check logs above for detailed MSG91 tracking")
print(f"📧 Check email inbox: {test_email}")
print("\n" + "=" * 80)
