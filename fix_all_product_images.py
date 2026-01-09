#!/usr/bin/env python3
"""
Fix ALL Product Image URLs in Database

This script updates the image URLs for ALL products in MongoDB
to match the actual file naming convention in Google Cloud Storage.

Changes:
- {SKUID}-1.png → {SKUID}.png (first image)
- {SKUID}-1_1.png → {SKUID}_1.png
- {SKUID}-1_2.png → {SKUID}_2.png
etc.

This applies to all products in the Faceaface folder, regardless of brand.
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
    # Only fix if URL contains the Faceaface folder
    if 'Faceaface/' not in url:
        return url
    
    # Pattern: {SKUID}-1.png → {SKUID}.png (first image)
    # Pattern: {SKUID}-1_N.png → {SKUID}_N.png (subsequent images)
    
    # Replace {SKUID}-1.png with {SKUID}.png (first image)
    url = url.replace(f"{skuid}-1.png", f"{skuid}.png")
    
    # Replace {SKUID}-1_N.png with {SKUID}_N.png (subsequent images)
    url = re.sub(f"{skuid}-1_(\\d+)\\.png", f"{skuid}_\\1.png", url)
    
    return url

def main():
    print("=" * 60)
    print("Universal Product Image URL Fix Script")
    print("=" * 60)
    
    # Connect to MongoDB
    print(f"\nConnecting to MongoDB...")
    print(f"Database: {config.DATABASE_NAME}")
    
    client = MongoClient(config.MONGO_URI)
    db = client[config.DATABASE_NAME]
    collection = db['products']
    
    # Find all products with images in Faceaface folder
    query = {
        'images': {'$exists': True, '$ne': []},
        'images.0': {'$regex': 'Faceaface/'}
    }
    products = list(collection.find(query))
    
    print(f"\nFound {len(products)} products with Faceaface images")
    
    if len(products) == 0:
        print("No products to update. Exiting.")
        return
    
    # Update each product
    updated_count = 0
    error_count = 0
    already_correct = 0
    
    for product in products:
        skuid = product.get('skuid', '')
        product_id = product.get('_id')
        brand = product.get('brand', 'Unknown')
        
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
            already_correct += 1
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
                print(f"✅ {brand} - {skuid}: Updated" + (" + variants" if variants_changed else ""))
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
    print(f"Total products found: {len(products)}")
    print(f"Successfully updated: {updated_count}")
    print(f"Already correct: {already_correct}")
    print(f"Errors/Skipped: {error_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
