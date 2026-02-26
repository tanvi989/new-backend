#!/usr/bin/env python3
"""
Test what variables are actually sent in order confirmation email
"""
import requests
import json

def test_order_email_variables():
    """
    Test order confirmation email with all variables
    """
    print("=" * 80)
    print("TESTING ORDER EMAIL VARIABLES")
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
    
    # Test with orderItems (what backend sends)
    payload = {
        "recipients": [{
            "to": [{
                "name": "Test Customer",
                "email": test_email
            }],
            "variables": {
                "NAME": "Test Customer",
                "ORDER_NUMBER": "TEST-789",
                "ORDER_DATE": "26 Feb 2026",
                "order_total": "£183.00",
                "shipping_cost": "£4.99",
                "orderItems": [
                    {
                        "name": "Test Multifocal Glasses",
                        "quantity": 1,
                        "price": "£89.00",
                        "product_id": "MF001"
                    },
                    {
                        "name": "Test Reading Glasses", 
                        "quantity": 2,
                        "price": "£44.50",
                        "product_id": "MF002"
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
        print(f"Sending test email with orderItems...")
        print(f"Variables being sent:")
        print(f"- NAME: {payload['recipients'][0]['variables']['NAME']}")
        print(f"- ORDER_NUMBER: {payload['recipients'][0]['variables']['ORDER_NUMBER']}")
        print(f"- ORDER_DATE: {payload['recipients'][0]['variables']['ORDER_DATE']}")
        print(f"- order_total: {payload['recipients'][0]['variables']['order_total']}")
        print(f"- shipping_cost: {payload['recipients'][0]['variables']['shipping_cost']}")
        print(f"- orderItems: {len(payload['recipients'][0]['variables']['orderItems'])} items")
        
        for i, item in enumerate(payload['recipients'][0]['variables']['orderItems']):
            print(f"  Item {i+1}: {item['name']} (Qty: {item['quantity']}, Price: {item['price']})")
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Test email sent successfully!")
            print(f"Unique ID: {response_data.get('data', {}).get('unique_id', 'N/A')}")
            print(f"\nCheck your email for:")
            print(f"- Order ID: TEST-789")
            print(f"- Customer name: Test Customer")
            print(f"- 2 items should appear if template uses {{#each orderItems}}")
            print(f"- If items don't appear, template might be using {{#each cart}}")
        else:
            print(f"Failed to send test email: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

def show_correct_template_syntax():
    """
    Show the correct template syntax
    """
    print("\n" + "=" * 80)
    print("CORRECT TEMPLATE SYNTAX")
    print("=" * 80)
    print("Your template should use:")
    print("{{#each orderItems}}")
    print("  {{name}} ({{product_id}})")
    print("  {{lens.main_category}} • {{lens.lensCategoryDisplay}} • {{lens.lensIndex}}")
    print("  Coating: {{lens.coating}}")
    print("  {{#if lens.tint_color}}")
    print("    Tint: {{lens.tint_type}} - {{lens.tint_color}}")
    print("  {{/if}}")
    print("  Qty: {{quantity}}")
    print("{{/each}}")
    print("\nNOT:")
    print("{{#each cart}}")
    print("  {{name}} ({{product_id}})")
    print("  ...")
    print("{{/each}}")
    print("\nThe backend sends 'orderItems', not 'cart'!")

if __name__ == "__main__":
    test_order_email_variables()
    show_correct_template_syntax()
