#!/usr/bin/env python3
"""
Test what variables the backend is actually sending
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import notification service
from notification_service import MSG91Service

def test_notification_variables():
    """
    Test what variables are actually sent by notification_service
    """
    print("=" * 80)
    print("TESTING NOTIFICATION SERVICE VARIABLES")
    print("=" * 80)
    
    # Create test data that matches what backend should send
    test_order_items = [
        {
            "name": "BERG",
            "quantity": 1,
            "price": "£273.00",
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
    
    print("Test order items:")
    for i, item in enumerate(test_order_items, 1):
        print(f"  Item {i}: {item}")
    
    # Create notification service
    notification_service = MSG91Service()
    
    # Test the send_order_confirmation method
    print("\nTesting send_order_confirmation...")
    
    try:
        # This will show what variables are actually sent
        result = notification_service.send_order_confirmation(
            email="paradkartanvii@gmail.com",
            order_id="TEST-VARIABLES-001",
            order_total="£273.00",
            name="Test Customer",
            order_items=test_order_items,
            shipping_address="Test Address",
            order_date="26/02/2026",
            subtotal="£267.00",
            discount_amount="£6.00",
            shipping_cost="£6.00"
        )
        
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_notification_variables()
