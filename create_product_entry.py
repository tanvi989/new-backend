#!/usr/bin/env python3
"""
Script to create/update product entry in MongoDB for E10A8615
"""

from pymongo import MongoClient

# Configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "multifolks"
COLLECTION_NAME = "products"

# Product data
product_data = {
    "skuid": "E10A8615",
    "naming_system": "E10A8615",
    "name": "E10A8615",
    "images": [
        "https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E10A8615/E10A8615_1.png",
        "https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E10A8615/E10A8615_2.png",
        "https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E10A8615/E10A8615_3.png",
        "https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E10A8615/E10A8615_4.png",
        "https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E10A8615/E10A8615_5.png",
        "https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E10A8615/E10A8615_6.png"
    ],
    "image": "https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E10A8615/E10A8615_1.png",
    "price": 0,  # Update with actual price
    "description": "",
    "features": [],
    "colors": [],
    "color_names": [],
    "variants": [],
    "sizes": [],
    "brand": "",
    "gender": "",
    "material": "",
    "shape": "",
    "style": ""
}

def main():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        print("=" * 60)
        print("Creating/Updating Product Entry for E10A8615")
        print("=" * 60)
        
        # Try to update existing product or insert new one
        result = collection.update_one(
            {"skuid": "E10A8615"},
            {"$set": product_data},
            upsert=True
        )
        
        if result.upserted_id:
            print(f"\n✓ Created new product entry")
            print(f"  Product ID: {result.upserted_id}")
        elif result.modified_count > 0:
            print(f"\n✓ Updated existing product")
            print(f"  Modified: {result.modified_count} document(s)")
        else:
            print(f"\n✓ Product already exists with same data")
        
        # Verify the product
        product = collection.find_one({"skuid": "E10A8615"})
        if product:
            print(f"\n✓ Product verified in database:")
            print(f"  SKU: {product.get('skuid')}")
            print(f"  Name: {product.get('naming_system')}")
            print(f"  Images: {len(product.get('images', []))} images")
            print(f"\nImage URLs:")
            for i, url in enumerate(product.get('images', []), 1):
                print(f"  {i}. {url}")
        
        print(f"\n{'=' * 60}")
        print("✓ SUCCESS: Product entry created/updated in database!")
        print(f"{'=' * 60}\n")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return 1
    finally:
        client.close()
    
    return 0

if __name__ == "__main__":
    exit(main())
