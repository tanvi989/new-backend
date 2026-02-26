#!/usr/bin/env python3
"""
Send confirmation email for the specific order ORD-1772098137784
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from datetime import datetime
from notification_service import MSG91Service

def send_specific_order_email():
    """
    Send confirmation email for ORD-1772098137784
    """
    print("=" * 80)
    print("SENDING CONFIRMATION EMAIL FOR ORDER: ORD-1772098137784")
    print("=" * 80)
    
    # MongoDB connection
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://tanvi9891:tanvi2701@ac-jq2pulx-shard-00-00.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-01.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-02.ck8iin3.mongodb.net:27017/?replicaSet=atlas-29v1f8-shard-0&ssl=true&authSource=admin')
    
    try:
        client = MongoClient(mongo_uri)
        db = client['gaMultilens']
        orders_collection = db['orders']
        
        # Find the specific order
        order = orders_collection.find_one({"order_id": "ORD-1772098137784"})
        
        if not order:
            print("ERROR: Order not found!")
            return
        
        print("Order found - preparing email...")
        
        # Extract order details
        customer_email = order.get('customer_email', 'paradkartanvii@gmail.com')
        cart_items = order.get('cart', [])
        
        # Prepare order items for email
        order_items = []
        for it in cart_items:
            qty = max(1, int(it.get("quantity", 1)))
            price_val = float(it.get("price", 0))
            line_total = price_val * qty
            
            # Extract lens data
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
        notification_service = MSG91Service()
        
        total = order.get("total_payable") or order.get("order_total") or 0
        total_str = f"£{float(total):.2f}"
        user_name = "Customer"
        created = order.get("created") or datetime.now()
        order_date_str = created.strftime("%d %b %Y, %H:%M") if hasattr(created, "strftime") else datetime.now().strftime("%d %b %Y, %H:%M")
        sub = order.get("subtotal")
        disc = order.get("discount_amount") or order.get("discount", 0)
        ship = order.get("shipping_cost", 0)
        
        print(f"Sending email to: {customer_email}")
        print(f"Order ID: ORD-1772098137784")
        print(f"Total: {total_str}")
        print(f"Items: {len(order_items)}")
        
        result = notification_service.send_order_confirmation(
            email=customer_email,
            order_id="ORD-1772098137784",
            order_total=total_str,
            name=user_name,
            order_items=order_items,
            shipping_address=order.get("shipping_address") or "",
            order_date=order_date_str,
            subtotal=f"£{float(sub):.2f}" if sub is not None else None,
            discount_amount=f"£{float(disc):.2f}",
            shipping_cost=f"£{float(ship):.2f}",
        )
        
        if result.get("success"):
            print("SUCCESS: Confirmation email sent!")
            print(f"Unique ID: {result.get('data', {}).get('unique_id', 'N/A')}")
            
            # Update the order to mark email as sent
            orders_collection.update_one(
                {"order_id": "ORD-1772098137784"},
                {"$set": {"confirmation_email_sent_at": datetime.now()}}
            )
            print("Order marked as email sent")
            
        else:
            print(f"ERROR: Failed to send confirmation email: {result.get('msg', 'Unknown error')}")
        
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    send_specific_order_email()
