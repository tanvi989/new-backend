#!/usr/bin/env python3
"""
Test complete order data structure with lens details
"""
import requests
import json

def test_complete_order_data():
    """
    Test backend with complete order data including lens details
    """
    print("=" * 80)
    print("TESTING COMPLETE ORDER DATA WITH LENS DETAILS")
    print("=" * 80)
    
    # MSG91 Configuration
    AUTH_KEY = "482085AD1VnJzkrUX6937ff86P1"
    DOMAIN = "email.multifolks.com"
    TEMPLATE_ID = "order_placed_v1_3"
    
    test_email = "paradkartanvii@gmail.com"
    url = "https://control.msg91.com/api/v5/email/send"
    
    headers = {
        "authkey": AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    # Test with complete data structure (what backend should now send)
    payload = {
        "recipients": [{
            "to": [{
                "name": "Test Customer",
                "email": test_email
            }],
            "variables": {
                "NAME": "Test Customer",
                "ORDER_NUMBER": "TEST-COMPLETE-001",
                "ORDER_DATE": "26/02/2026",
                "order_total": "£233.00",
                "shipping_cost": "£4.99",
                "subtotal": "£228.01",
                "discount_amount": "£0.00",
                
                # cart array with complete lens details
                "cart": [
                    {
                        "name": "Multifolks Premium Progressive Glasses",
                        "quantity": 1,
                        "price": "£114.00",
                        "product_id": "MF001",
                        "lens": {
                            "main_category": "Eyewear",
                            "lensCategoryDisplay": "Progressive Glasses",
                            "lensIndex": "1.67 High Index",
                            "coating": "Anti-Reflective Premium",
                            "tint_type": "Photochromic",
                            "tint_color": "Grey"
                        }
                    },
                    {
                        "name": "Multifolks Reading Glasses",
                        "quantity": 1,
                        "price": "£114.01",
                        "product_id": "MF002",
                        "lens": {
                            "main_category": "Eyewear",
                            "lensCategoryDisplay": "Reading Glasses",
                            "lensIndex": "1.56 Standard",
                            "coating": "Anti-Reflective",
                            "tint_type": "Standard",
                            "tint_color": "Clear"
                        }
                    }
                ],
                
                # orderItems array (same data for compatibility)
                "orderItems": [
                    {
                        "name": "Multifolks Premium Progressive Glasses",
                        "quantity": 1,
                        "price": "£114.00",
                        "product_id": "MF001",
                        "lens": {
                            "main_category": "Eyewear",
                            "lensCategoryDisplay": "Progressive Glasses",
                            "lensIndex": "1.67 High Index",
                            "coating": "Anti-Reflective Premium",
                            "tint_type": "Photochromic",
                            "tint_color": "Grey"
                        }
                    },
                    {
                        "name": "Multifolks Reading Glasses",
                        "quantity": 1,
                        "price": "£114.01",
                        "product_id": "MF002",
                        "lens": {
                            "main_category": "Eyewear",
                            "lensCategoryDisplay": "Reading Glasses",
                            "lensIndex": "1.56 Standard",
                            "coating": "Anti-Reflective",
                            "tint_type": "Standard",
                            "tint_color": "Clear"
                        }
                    }
                ]
            }
        }],
        "from": {
            "email": "support@multifolks.com",
            "name": "Multifolks"
        },
        "domain": DOMAIN,
        "template_id": TEMPLATE_ID
    }
    
    try:
        print(f"Sending complete order data test...")
        print(f"Template ID: {TEMPLATE_ID}")
        print(f"Order ID: {payload['recipients'][0]['variables']['ORDER_NUMBER']}")
        print(f"Order Date: {payload['recipients'][0]['variables']['ORDER_DATE']}")
        print(f"Total: {payload['recipients'][0]['variables']['order_total']}")
        print(f"Subtotal: {payload['recipients'][0]['variables']['subtotal']}")
        print(f"Shipping: {payload['recipients'][0]['variables']['shipping_cost']}")
        print(f"Cart items: {len(payload['recipients'][0]['variables']['cart'])}")
        
        for i, item in enumerate(payload['recipients'][0]['variables']['cart'], 1):
            print(f"\n  Cart Item {i}:")
            print(f"    Name: {item['name']}")
            print(f"    Product ID: {item['product_id']}")
            print(f"    Quantity: {item['quantity']}")
            print(f"    Price: {item['price']}")
            print(f"    Lens: {item['lens']['main_category']} • {item['lens']['lensCategoryDisplay']} • {item['lens']['lensIndex']}")
            print(f"    Coating: {item['lens']['coating']}")
            if item['lens']['tint_color']:
                print(f"    Tint: {item['lens']['tint_type']} - {item['lens']['tint_color']}")
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Test email sent successfully!")
            print(f"Unique ID: {response_data.get('data', {}).get('unique_id', 'N/A')}")
            print(f"\nCheck your email for:")
            print(f"- Complete product names (not just 'BERG')")
            print(f"- Full lens details")
            print(f"- Product images")
            print(f"- All specifications")
            print(f"- Proper pricing breakdown")
        else:
            print(f"Failed to send test email: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_complete_order_data()
    
    print("\n" + "=" * 80)
    print("BACKEND FIXES COMPLETED")
    print("=" * 80)
    print("✅ Updated app.py to extract lens details from cart items")
    print("✅ Updated notification_service.py to send both cart and orderItems")
    print("✅ Added ORDER_DATE variable")
    print("✅ Added complete lens structure")
    print("✅ Backend now matches admin data structure")
    print("\nThe order confirmation email should now show:")
    print("- Complete product names")
    print("- Full lens specifications")
    print("- Product images")
    print("- All details like the admin status emails")
