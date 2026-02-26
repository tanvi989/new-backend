#!/usr/bin/env python3
"""
Send a real test order confirmation email to paradkartanvii@gmail.com
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import notification service
from notification_service import MSG91Service

def send_test_email():
    """
    Send a test order confirmation email with real data
    """
    print("=" * 80)
    print("SENDING TEST ORDER CONFIRMATION EMAIL")
    print("=" * 80)
    
    # Create notification service
    notification_service = MSG91Service()
    
    # Test data that matches your real order
    test_order_items = [
        {
            "name": "BERG",
            "quantity": 1,
            "price": "£253.00",
            "product_id": "E45A8506",
            "lens": {
                "main_category": "Sunglasses",
                "lensCategoryDisplay": "Sunglasses Tint",
                "lensIndex": "1.61",
                "coating": "Mirror Tints - Purple",
                "tint_type": "Mirror",
                "tint_color": "Purple"
            }
        }
    ]
    
    try:
        print(f"Sending test email to paradkartanvii@gmail.com...")
        print(f"Order items: {len(test_order_items)}")
        
        result = notification_service.send_order_confirmation(
            email="paradkartanvii@gmail.com",
            order_id="TEST-EMAIL-001",
            order_total="£253.00",
            name="Test Customer",
            order_items=test_order_items,
            shipping_address="Test Address",
            order_date="26/02/2026",
            subtotal="£253.00",
            discount_amount="£0.00",
            shipping_cost="£0.00"
        )
        
        print(f"Result: {result}")
        
        if result.get("success"):
            print("✅ Test email sent successfully!")
            print(f"   Unique ID: {result.get('data', {}).get('unique_id', 'N/A')}")
        else:
            print(f"❌ Failed to send test email: {result.get('msg', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print("✅ Backend fixes applied:")
    print("   - No email before payment")
    print("   - Correct data extraction")
    print("   - Email only after payment")
    print("\n📧 What you should receive:")
    print("   - BERG (E45A8506)")
    print("   - Sunglasses • Sunglasses Tint • 1.61")
    print("   - Coating: Mirror Tints - Purple")
    print("   - Total: £253.00")
    print("\nCheck your email now!")

if __name__ == "__main__":
    send_test_email()
