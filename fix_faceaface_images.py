#!/usr/bin/env python3
"""
Fix Face-a-Face Image URLs in Database

This script updates the image URLs for Face-a-Face products in MongoDB
to match the actual file naming convention in Google Cloud Storage.

Changes:
- E15A0001-1.png → E15A0001.png (first image)
- E15A0001-1_1.png → E15A0001_1.png
- E15A0001-1_2.png → E15A0001_2.png
etc.
"""

import sys
import re
from pymongo import MongoClient
import config

def fix_image_url(url, skuid):
    """
    Fix a single image URL by replacing the dash-separated naming
    with underscore-separated naming.
    
    Args:
        url: Original image URL
        skuid: Product SKU ID
        
    Returns:
        Fixed image URL
    """
    # Pattern: {SKUID}-1.png → {SKUID}.png (first image)
    # Pattern: {SKUID}-1_N.png → {SKUID}_N.png (subsequent images)
    
    # Replace {SKUID}-1.png with {SKUID}.png (first image)
    url = url.replace(f"{skuid}-1.png", f"{skuid}.png")
    
    # Replace {SKUID}-1_N.png with {SKUID}_N.png (subsequent images)
    url = re.sub(f"{skuid}-1_(\d+)\.png", f"{skuid}_\\1.png", url)
    
    return url

def main():
    print("=" * 60)
    print("Face-a-Face Image URL Fix Script")
    print("=" * 60)
    
    # Connect to MongoDB
    print(f"\nConnecting to MongoDB...")
    print(f"Database: {config.DATABASE_NAME}")
    
    client = MongoClient(config.MONGO_URI)
    db = client[config.DATABASE_NAME]
    collection = db['products']
    
    # Find all Face-a-Face products
    query = {'brand': {'$regex': 'face', '$options': 'i'}}
    faceaface_products = list(collection.find(query))
    
    print(f"\nFound {len(faceaface_products)} Face-a-Face products")
    
    if len(faceaface_products) == 0:
        print("No products to update. Exiting.")
        return
    
    # Update each product
    updated_count = 0
    error_count = 0
    
    for product in faceaface_products:
        skuid = product.get('skuid', '')
        product_id = product.get('_id')
        
        if not skuid:
            print(f"⚠️  Skipping product {product_id}: No SKUID")
            error_count += 1
            continue
        
        # Get current images
        current_images = product.get('images', [])
        current_image = product.get('image', '')
        
        if not current_images:
            print(f"⚠️  Skipping {skuid}: No images array")
            error_count += 1
            continue
        
        # Fix image URLs
        fixed_images = [fix_image_url(img, skuid) for img in current_images]
        fixed_image = fix_image_url(current_image, skuid) if current_image else ''
        
        # Fix variants array images
        current_variants = product.get('variants', [])
        fixed_variants = []
        variants_changed = False
        
        for variant in current_variants:
            fixed_variant = variant.copy()
            if 'image' in variant and variant['image']:
                fixed_variant_image = fix_image_url(variant['image'], skuid)
                if fixed_variant_image != variant['image']:
                    variants_changed = True
                fixed_variant['image'] = fixed_variant_image
            fixed_variants.append(fixed_variant)
        
        # Check if anything changed
        if fixed_images == current_images and fixed_image == current_image and not variants_changed:
            print(f"✓ {skuid}: Already correct")
            continue
        
        # Update database
        try:
            update_data = {
                'images': fixed_images,
                'image': fixed_image
            }
            
            # Only update variants if they exist and changed
            if current_variants and variants_changed:
                update_data['variants'] = fixed_variants
            
            result = collection.update_one(
                {'_id': product_id},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                print(f"✅ {skuid}: Updated {len(fixed_images)} images" + (" + variants" if variants_changed else ""))
                print(f"   Old: {current_images[0]}")
                print(f"   New: {fixed_images[0]}")
                updated_count += 1
            else:
                print(f"⚠️  {skuid}: Update failed")
                error_count += 1
                
        except Exception as e:
            print(f"❌ {skuid}: Error - {e}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total products found: {len(faceaface_products)}")
    print(f"Successfully updated: {updated_count}")
    print(f"Errors/Skipped: {error_count}")
    print(f"Already correct: {len(faceaface_products) - updated_count - error_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
