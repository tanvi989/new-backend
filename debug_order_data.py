#!/usr/bin/env python3
"""
Debug what's actually in the order data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from datetime import datetime

def debug_order_data():
    """
    Debug the actual order data structure
    """
    print("=" * 80)
    print("DEBUGGING ORDER DATA STRUCTURE")
    print("=" * 80)
    
    # MongoDB connection
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    
    try:
        client = MongoClient(mongo_uri)
        db = client['gaMultilens']
        orders_collection = db['orders']
        
        # Find recent orders
        recent_orders = list(orders_collection.find({"order_id": {"$regex": "E45A8506"}}).sort("created", -1).limit(3))
        
        if not recent_orders:
            print("No orders found with E45A8506")
            return
        
        print(f"Found {len(recent_orders)} recent orders:")
        
        for i, order in enumerate(recent_orders, 1):
            print(f"\n{'='*60}")
            print(f"ORDER {i}: {order.get('order_id')}")
            print(f"{'='*60}")
            print(f"Created: {order.get('created')}")
            print(f"Total: {order.get('total_payable', order.get('order_total', 'N/A'))}")
            
            # Check cart items
            cart_items = order.get('cart', [])
            print(f"Cart items: {len(cart_items)}")
            
            for j, item in enumerate(cart_items, 1):
                print(f"\n  Item {j}:")
                print(f"    Name: {item.get('name', 'N/A')}")
                print(f"    Product ID: {item.get('product_id', 'N/A')}")
                print(f"    Quantity: {item.get('quantity', 'N/A')}")
                print(f"    Price: {item.get('price', 'N/A')}")
                
                # Check lens data
                lens_data = item.get('lens', {})
                print(f"    Lens data keys: {list(lens_data.keys()) if lens_data else 'No lens data'}")
                
                if lens_data:
                    print(f"    Main Category: {lens_data.get('main_category', 'N/A')}")
                    print(f"    Lens Category Display: {lens_data.get('lensCategoryDisplay', 'N/A')}")
                    print(f"    Lens Index: {lens_data.get('lensIndex', 'N/A')}")
                    print(f"    Coating: {lens_data.get('coating', 'N/A')}")
                    print(f"    Tint Type: {lens_data.get('tint_type', 'N/A')}")
                    print(f"    Tint Color: {lens_data.get('tint_color', 'N/A')}")
                else:
                    print(f"    No lens data found!")
                
                # Check if lens data is stored elsewhere
                print(f"    All item keys: {list(item.keys())}")
                
                # Check product object
                product_data = item.get('product', {})
                if product_data:
                    print(f"    Product keys: {list(product_data.keys())}")
                    products_data = product_data.get('products', {})
                    if products_data:
                        print(f"    Products keys: {list(products_data.keys())}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_order_data()
