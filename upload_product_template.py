#!/usr/bin/env python3
"""
Simple template script to upload a new product to MongoDB.
Just edit the product_data dictionary below with your product information and run!
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables (if using .env file)
load_dotenv()

# Configuration - Update these if needed
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DATABASE_NAME', 'multifolks')
COLLECTION_NAME = "products"

# ============================================
# YOUR PRODUCT DATA - EDIT THIS SECTION
# ============================================
product_data = {
    # REQUIRED FIELDS
    "skuid": "YOUR_SKU_ID_HERE",  # ⚠️ CHANGE THIS: Unique product SKU (e.g., "PROD001")
    "name": "Your Product Name",  # ⚠️ CHANGE THIS: Product display name
    "price": 0.0,  # ⚠️ CHANGE THIS: Product price (e.g., 99.99)
    
    # RECOMMENDED FIELDS
    "naming_system": "YOUR_SKU_ID_HERE",  # Usually same as skuid
    "image": "https://example.com/image.jpg",  # Main product image URL
    "images": [  # Array of all product images
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
    ],
    "brand": "Your Brand Name",
    "description": "Product description here",
    
    # OPTIONAL FIELDS
    "list_price": None,  # Original/list price (for showing discounts)
    "colors": [],  # Color codes (e.g., ["#000000", "#FFFFFF"])
    "color_names": [],  # Color names (e.g., ["Black", "White"])
    "framecolor": "",  # Frame color (e.g., "Black", "Brown")
    "style": "",  # Frame style: "Full Frame", "Half Frame", "Rimless"
    "gender": "",  # Target gender: "Men", "Women", "Unisex", "Kids"
    "size": "",  # Product size (e.g., "Small", "Medium", "Large")
    "material": "",  # Frame material (e.g., "Acetate", "Metal", "Plastic")
    "shape": "",  # Frame shape (e.g., "Round", "Square", "Aviator")
    "features": [],  # Product features (e.g., ["UV Protection", "Lightweight"])
    "variants": [],  # Product variants (if any)
    "sizes": [],  # Available sizes (e.g., ["S", "M", "L"])
    "primary_category": "",  # Primary category (e.g., "Eyeglasses")
    "secondary_category": "",  # Secondary category (e.g., "Sunglasses")
    "comfort": [],  # Comfort features (e.g., ["Lightweight", "Flexible"])
    "is_active": True  # Set to False to hide product
}

# ============================================
# SCRIPT EXECUTION - NO NEED TO EDIT BELOW
# ============================================

def main():
    try:
        print("=" * 60)
        print("📦 PRODUCT UPLOAD SCRIPT")
        print("=" * 60)
        print(f"\nConnecting to MongoDB...")
        print(f"  URI: {MONGO_URI}")
        print(f"  Database: {DB_NAME}")
        print(f"  Collection: {COLLECTION_NAME}")
        
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        print(f"\n✅ Connected to MongoDB!")
        print(f"\n📝 Product Information:")
        print(f"  SKU: {product_data['skuid']}")
        print(f"  Name: {product_data['name']}")
        print(f"  Price: ${product_data['price']}")
        
        # Validate required fields
        if not product_data.get('skuid') or product_data['skuid'] == "YOUR_SKU_ID_HERE":
            print("\n❌ ERROR: Please set a valid 'skuid' in product_data")
            return 1
        
        if not product_data.get('name') or product_data['name'] == "Your Product Name":
            print("\n❌ ERROR: Please set a valid 'name' in product_data")
            return 1
        
        if product_data.get('price', 0) == 0:
            print("\n⚠️  WARNING: Price is set to 0. Is this correct?")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return 1
        
        # Clean up None values
        cleaned_data = {k: v for k, v in product_data.items() if v is not None and v != ""}
        
        # Set naming_system if not provided
        if 'naming_system' not in cleaned_data or not cleaned_data['naming_system']:
            cleaned_data['naming_system'] = cleaned_data['skuid']
        
        print(f"\n🔄 Uploading product...")
        
        # Upsert product (create if doesn't exist, update if exists)
        result = collection.update_one(
            {"skuid": product_data["skuid"]},
            {"$set": cleaned_data},
            upsert=True
        )
        
        # Get the created/updated product
        created_product = collection.find_one({"skuid": product_data["skuid"]})
        
        if result.upserted_id:
            print(f"\n✅ SUCCESS: Created new product!")
            print(f"  Product ID: {result.upserted_id}")
        elif result.modified_count > 0:
            print(f"\n✅ SUCCESS: Updated existing product!")
            print(f"  Modified fields: {result.modified_count}")
        else:
            print(f"\n✅ SUCCESS: Product already exists with same data")
        
        # Display product summary
        if created_product:
            print(f"\n📋 Product Summary:")
            print(f"  SKU: {created_product.get('skuid')}")
            print(f"  Name: {created_product.get('name')}")
            print(f"  Price: ${created_product.get('price', 0)}")
            print(f"  Brand: {created_product.get('brand', 'N/A')}")
            print(f"  Images: {len(created_product.get('images', []))} image(s)")
            print(f"  Active: {created_product.get('is_active', True)}")
        
        print(f"\n{'=' * 60}")
        print("✅ PRODUCT UPLOAD COMPLETE!")
        print(f"{'=' * 60}\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if 'client' in locals():
            client.close()
            print("🔌 Database connection closed")

if __name__ == "__main__":
    exit(main())

