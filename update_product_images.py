#!/usr/bin/env python3
"""
Script to upload product images to Google Cloud Storage and update MongoDB database.
Usage: python update_product_images.py <product_sku> <images_directory>
Example: python update_product_images.py EA10A8615 /home/selfeey-india/Downloads/EA10A8615
"""

import os
import sys
from google.cloud import storage
from pymongo import MongoClient
from pathlib import Path
import json

# Configuration
GCS_CREDENTIALS_PATH = "gcs-service-account.json"
BUCKET_NAME = "myapp-image-bucket-001"
GCS_BASE_PATH = "Spexmojo_images/Spexmojo_images"
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "multifolks"
COLLECTION_NAME = "products"

def upload_to_gcs(local_file_path, gcs_destination_path):
    """Upload a file to Google Cloud Storage."""
    try:
        # Initialize GCS client
        client = storage.Client.from_service_account_json(GCS_CREDENTIALS_PATH)
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(gcs_destination_path)
        
        # Upload file
        blob.upload_from_filename(local_file_path)
        
        # Note: Bucket has uniform bucket-level access, so no need to make_public()
        # The bucket itself is configured for public access
        
        # Return public URL
        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{gcs_destination_path}"
        print(f"✓ Uploaded: {local_file_path} -> {public_url}")
        return public_url
    except Exception as e:
        print(f"✗ Error uploading {local_file_path}: {str(e)}")
        return None

def update_database(sku, image_urls):
    """Update MongoDB with new image URLs."""
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Update product images
        result = collection.update_one(
            {"skuid": sku},
            {
                "$set": {
                    "images": image_urls,
                    "image": image_urls[0] if image_urls else None
                }
            }
        )
        
        if result.matched_count > 0:
            print(f"✓ Updated database for SKU: {sku}")
            print(f"  - Matched: {result.matched_count} document(s)")
            print(f"  - Modified: {result.modified_count} document(s)")
            return True
        else:
            print(f"✗ No product found with SKU: {sku}")
            return False
    except Exception as e:
        print(f"✗ Error updating database: {str(e)}")
        return False
    finally:
        client.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python update_product_images.py <product_sku> <images_directory>")
        print("Example: python update_product_images.py EA10A8615 /home/selfeey-india/Downloads/EA10A8615")
        sys.exit(1)
    
    sku = sys.argv[1]
    images_dir = sys.argv[2]
    
    # Validate inputs
    if not os.path.exists(images_dir):
        print(f"✗ Error: Directory not found: {images_dir}")
        sys.exit(1)
    
    if not os.path.exists(GCS_CREDENTIALS_PATH):
        print(f"✗ Error: GCS credentials not found: {GCS_CREDENTIALS_PATH}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"Updating images for product: {sku}")
    print(f"Source directory: {images_dir}")
    print(f"{'='*60}\n")
    
    # Get all image files from directory
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    image_files = []
    
    for file in sorted(os.listdir(images_dir)):
        file_path = os.path.join(images_dir, file)
        if os.path.isfile(file_path) and Path(file).suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    if not image_files:
        print(f"✗ No image files found in {images_dir}")
        sys.exit(1)
    
    print(f"Found {len(image_files)} image(s) to upload:\n")
    for img in image_files:
        print(f"  - {os.path.basename(img)}")
    print()
    
    # Upload images to GCS
    uploaded_urls = []
    for idx, local_file in enumerate(image_files, 1):
        filename = os.path.basename(local_file)
        extension = Path(filename).suffix
        
        # Create GCS path: Spexmojo_images/Spexmojo_images/SKU/SKU_N.ext
        gcs_filename = f"{sku}_{idx}{extension}"
        gcs_path = f"{GCS_BASE_PATH}/{sku}/{gcs_filename}"
        
        url = upload_to_gcs(local_file, gcs_path)
        if url:
            uploaded_urls.append(url)
    
    if not uploaded_urls:
        print("\n✗ No images were uploaded successfully")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"Successfully uploaded {len(uploaded_urls)} image(s)")
    print(f"{'='*60}\n")
    
    # Update database
    print("Updating database...")
    if update_database(sku, uploaded_urls):
        print(f"\n{'='*60}")
        print("✓ SUCCESS: Images uploaded and database updated!")
        print(f"{'='*60}\n")
        print("Image URLs:")
        for i, url in enumerate(uploaded_urls, 1):
            print(f"  {i}. {url}")
        print()
    else:
        print("\n✗ Failed to update database")
        sys.exit(1)

if __name__ == "__main__":
    main()
