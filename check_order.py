#!/usr/bin/env python3
"""
Check the specific order without Unicode characters
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from notification_service import MSG91Service

def check_order():
    """
    Check the specific order ID
    """
    print("=" * 80)
    print("CHECKING ORDER: ORD-1772098137784")
    print("=" * 80)
    
    # MongoDB connection
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://tanvi9891:tanvi2701@ac-jq2pulx-shard-00-00.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-01.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-02.ck8iin3.mongodb.net:27017/?replicaSet=atlas-29v1f8-shard-0&ssl=true&authSource=admin')
    
    try:
        client = MongoClient(mongo_uri)
        db = client['gaMultilens']
        orders_collection = db['orders']
        
        # Find the specific order
        print("Finding order ORD-1772098137784...")
        order = orders_collection.find_one({"order_id": "ORD-1772098137784"})
        
        if not order:
            print("ERROR: Order not found in database!")
            print("This means:")
            print("1. The order was not created in the database")
            print("2. The order_id might be different")
            print("3. The payment webhook failed")
            return
        
        print("SUCCESS: Order found in database!")
        print(f"Customer email: {order.get('customer_email', 'N/A')}")
        print(f"Created: {order.get('created', 'N/A')}")
        print(f"Status: {order.get('order_status', 'N/A')}")
        
        # Check if email was already sent
        email_sent_at = order.get('confirmation_email_sent_at')
        if email_sent_at:
            print(f"WARNING: Email already sent at: {email_sent_at}")
            print("This explains why you're not getting another email")
        else:
            print("SUCCESS: Email not sent yet - this is expected")
        
        # Check cart items
        cart_items = order.get('cart', [])
        print(f"Cart items: {len(cart_items)}")
        
        for i, item in enumerate(cart_items, 1):
            print(f"\n  Item {i}:")
            print(f"    Name: {item.get('name', 'N/A')}")
            print(f"    Product ID: {item.get('product_id', 'N/A')}")
            print(f"    Quantity: {item.get('quantity', 'N/A')}")
            print(f"    Price: {item.get('price', 'N/A')}")
            
            # Check lens data
            lens_data = item.get('lens', {})
            if lens_data:
                print(f"    SUCCESS: Lens data found:")
                print(f"      Main Category: {lens_data.get('main_category', 'N/A')}")
                print(f"      Lens Category Display: {lens_data.get('lensCategoryDisplay', 'N/A')}")
                print(f"      Lens Index: {lens_data.get('lensIndex', 'N/A')}")
                print(f"      Coating: {lens_data.get('coating', 'N/A')}")
            else:
                print(f"    ERROR: No lens data found!")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_order()
