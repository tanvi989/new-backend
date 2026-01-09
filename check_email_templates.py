import pymongo
import sys
sys.path.append('/home/selfeey-india/Documents/AI_Projects/login_api')
import config

# Connect to MongoDB
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.DATABASE_NAME]

print("=" * 80)
print("CHECKING FOR EMAIL TEMPLATES IN DATABASE")
print("=" * 80)

# Check all collections for email-related data
collections = db.list_collection_names()

# Look for email template collections
email_related = [c for c in collections if 'email' in c.lower() or 'template' in c.lower() or 'msg' in c.lower()]

if email_related:
    print(f"\n📧 Email-related collections found:")
    for coll_name in email_related:
        count = db[coll_name].count_documents({})
        print(f"   - {coll_name} ({count} documents)")
        
        # Show sample document
        sample = db[coll_name].find_one()
        if sample:
            print(f"     Sample document:")
            for key, value in sample.items():
                if isinstance(value, str) and len(value) > 100:
                    print(f"       {key}: {value[:100]}...")
                else:
                    print(f"       {key}: {value}")
else:
    print("\n❌ No email-related collections found")

# Check for pigeon email templates
print("\n" + "=" * 80)
print("CHECKING PIGEON EMAIL TEMPLATES")
print("=" * 80)

pigeon_collections = [c for c in collections if 'pigeon' in c.lower()]
if pigeon_collections:
    print(f"\n📧 Pigeon collections found:")
    for coll_name in pigeon_collections:
        count = db[coll_name].count_documents({})
        print(f"   - {coll_name} ({count} documents)")
        
        # Show all documents
        docs = list(db[coll_name].find())
        for i, doc in enumerate(docs, 1):
            print(f"\n   Document {i}:")
            for key, value in doc.items():
                if isinstance(value, str) and len(value) > 200:
                    print(f"     {key}: {value[:200]}...")
                else:
                    print(f"     {key}: {value}")
else:
    print("\n❌ No pigeon collections found")

# Check for MSG91 configuration in any collection
print("\n" + "=" * 80)
print("CHECKING MSG91 CONFIGURATION")
print("=" * 80)

print(f"\nMSG91 Config from config.py:")
print(f"  AUTH_KEY: {config.MSG91_AUTH_KEY}")
print(f"  DOMAIN: {config.MSG91_DOMAIN}")
print(f"  TEMPLATE_ID: {config.MSG91_TEMPLATE_ID}")
print(f"  RESET_TEMPLATE_ID: {config.MSG91_RESET_TEMPLATE_ID}")
print(f"  WELCOME_TEMPLATE_ID: {config.MSG91_WELCOME_TEMPLATE_ID}")
print(f"  ORDER_TEMPLATE_ID: {config.MSG91_ORDER_TEMPLATE_ID}")
print(f"  SENDER_EMAIL: {config.MSG91_SENDER_EMAIL}")
print(f"  SENDER_NAME: {config.MSG91_SENDER_NAME}")

client.close()
print("\n" + "=" * 80)
