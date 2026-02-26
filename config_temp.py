import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from this file's directory (newbackend) so DB is correct even when run from elsewhere
_script_dir = Path(__file__).resolve().parent
load_dotenv(_script_dir / ".env")
load_dotenv()

# MongoDB Configuration - same DB for users (accounts_login) and cart (collection "cart")
MONGO_URI = (os.getenv("MONGO_URI") or "").strip() or "mongodb+srv://gaMultilens:gaMultilens@cluster0.mongodb.net/"
DATABASE_NAME = os.getenv("DATABASE_NAME", "gaMultilens")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "accounts_login")

# SKU frame/lens measurements (collection name; optional in .env)
SKU_MEASUREMENTS_COLLECTION = os.getenv("SKU_MEASUREMENTS_COLLECTION", "sku_measurements")

# JWT Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Server Configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Stripe Configuration
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

# Payment Configuration
CURRENCY = os.getenv('CURRENCY', 'gbp')  # UK currency
PAYMENT_SUCCESS_URL = os.getenv('PAYMENT_SUCCESS_URL', 'https://mvp.multifolks.com/thank-you')
PAYMENT_CANCEL_URL = os.getenv('PAYMENT_CANCEL_URL', 'https://mvp.multifolks.com/payment/cancel')

# BlueDart Delivery Configuration
BLUEDART_BASE_URL = os.getenv('BLUEDART_BASE_URL', 'https://netconnect.bluedart.com/Ver1.10/')
BLUEDART_CUSTOMER_CODE = os.getenv('BLUEDART_CUSTOMER_CODE', '940553')
BLUEDART_LOGIN_ID = os.getenv('BLUEDART_LOGIN_ID', 'GG940553')
BLUEDART_LICENSE_KEY = os.getenv('BLUEDART_LICENSE_KEY', '0bcbd949df368625eb964bb846041db1')

# Warehouse Configuration
WAREHOUSE_PINCODE = os.getenv('WAREHOUSE_PINCODE', '122001')
WAREHOUSE_ADDRESS = {
    'line1': os.getenv('WAREHOUSE_ADDRESS_LINE1', 'Plot A-8, Infocity 1'),
    'line2': os.getenv('WAREHOUSE_ADDRESS_LINE2', 'Sector 34'),
    'line3': os.getenv('WAREHOUSE_ADDRESS_LINE3', 'Gurgaon, Haryana 122002'),
    'phone': os.getenv('WAREHOUSE_PHONE', '0124-6101010')
}

# MSG91 Configuration
MSG91_AUTH_KEY = os.getenv('MSG91_AUTH_KEY', '482085AD1VnJzkrUX6937ff86P1')
MSG91_DOMAIN = os.getenv('MSG91_DOMAIN', 'email.multifolks.com')
MSG91_TEMPLATE_ID = os.getenv('MSG91_TEMPLATE_ID', 'request_otp_new')
MSG91_RESET_TEMPLATE_ID = os.getenv('MSG91_RESET_TEMPLATE_ID', 'request_otp_new')
MSG91_WELCOME_TEMPLATE_ID = os.getenv('MSG91_WELCOME_TEMPLATE_ID', 'welcome_emailer_new')
MSG91_ORDER_TEMPLATE_ID = os.getenv('MSG91_ORDER_TEMPLATE_ID', 'order_placed_v1_3')
MSG91_SENDER_EMAIL = os.getenv('MSG91_SENDER_EMAIL', 'support@multifolks.com')
MSG91_SENDER_NAME = os.getenv('MSG91_SENDER_NAME', 'Multifolks')

# SMTP for contact form notifications (e.g. Gmail: smtp.gmail.com, port 587, use App Password)
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_EMAIL = os.getenv('SMTP_EMAIL', '')           # Your email (e.g. yourname@gmail.com)
SMTP_APP_PASSWORD = os.getenv('SMTP_APP_PASSWORD', '')  # App password (not regular password)
CONTACT_FORM_TO_EMAIL = os.getenv('CONTACT_FORM_TO_EMAIL', '')  # Where to receive contact form submissions (can be same as SMTP_EMAIL)