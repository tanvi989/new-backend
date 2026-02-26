#!/usr/bin/env python3
"""
Send order confirmation email for the last order in the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from datetime import datetime
from notification_service import MSG91Service

def send_last_order_email():
    """
    Find the last order and send confirmation email
    """
    print("=" * 80)
    print("SENDING CONFIRMATION EMAIL FOR LAST ORDER")
    print("=" * 80)
    
    # MongoDB connection
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://tanvi9891:tanvi2701@ac-jq2pulx-shard-00-00.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-01.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-02.ck8iin3.mongodb.net:27017/?replicaSet=atlas-29v1f8-shard-0&ssl=true&authSource=admin')
    
    try:
        client = MongoClient(mongo_uri)
        db = client['gaMultilens']
        orders_collection = db['orders']
        
        # Find the most recent order
        print("Finding most recent order...")
        recent_order = orders_collection.find_one(
            {"customer_email": {"$regex": "paradkartanvii@gmail.com", "$options": "i"}},
            sort=[("created", -1)]
        )
        
        if not recent_order:
            print("No orders found for paradkartanvii@gmail.com")
            return
        
        order_id = recent_order.get('order_id', 'UNKNOWN')
        customer_email = recent_order.get('customer_email', 'paradkartanvii@gmail.com')
        created = recent_order.get('created', datetime.now())
        
        print(f"Found order: {order_id}")
        print(f"Customer email: {customer_email}")
        print(f"Created: {created}")
        
        # Extract order items
        cart_items = recent_order.get('cart', [])
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
                print(f"    Lens data found:")
                print(f"      Main Category: {lens_data.get('main_category', 'N/A')}")
                print(f"      Lens Category Display: {lens_data.get('lensCategoryDisplay', 'N/A')}")
                print(f"      Lens Index: {lens_data.get('lensIndex', 'N/A')}")
                print(f"      Coating: {lens_data.get('coating', 'N/A')}")
                print(f"      Tint Type: {lens_data.get('tint_type', 'N/A')}")
                print(f"      Tint Color: {lens_data.get('tint_color', 'N/A')}")
            else:
                print(f"    No lens data found!")
        
        # Prepare order items for email
        order_items = []
        for it in cart_items:
            qty = max(1, int(it.get("quantity", 1)))
            price_val = float(it.get("price", 0))
            line_total = price_val * qty
            
            # Extract lens data like admin panel does
            lens_data = it.get("lens", {})
            
            order_items.append({
                "name": str(it.get("name", "Item")),
                "quantity": qty,
                "price": f"£{price_val:.2f}",
                "lineTotal": f"£{line_total:.2f}",
                "product_id": str(it.get("product_id", "")),
                "lens": {
                    "main_category": lens_data.get("main_category", "Eyewear"),
                    "lensCategoryDisplay": lens_data.get("lensCategoryDisplay", "Glasses"),
                    "lensIndex": lens_data.get("lensIndex", "Standard"),
                    "coating": lens_data.get("coating", "Standard"),
                    "tint_type": lens_data.get("tint_type", ""),
                    "tint_color": lens_data.get("tint_color", "")
                }
            })
        
        # Send email
        print(f"\nSending confirmation email...")
        
        notification_service = MSG91Service()
        
        total = recent_order.get("total_payable") or recent_order.get("order_total") or 0
        total_str = f"£{float(total):.2f}"
        user_name = "Customer"
        order_date_str = created.strftime("%d %b %Y, %H:%M") if hasattr(created, "strftime") else datetime.now().strftime("%d %b %Y, %H:%M")
        sub = recent_order.get("subtotal")
        disc = recent_order.get("discount_amount") or recent_order.get("discount", 0)
        ship = recent_order.get("shipping_cost", 0)
        
        result = notification_service.send_order_confirmation(
            email=customer_email,
            order_id=order_id,
            order_total=total_str,
            name=user_name,
            order_items=order_items,
            shipping_address=recent_order.get("shipping_address") or "",
            order_date=order_date_str,
            subtotal=f"£{float(sub):.2f}" if sub is not None else None,
            discount_amount=f"£{float(disc):.2f}",
            shipping_cost=f"£{float(ship):.2f}",
        )
        
        if result.get("success"):
            print(f"✅ Confirmation email sent successfully!")
            print(f"   Unique ID: {result.get('data', {}).get('unique_id', 'N/A')}")
            print(f"\nCheck your email at {customer_email}")
        else:
            print(f"❌ Failed to send confirmation email: {result.get('msg', 'Unknown error')}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    send_last_order_email()
