import sys
sys.path.append('/home/selfeey-india/Documents/AI_Projects/login_api')
import config
from notification_service import MSG91Service

print("=" * 80)
print("TESTING MSG91 EMAIL INTEGRATION")
print("=" * 80)

# Initialize MSG91 Service
msg91 = MSG91Service()

test_email = "bharath@softreey.com"
test_name = "Bharath"

print(f"\n📧 Test Email: {test_email}")
print(f"👤 Test Name: {test_name}")
print(f"\n🔧 MSG91 Configuration:")
print(f"   Domain: {msg91.domain}")
print(f"   Sender: {msg91.sender_email}")
print(f"   Auth Key: {msg91.auth_key[:10]}...")

print("\n" + "=" * 80)
print("TEST 1: WELCOME EMAIL")
print("=" * 80)

result = msg91.send_welcome_email(test_email, test_name)
print(f"Result: {result}")

print("\n" + "=" * 80)
print("TEST 2: LOGIN PIN EMAIL")
print("=" * 80)

test_pin = "123456"
result = msg91.send_login_pin(test_email, test_pin, test_name)
print(f"Result: {result}")

print("\n" + "=" * 80)
print("TEST 3: PASSWORD RESET PIN EMAIL")
print("=" * 80)

result = msg91.send_password_reset_pin(test_email, test_pin, test_name)
print(f"Result: {result}")

print("\n" + "=" * 80)
print("TEST 4: ORDER CONFIRMATION EMAIL")
print("=" * 80)

test_order_id = "ORD-TEST-001"
test_total = "£99.99"
result = msg91.send_order_confirmation(test_email, test_order_id, test_total, test_name)
print(f"Result: {result}")

print("\n" + "=" * 80)
print("TESTING COMPLETE")
print("=" * 80)
print("\n✅ Check the email inbox for: " + test_email)
print("📧 Expected emails:")
print("   1. Welcome email")
print("   2. Login PIN email (PIN: 123456)")
print("   3. Password reset PIN email (PIN: 123456)")
print("   4. Order confirmation email (Order: ORD-TEST-001, Total: £99.99)")
print("\n" + "=" * 80)
