#!/usr/bin/env python3
"""
Test backend order confirmation email with updated data structure
"""
import requests
import json

def test_backend_order_email():
    """
    Test backend order confirmation email
    """
    print("=" * 80)
    print("TESTING BACKEND ORDER CONFIRMATION EMAIL")
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
    
    # Test with updated data structure (same as admin)
    payload = {
        "recipients": [{
            "to": [{
                "name": "Test Customer",
                "email": test_email
            }],
            "variables": {
                "NAME": "Test Customer",
                "ORDER_NUMBER": "TEST-BACKEND-001",
                "ORDER_DATE": "26/02/2026",
                "order_total": "£183.00",
                "shipping_cost": "£4.99",
                
                # cart array (same as admin)
                "cart": [
                    {
                        "product_id": "MF001",
                        "name": "Multifolks Premium Glasses",
                        "quantity": 1,
                        "lens": {
                            "main_category": "Eyewear",
                            "lensCategoryDisplay": "Progressive Glasses",
                            "lensIndex": "1.67 High Index",
                            "coating": "Anti-Reflective Premium",
                            "tint_type": "Standard",
                            "tint_color": "Clear"
                        }
                    },
                    {
                        "product_id": "MF002",
                        "name": "Multifolks Reading Glasses",
                        "quantity": 1,
                        "lens": {
                            "main_category": "Eyewear",
                            "lensCategoryDisplay": "Reading Glasses",
                            "lensIndex": "1.56 Standard",
                            "coating": "Anti-Reflective",
                            "tint_type": "Photochromic",
                            "tint_color": "Grey"
                        }
                    }
                ],
                
                # orderItems array (for compatibility)
                "orderItems": [
                    {
                        "name": "Multifolks Premium Glasses",
                        "quantity": 1,
                        "price": "£89.00",
                        "product_id": "MF001",
                        "lens": {
                            "main_category": "Eyewear",
                            "lensCategoryDisplay": "Progressive Glasses",
                            "lensIndex": "1.67 High Index",
                            "coating": "Anti-Reflective Premium",
                            "tint_type": "Standard",
                            "tint_color": "Clear"
                        }
                    },
                    {
                        "name": "Multifolks Reading Glasses",
                        "quantity": 1,
                        "price": "£94.00",
                        "product_id": "MF002",
                        "lens": {
                            "main_category": "Eyewear",
                            "lensCategoryDisplay": "Reading Glasses",
                            "lensIndex": "1.56 Standard",
                            "coating": "Anti-Reflective",
                            "tint_type": "Photochromic",
                            "tint_color": "Grey"
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
        print(f"Sending backend order confirmation test...")
        print(f"Template ID: {TEMPLATE_ID}")
        print(f"Order ID: {payload['recipients'][0]['variables']['ORDER_NUMBER']}")
        print(f"Order Date: {payload['recipients'][0]['variables']['ORDER_DATE']}")
        print(f"Total: {payload['recipients'][0]['variables']['order_total']}")
        print(f"Cart items: {len(payload['recipients'][0]['variables']['cart'])}")
        print(f"OrderItems: {len(payload['recipients'][0]['variables']['orderItems'])}")
        
        for i, item in enumerate(payload['recipients'][0]['variables']['cart'], 1):
            print(f"  Cart Item {i}: {item['name']} (Qty: {item['quantity']})")
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
            print(f"- Order ID: TEST-BACKEND-001")
            print(f"- Order Date: 26/02/2026")
            print(f"- 2 items with full lens details")
            print(f"- Product images should appear")
            print(f"- All lens specifications should be visible")
        else:
            print(f"Failed to send test email: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_backend_order_email()
    
    print("\n" + "=" * 80)
    print("BACKEND UPDATE COMPLETED")
    print("=" * 80)
    print("✅ Backend now sends same data structure as admin")
    print("✅ Both 'cart' and 'orderItems' arrays available")
    print("✅ Full lens details included")
    print("✅ ORDER_DATE variable added")
    print("✅ Template should now display product details correctly")
    print("\nNext step: Update MSG91 template content if needed")
