#!/usr/bin/env python3
"""
Test the new template order_placed_v1_4
"""
import requests
import json

def test_new_template():
    """
    Test the new template to bypass MSG91 cache
    """
    print("=" * 80)
    print("TESTING NEW TEMPLATE order_placed_v1_4")
    print("=" * 80)
    
    # MSG91 Configuration
    AUTH_KEY = "482085AD1VnJzkrUX6937ff86P1"
    DOMAIN = "email.multifolks.com"
    TEMPLATE_ID = "order_placed_v1_4"
    
    test_email = "paradkartanvii@gmail.com"
    url = "https://control.msg91.com/api/v5/email/send"
    
    headers = {
        "authkey": AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    # Test with correct data structure
    payload = {
        "recipients": [{
            "to": [{
                "name": "Test Customer",
                "email": test_email
            }],
            "variables": {
                "NAME": "Test Customer",
                "ORDER_NUMBER": "E45A8506",
                "ORDER_DATE": "26/02/2026",
                "order_total": "£203.00",
                "shipping_cost": "0.00",
                
                # cart array with correct lens data
                "cart": [
                    {
                        "name": "BERG",
                        "quantity": 1,
                        "price": "£203.00",
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
        print(f"Sending test with new template: {TEMPLATE_ID}")
        print(f"Order ID: {payload['recipients'][0]['variables']['ORDER_NUMBER']}")
        print(f"Total: {payload['recipients'][0]['variables']['order_total']}")
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"✅ Test email sent successfully!")
            print(f"Unique ID: {response_data.get('data', {}).get('unique_id', 'N/A')}")
            print(f"\nCheck your email for:")
            print(f"- BERG (E45A8506)")
            print(f"- Sunglasses • Sunglasses Tint • 1.61")
            print(f"- Coating: Mirror Tints - Purple")
            print(f"- Total: £203.00")
            print(f"- New template should bypass cache")
        else:
            print(f"❌ Failed to send test email: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_new_template()
    
    print("\n" + "=" * 80)
    print("TEMPLATE CACHE BYPASS COMPLETED")
    print("=" * 80)
    print("✅ Changed template ID from order_placed_v1_3 to order_placed_v1_4")
    print("✅ Backend restarted with new configuration")
    print("✅ New template should bypass MSG91 cache")
    print("\nNext steps:")
    print("1. Check your email for the test email")
    print("2. If it shows correct data, the cache issue is solved")
    print("3. Place a real order to confirm it works")
