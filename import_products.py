#!/usr/bin/env python3
"""
Import products from mapped_products.csv into MongoDB
"""
import csv
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'gaMultilens')

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
products_collection = db['products']

def import_products():
    print("Starting product import...")
    
    # Read CSV file
    csv_file = 'mapped_products.csv'
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        products = []
        
        for row in reader:
            # Create product document
            product = {
                'skuid': row.get('skuid', ''),
                'name': row.get('name', ''),
                'naming_system': row.get('naming_system', ''),
                'brand': row.get('brand', ''),
                'price': float(row.get('price', 0)) if row.get('price') else 0,
                'list_price': float(row.get('list_price', 0)) if row.get('list_price') else 0,
                'image': row.get('image', ''),
                'images': row.get('images', '').split(',') if row.get('images') else [],
                'colors': row.get('colors', '').split(',') if row.get('colors') else [],
                'color_names': row.get('color_names', '').split(',') if row.get('color_names') else [],
                'framecolor': row.get('framecolor', ''),
                'style': row.get('style', ''),
                'gender': row.get('gender', ''),
                'size': row.get('size', ''),
                'material': row.get('material', ''),
                'shape': row.get('shape', ''),
                'description': row.get('description', ''),
                'features': row.get('features', '').split('|') if row.get('features') else [],
            }
            
            # Add variants if available
            if row.get('variants'):
                try:
                    import json
                    product['variants'] = json.loads(row.get('variants', '[]'))
                except:
                    product['variants'] = []
            
            products.append(product)
            
            # Batch insert every 100 products
            if len(products) >= 100:
                products_collection.insert_many(products)
                print(f"Inserted {len(products)} products...")
                products = []
        
        # Insert remaining products
        if products:
            products_collection.insert_many(products)
            print(f"Inserted {len(products)} products...")
    
    # Get total count
    total = products_collection.count_documents({})
    print(f"\n✅ Import complete! Total products in database: {total}")
    
    # Show sample products
    print("\nSample products:")
    for p in products_collection.find().limit(5):
        print(f"  - {p.get('naming_system', p.get('name'))} ({p.get('skuid')}) - £{p.get('price')}")

if __name__ == '__main__':
    import_products()
