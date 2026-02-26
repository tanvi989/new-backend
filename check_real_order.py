#!/usr/bin/env python3
"""
Check the actual order data structure in the database
"""
import requests
import json

def check_order_via_api():
    """
    Check order data via the backend API
    """
    print("=" * 80)
    print("CHECKING ORDER DATA VIA API")
    print("=" * 80)
    
    backend_url = "http://localhost:5000"
    
    # Try to get order details (this will show us the actual data structure)
    test_order_id = "E45A8506"  # Use your actual order ID
    
    try:
        # Try the public endpoint first
        response = requests.get(f"{backend_url}/api/v1/public/orders/{test_order_id}")
        
        if response.status_code == 200:
            order_data = response.json()
            print(f"✅ Order found via public endpoint")
            print(f"Order ID: {order_data.get('data', {}).get('order_id', 'N/A')}")
            print(f"Total: {order_data.get('data', {}).get('total', 'N/A')}")
            
            # Check cart items
            cart_items = order_data.get('data', {}).get('cart', [])
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
                    print(f"    ✅ Lens data found:")
                    print(f"      Main Category: {lens_data.get('main_category', 'N/A')}")
                    print(f"      Lens Category Display: {lens_data.get('lensCategoryDisplay', 'N/A')}")
                    print(f"      Lens Index: {lens_data.get('lensIndex', 'N/A')}")
                    print(f"      Coating: {lens_data.get('coating', 'N/A')}")
                    print(f"      Tint Type: {lens_data.get('tint_type', 'N/A')}")
                    print(f"      Tint Color: {lens_data.get('tint_color', 'N/A')}")
                else:
                    print(f"    ❌ No lens data found!")
                    print(f"    Available keys: {list(item.keys())}")
                    
                    # Check if lens data is stored under different key
                    for key in item.keys():
                        if 'lens' in key.lower() or 'category' in key.lower() or 'coating' in key.lower():
                            print(f"    Possible lens key: {key} = {item.get(key, 'N/A')}")
        else:
            print(f"❌ Order not found via public endpoint: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

def check_backend_logs():
    """
    Check what the backend is actually sending
    """
    print("\n" + "=" * 80)
    print("CHECKING BACKEND EMAIL LOGS")
    print("=" * 80)
    
    print("Look for these patterns in backend logs:")
    print("1. [MSG91] Sending order confirmation to")
    print("2. Variables sent:")
    print("3. cart: [")
    print("4. orderItems: [")
    print("\nThe backend logs should show exactly what data is being sent to MSG91")

if __name__ == "__main__":
    check_order_via_api()
    check_backend_logs()
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("1. Check if the API shows lens data")
    print("2. If lens data exists, the backend extraction needs fixing")
    print("3. If no lens data, check how data is stored in database")
    print("4. The issue is likely in notification_service.py data extraction")
