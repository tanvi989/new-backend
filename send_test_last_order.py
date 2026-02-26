#!/usr/bin/env python3
"""
Send test email for the last order
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from order_service import OrderService
import config
from pymongo import MongoClient
import certifi
from notification_service import MSG91Service

def get_last_order():
    """Get the most recent order from database"""
    try:
        # Connect to database
        uri = config.MONGO_URI
        client = MongoClient(uri, tlsCAFile=certifi.where())
        db = client[config.DATABASE_NAME]
        orders_collection = db['orders']

        # Get the most recent order
        latest_order = orders_collection.find_one({}, sort=[('created', -1)])
        
        if latest_order:
            print(f'Latest Order ID: {latest_order.get("order_id")}')
            print(f'Customer Email: {latest_order.get("customer_email")}')
            print(f'Order Total: £{latest_order.get("order_total", 0):.2f}')
            print(f'Created: {latest_order.get("created")}')
            print(f'Items: {len(latest_order.get("cart", []))}')
            return latest_order
        else:
            print('No orders found')
            return None
            
    except Exception as e:
        print(f'Error fetching order: {e}')
        return None

def send_test_email(order):
    """Send test email for the given order"""
    try:
        # Create notification service
        notification_service = MSG91Service()
        
        # Extract order data
        order_id = order.get("order_id")
        customer_email = order.get("customer_email")
        total = order.get("total_payable") or order.get("order_total") or 0
        total_str = f"£{float(total):.2f}"
        
        # Prepare order items
        order_items = []
        for it in order.get("cart", []):
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
        
        # Extract other details
        from datetime import datetime, timezone
        created = order.get("created") or order.get("updated_at") or datetime.now(timezone.utc)
        order_date_str = created.strftime("%d %b %Y, %H:%M") if hasattr(created, "strftime") else datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M")
        
        sub = order.get("subtotal")
        disc = order.get("discount_amount") or order.get("discount", 0)
        ship = order.get("shipping_cost", 0)
        
        print(f"\nSending test email to: {customer_email}")
        print(f"Order ID: {order_id}")
        print(f"Total: {total_str}")
        print(f"Items: {len(order_items)}")
        
        # Send the email
        result = notification_service.send_order_confirmation(
            customer_email, order_id, total_str, "Test Customer", order_items=order_items,
            shipping_address=order.get("shipping_address") or "",
            order_date=order_date_str,
            subtotal=f"£{float(sub):.2f}" if sub is not None else None,
            discount_amount=f"£{float(disc):.2f}",
            shipping_cost=f"£{float(ship):.2f}",
        )
        
        print(f"\nEmail result: {result}")
        
        if result.get("success"):
            print("✅ Test email sent successfully!")
        else:
            print(f"❌ Failed to send email: {result.get('msg')}")
            
    except Exception as e:
        print(f'Error sending email: {e}')
        import traceback
        traceback.print_exc()

def main():
    print("=" * 80)
    print("SENDING TEST EMAIL FOR LAST ORDER")
    print("=" * 80)
    
    # Get the last order
    last_order = get_last_order()
    
    if last_order:
        # Send test email
        send_test_email(last_order)
    else:
        print("No orders found to test with")

if __name__ == "__main__":
    main()
