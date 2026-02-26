#!/usr/bin/env python3
"""
Find why duplicate order confirmation emails are being sent
"""

def check_email_triggers():
    """
    Check all places where order confirmation emails are triggered
    """
    print("=" * 80)
    print("DUPLICATE EMAIL INVESTIGATION")
    print("=" * 80)
    
    print("\n1. ALL ORDER CONFIRMATION TRIGGERS:")
    print("=" * 40)
    
    triggers = [
        {
            "location": "app.py line 1659",
            "endpoint": "POST /orders",
            "trigger": "When order is created via API",
            "data": "Extracts from request.cart_items"
        },
        {
            "location": "app.py line 1803", 
            "endpoint": "POST /send-confirmation-email",
            "trigger": "When order not found in DB",
            "data": "order_items=[] (EMPTY!)"
        },
        {
            "location": "app.py line 1851",
            "endpoint": "POST /send-confirmation-email", 
            "trigger": "When order found in DB",
            "data": "Extracts from order_doc.cart"
        },
        {
            "location": "app.py line 2018",
            "endpoint": "POST /payments/confirm",
            "trigger": "When payment confirmed",
            "data": "Extracts from cart_service.get_cart()"
        },
        {
            "location": "app.py line 2128",
            "endpoint": "POST /payments/stripe-webhook",
            "trigger": "When Stripe webhook received",
            "data": "Extracts from order_doc.cart"
        }
    ]
    
    for i, trigger in enumerate(triggers, 1):
        print(f"{i}. {trigger['location']}")
        print(f"   Endpoint: {trigger['endpoint']}")
        print(f"   Trigger: {trigger['trigger']}")
        print(f"   Data: {trigger['data']}")
        print()
    
    print("2. POSSIBLE DUPLICATE CAUSES:")
    print("=" * 40)
    print("A. Multiple cart items:")
    print("   - If you have BERG and K+ in cart")
    print("   - Each item might trigger separate email")
    print()
    print("B. Multiple payment confirmations:")
    print("   - Payment webhook + frontend confirmation")
    print("   - Double trigger from payment flow")
    print()
    print("C. Multiple order creation attempts:")
    print("   - Order created + confirmation email sent")
    print("   - Then send-confirmation-email called again")
    print()
    print("D. Cart has multiple items:")
    print("   - BERG (E45A8506) - £217.00")
    print("   - K+ (unknown ID) - £177.00")
    print("   - Total: £394.00 (but you see £217.00 and £177.00 separately)")
    
    print("\n3. CHECK YOUR CART:")
    print("=" * 40)
    print("The K+ email suggests you have another item in your cart.")
    print("Check if your cart contains:")
    print("- BERG (E45A8506) - £217.00")
    print("- K+ (unknown ID) - £177.00")
    print()
    print("If so, the system might be sending separate emails for each item.")
    
    print("\n4. SOLUTIONS:")
    print("=" * 40)
    print("Option 1: Clear your cart")
    print("   - Remove K+ item from cart")
    print("   - Only keep BERG item")
    print()
    print("Option 2: Check backend logic")
    print("   - Look for loops that send emails per item")
    print("   - Ensure only one email per order")
    print()
    print("Option 3: Check payment flow")
    print("   - See if payment confirmation triggers multiple emails")
    print("   - Add deduplication logic")
    
    print("\n5. IMMEDIATE ACTION:")
    print("=" * 40)
    print("Check your cart at: http://localhost:3001/cart")
    print("See if you have multiple items (BERG + K+)")
    print("If yes, remove K+ and try again")

if __name__ == "__main__":
    check_email_triggers()
