#!/usr/bin/env python3
"""
Test what variables are actually sent for order confirmation
"""
import requests
import json

def test_order_variables():
    print("=" * 80)
    print("TESTING ORDER CONFIRMATION VARIABLES")
    print("=" * 80)
    
    # MSG91 Configuration
    AUTH_KEY = "482085AD1VnJzkrUX6937ff86P1"
    DOMAIN = "email.multifolks.com"
    TEMPLATE_ID = "order_placed_23"
    
    test_email = "paradkartanvii@gmail.com"
    url = "https://control.msg91.com/api/v5/email/send"
    
    headers = {
        "authkey": AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    # Test with simple variables first
    payload = {
        "recipients": [{
            "to": [{
                "name": "Test Customer",
                "email": test_email
            }],
            "variables": {
                "NAME": "Test Customer",
                "order_id": "TEST-123",
                "ORDER_ID": "TEST-123",
                "order_total": "99.99",
                "ORDER_TOTAL": "99.99",
                "orderDate": "26 Feb 2026",
                "shippingCost": "4.99",
                "orderItems": [
                    {
                        "name": "Test Product 1",
                        "quantity": 1,
                        "price": "£49.99"
                    },
                    {
                        "name": "Test Product 2", 
                        "quantity": 2,
                        "price": "£24.99"
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
        print(f"Sending test with orderItems array...")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Test email sent successfully!")
            print(f"Unique ID: {response_data.get('data', {}).get('unique_id', 'N/A')}")
            print(f"\nCheck your email for:")
            print(f"- Order ID: TEST-123")
            print(f"- Items should appear if template uses {{#each orderItems}}")
            print(f"- If items don't appear, template might be using different variable name")
        else:
            print(f"Failed to send test email: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_order_variables()
    
    print("\n" + "=" * 80)
    print("CORRECTED TEMPLATE VARIABLES")
    print("=" * 80)
    print("Backend sends: orderItems (array)")
    print("Template should use: {{#each orderItems}}")
    print("Available variables per item:")
    print("- name")
    print("- quantity") 
    print("- price")
    print("\nUpdate your template to use:")
    print("{{#each orderItems}}")
    print("  {{name}} (Qty: {{quantity}})")
    print("  {{price}}")
    print("{{/each}}")
