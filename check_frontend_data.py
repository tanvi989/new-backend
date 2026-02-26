#!/usr/bin/env python3
"""
Check how frontend gets order data from backend
"""
import requests
import json

def check_order_details_endpoint():
    """
    Check the order details endpoint
    """
    backend_url = "http://localhost:5000"
    frontend_url = "http://localhost:3001"
    
    print("=" * 80)
    print("CHECKING ORDER DETAILS ENDPOINTS")
    print("=" * 80)
    
    # Test order ID
    test_order_id = "TEST-123"
    
    print(f"Backend endpoint: {backend_url}/api/v1/orders/{test_order_id}")
    print(f"Frontend page: {frontend_url}/order-details")
    
    try:
        # Check backend endpoint
        print("\n1. Testing backend endpoint...")
        backend_response = requests.get(f"{backend_url}/api/v1/orders/{test_order_id}")
        
        if backend_response.status_code == 200:
            backend_data = backend_response.json()
            print(f"✅ Backend response status: {backend_response.status_code}")
            print(f"Backend data keys: {list(backend_data.keys())}")
            
            # Check what variables backend sends
            if 'customer_details' in backend_data:
                customer = backend_data['customer_details']
                print(f"✅ Customer details found:")
                print(f"   Name: {customer.get('firstName', '')} {customer.get('lastName', '')}")
                print(f"   Email: {customer.get('email', '')}")
                print(f"   Phone: {customer.get('phone', '')}")
            
            if 'cart' in backend_data:
                cart_items = backend_data['cart']
                print(f"\u2705 Cart items found: {len(cart_items)} items")
                for idx, item in enumerate(cart_items):
                    print(f"   Item {idx}: {item.get('name', '')} (Qty: {item.get('quantity', '')})")
        else:
            print(f"Backend returned: {backend_response.text}")
            
    except Exception as e:
        print(f"\u274C Error checking backend: {e}")
    
    # Check frontend page (simulate what frontend might be doing)
    print(f"\n2. Checking frontend page access...")
    print(f"   Frontend might be making GET request to: {backend_url}/api/v1/orders/{test_order_id}")
    
    # Common frontend patterns for getting order data
    frontend_patterns = [
        f"GET {backend_url}/api/v1/orders/{test_order_id}",
        f"GET {backend_url}/api/v1/orders?order_id={test_order_id}",
        f"POST {backend_url}/api/v1/orders/details",
        f"POST {backend_url}/api/v1/order-details"
    ]
    
    for i, pattern in enumerate(frontend_patterns, 1):
        print(f"   Pattern {i}: {pattern}")
    
    print(f"\n3. Available variables from backend:")
    print("   Based on backend code, these should be available:")
    print("   - ORDER_NUMBER or order_id")
    print("   - ORDER_DATE or created")
    print("   - order_total or total")
    print("   - shipping_cost")
    print("   - NAME or firstName")
    print("   - customer_details.firstName")
    print("   - customer_details.email")
    print("   - cart (array of items)")
    print("   - For each item: name, quantity, price")
    print("   - For each item: product_id, lens.main_category, lens.lensCategoryDisplay, lens.lensIndex, lens.coating, lens.tint_type, lens.tint_color")

if __name__ == "__main__":
    check_order_details_endpoint()
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print("For frontend order-details page:")
    print("1. Use: GET /api/v1/orders/{order_id}")
    print("2. Display all available variables")
    print("3. Use {{#each cart}} or {{#each orderItems}} for product loop")
    print("4. Make sure to handle missing data gracefully")
    print("\nFor MSG91 template:")
    print("1. Use {{ORDER_NUMBER}} for order ID")
    print("2. Use {{ORDER_DATE}} for order date")
    print("3. Use {{order_total}} for total amount")
    print("4. Use {{NAME}} for customer name")
    print("5. Use {{#each cart}} for product items")
