import pymongo
import sys
sys.path.append('/home/selfeey-india/Documents/AI_Projects/login_api')
import config
from notification_service import MSG91Service

# Connect to MongoDB
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.DATABASE_NAME]

print("=" * 80)
print("TESTING MSG91 EMAIL INTEGRATION")
print("=" * 80)

# Initialize MSG91 Service
msg91 = MSG91Service()

print("\n📧 MSG91 Configuration:")
print(f"   Auth Key: {msg91.auth_key}")
print(f"   Domain: {msg91.domain}")
print(f"   Sender Email: {msg91.sender_email}")
print(f"   Sender Name: {msg91.sender_name}")
print(f"   Base URL: {msg91.base_url}")

print("\n📝 Template IDs:")
print(f"   OTP Template: {config.MSG91_TEMPLATE_ID}")
print(f"   Reset Template: {config.MSG91_RESET_TEMPLATE_ID}")
print(f"   Welcome Template: {config.MSG91_WELCOME_TEMPLATE_ID}")
print(f"   Order Template: {config.MSG91_ORDER_TEMPLATE_ID}")

print("\n" + "=" * 80)
print("CHECKING EMAIL USAGE IN APP.PY")
print("=" * 80)

# Check recent users who might have received emails
users = list(db['accounts_login'].find().limit(5))
print(f"\n👥 Sample Users in Database: {len(users)}")
for user in users:
    print(f"   - Email: {user.get('email', 'N/A')}")
    print(f"     Name: {user.get('first_name', 'N/A')} {user.get('last_name', '')}")
    print(f"     Created: {user.get('created_at', 'N/A')}")
    print()

print("\n" + "=" * 80)
print("CHECKING ORDERS FOR EMAIL NOTIFICATIONS")
print("=" * 80)

orders = list(db['orders'].find().limit(3))
print(f"\n📦 Sample Orders: {len(orders)}")
for order in orders:
    print(f"   - Order ID: {order.get('_id')}")
    print(f"     Email: {order.get('email', 'N/A')}")
    print(f"     Status: {order.get('status', 'N/A')}")
    print(f"     Created: {order.get('created_at', 'N/A')}")
    print()

print("\n" + "=" * 80)
print("⚠️  ISSUES FOUND")
print("=" * 80)
print("\n1. Sender Email Typo:")
print(f"   Current: {msg91.sender_email}")
print(f"   Should be: support@multifolks.com")

print("\n2. No user name personalization in email templates")
print("   Currently hardcoded as 'User'")

print("\n" + "=" * 80)

client.close()
