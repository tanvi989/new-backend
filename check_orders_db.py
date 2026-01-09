#!/usr/bin/env python3
"""
Script to check orders in the database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import config
from pymongo import MongoClient
import json
from datetime import datetime

def main():
    print("=" * 80)
    print("CHECKING ORDERS IN DATABASE")
    print("=" * 80)
    
    # Connect to MongoDB
    print(f"\n📦 Connecting to MongoDB...")
    print(f"   URI: {config.MONGO_URI[:50]}...")
    print(f"   Database: {config.DATABASE_NAME}")
    
    try:
        client = MongoClient(config.MONGO_URI)
        db = client[config.DATABASE_NAME]
        
        # Test connection
        db.command('ping')
        print(f"✅ Connected successfully!")
        
        # List collections
        collections = db.list_collection_names()
        print(f"\n📋 Collections in database: {collections}")
        
        # Check orders collection
        if 'orders' in collections:
            orders_count = db.orders.count_documents({})
            print(f"\n📦 Orders collection:")
            print(f"   Total orders: {orders_count}")
            
            if orders_count > 0:
                # Get latest order
                latest_order = db.orders.find_one({}, sort=[('created', -1)])
                
                print(f"\n📄 Latest Order:")
                print(f"   Order ID: {latest_order.get('order_id')}")
                print(f"   User ID: {latest_order.get('user_id')}")
                print(f"   Payment Status: {latest_order.get('payment_status')}")
                print(f"   Order Status: {latest_order.get('order_status')}")
                print(f"   Order Total: £{latest_order.get('order_total', 0)}")
                print(f"   Created: {latest_order.get('created')}")
                
                # Check if prescription data exists in cart items
                cart_items = latest_order.get('cart', [])
                print(f"\n   Cart Items: {len(cart_items)}")
                
                for idx, item in enumerate(cart_items, 1):
                    print(f"\n   Item {idx}:")
                    product = item.get('product', {}).get('products', {})
                    print(f"      Product: {product.get('name', 'N/A')}")
                    print(f"      Price: £{product.get('list_price', 0)}")
                    
                    # Check prescription
                    prescription = item.get('prescription', {})
                    if prescription:
                        print(f"      Prescription: ✅ Present")
                        print(f"         Mode: {prescription.get('mode', 'N/A')}")
                        if 'gcs_url' in prescription:
                            print(f"         GCS URL: {prescription['gcs_url'][:60]}...")
                    else:
                        print(f"      Prescription: ❌ Not found")
                
                # Show full order structure (first order only)
                print(f"\n" + "=" * 80)
                print("FULL ORDER STRUCTURE (Latest Order):")
                print("=" * 80)
                print(json.dumps(latest_order, indent=2, default=str))
            else:
                print(f"\n⚠️  No orders found in database")
        else:
            print(f"\n❌ Orders collection does not exist!")
            print(f"   Available collections: {collections}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
