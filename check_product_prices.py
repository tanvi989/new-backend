from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://doadmin:4k859D3p17t6InoB@db-mongodb-blr1-66755-1215b072.mongo.ondigitalocean.com/admin?tls=true&authSource=admin")
DATABASE_NAME = os.getenv("DATABASE_NAME", "multifolks")

try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    products = db.products.find_one()
    
    if products:
        print(f"Product ID: {products.get('_id')}")
        print(f"Name: {products.get('name')}")
        print(f"Price: {products.get('price')}")
        print(f"List Price: {products.get('list_price')}")
        print(f"Selling Price: {products.get('selling_price')}")
        print(f"Full Document Keys: {list(products.keys())}")
    else:
        print("No products found")

except Exception as e:
    print(f"Error: {e}")
