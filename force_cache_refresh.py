#!/usr/bin/env python3
"""
Force MSG91 template cache refresh by making a template change
"""
import requests
import json

def force_cache_refresh():
    """
    Force MSG91 to clear template cache by making a tiny template change
    """
    print("=" * 80)
    print("FORCING MSG91 TEMPLATE CACHE REFRESH")
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
    
    # Test with minimal change to force cache refresh
    payload = {
        "recipients": [{
            "to": [{
                "name": "Cache Refresh Test",
                "email": test_email
            }],
            "variables": {
                "NAME": "Cache Refresh Test",
                "ORDER_NUMBER": "REFRESH-001",
                "ORDER_DATE": "26/02/2026",
                "order_total": "£0.01",
                "shipping_cost": "£0.00",
                "cart": []
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
        print(f"Sending cache refresh test...")
        print(f"Template ID: {TEMPLATE_ID}")
        print(f"This tiny change should force MSG91 to clear template cache")
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"✅ Cache refresh sent successfully!")
            print(f"Unique ID: {response_data.get('data', {}).get('unique_id', 'N/A')}")
            print(f"\nThis should force MSG91 to clear the template cache")
            print(f"Your order confirmation emails should now use the updated template")
        else:
            print(f"❌ Failed to send cache refresh: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("1. Check your email in 2-3 minutes")
    print("2. If still old template, try again")
    print("3. If still old template, contact MSG91 support")
    print("4. The cache refresh should clear the old template content")
    print("\nThis forces MSG91 to treat the template as 'updated' and clear any cached content")

if __name__ == "__main__":
    force_cache_refresh()
