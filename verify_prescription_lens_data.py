#!/usr/bin/env python3
"""
Test script to verify complete prescription and lens data storage in orders
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import config
from pymongo import MongoClient
import json
from datetime import datetime

def check_prescription_fields(prescription):
    """Check if all prescription fields are present"""
    required_fields = {
        'mode': 'Prescription mode (upload/manual)',
        'gcs_url': 'GCS URL for uploaded prescription',
        'fileName': 'Original file name',
        'fileType': 'File type',
        'fileSize': 'File size'
    }
    
    manual_fields = {
        'rightEye': 'Right eye prescription',
        'leftEye': 'Left eye prescription',
        'pd': 'Pupillary distance',
        'addPower': 'Additional power'
    }
    
    print("\n   📋 Prescription Fields:")
    mode = prescription.get('mode', 'N/A')
    print(f"      Mode: {mode}")
    
    if mode == 'upload':
        for field, description in required_fields.items():
            value = prescription.get(field)
            status = "✅" if value else "❌"
            print(f"      {status} {field}: {value if value else 'MISSING'}")
    elif mode == 'manual':
        for field, description in manual_fields.items():
            value = prescription.get(field)
            status = "✅" if value else "❌"
            if isinstance(value, dict):
                print(f"      {status} {field}:")
                for k, v in value.items():
                    print(f"         {k}: {v}")
            else:
                print(f"      {status} {field}: {value if value else 'MISSING'}")

def check_lens_fields(lens):
    """Check if all lens fields are present"""
    lens_fields = {
        'lensType': 'Lens type (Single Vision, Bifocal, etc.)',
        'lensPackage': 'Lens package name',
        'selling_price': 'Lens price',
        'coating': 'Lens coating',
        'coating_price': 'Coating price',
        'tint': 'Lens tint',
        'tintColor': 'Tint color'
    }
    
    print("\n   👓 Lens Fields:")
    for field, description in lens_fields.items():
        value = lens.get(field)
        status = "✅" if value is not None else "⚠️"
        print(f"      {status} {field}: {value if value is not None else 'Not set'}")

def main():
    print("=" * 80)
    print("VERIFYING COMPLETE PRESCRIPTION & LENS DATA STORAGE")
    print("=" * 80)
    
    try:
        client = MongoClient(config.MONGO_URI)
        db = client[config.DATABASE_NAME]
        
        # Check orders
        orders_count = db.orders.count_documents({})
        print(f"\n📦 Total orders in database: {orders_count}")
        
        if orders_count == 0:
            print("\n⚠️  No orders found. Please complete a test order first.")
            return
        
        # Get all orders
        orders = list(db.orders.find({}).sort('created', -1))
        
        print(f"\n🔍 Analyzing {len(orders)} order(s)...\n")
        
        for idx, order in enumerate(orders, 1):
            print("=" * 80)
            print(f"ORDER {idx}: {order.get('order_id')}")
            print("=" * 80)
            print(f"User ID: {order.get('user_id')}")
            print(f"Payment Status: {order.get('payment_status')}")
            print(f"Order Status: {order.get('order_status')}")
            print(f"Created: {order.get('created')}")
            
            cart_items = order.get('cart', [])
            print(f"\n📦 Cart Items: {len(cart_items)}")
            
            for item_idx, item in enumerate(cart_items, 1):
                print(f"\n{'─' * 80}")
                print(f"ITEM {item_idx}:")
                print(f"{'─' * 80}")
                
                # Product info
                product = item.get('product', {}).get('products', {})
                print(f"   Product: {product.get('name', 'N/A')}")
                print(f"   SKU: {product.get('skuid', 'N/A')}")
                print(f"   Price: £{product.get('list_price', 0)}")
                print(f"   Quantity: {item.get('quantity', 1)}")
                
                # Check lens data
                lens = item.get('lens')
                if lens:
                    print(f"\n   ✅ LENS DATA FOUND")
                    check_lens_fields(lens)
                else:
                    print(f"\n   ❌ NO LENS DATA")
                
                # Check prescription data
                prescription = item.get('prescription')
                if prescription:
                    print(f"\n   ✅ PRESCRIPTION DATA FOUND")
                    check_prescription_fields(prescription)
                else:
                    print(f"\n   ❌ NO PRESCRIPTION DATA")
            
            print("\n" + "=" * 80)
            print("COMPLETE ORDER STRUCTURE:")
            print("=" * 80)
            print(json.dumps(order, indent=2, default=str))
            print("\n")
        
        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        
        total_items = sum(len(order.get('cart', [])) for order in orders)
        items_with_prescription = sum(
            1 for order in orders 
            for item in order.get('cart', []) 
            if item.get('prescription')
        )
        items_with_lens = sum(
            1 for order in orders 
            for item in order.get('cart', []) 
            if item.get('lens')
        )
        
        print(f"Total Items: {total_items}")
        print(f"Items with Prescription: {items_with_prescription}")
        print(f"Items with Lens: {items_with_lens}")
        
        if total_items > 0:
            print(f"\nPrescription Coverage: {(items_with_prescription/total_items)*100:.1f}%")
            print(f"Lens Coverage: {(items_with_lens/total_items)*100:.1f}%")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
