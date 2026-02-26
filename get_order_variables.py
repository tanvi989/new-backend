#!/usr/bin/env python3
"""
Get order details and show all available variables for email template
"""
import requests
import json

def get_order_details(order_id):
    """
    Fetch order details from backend API
    """
    backend_url = "http://localhost:5000"
    
    try:
        # Get order details (no auth required for this endpoint)
        response = requests.get(f"{backend_url}/api/v1/orders/{order_id}")
        
        if response.status_code == 200:
            order_data = response.json()
            return order_data
        else:
            print(f"Failed to fetch order: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error fetching order: {e}")
        return None

def display_order_variables(order_data):
    """
    Display all available variables from order data
    """
    if not order_data:
        print("No order data available")
        return
    
    print("=" * 80)
    print("ORDER DETAILS AND VARIABLES")
    print("=" * 80)
    
    print(f"Order ID: {order_data.get('order_id', 'N/A')}")
    print(f"User ID: {order_data.get('user_id', 'N/A')}")
    print(f"Payment Status: {order_data.get('payment_status', 'N/A')}")
    print(f"Order Status: {order_data.get('order_status', 'N/A')}")
    print(f"Created: {order_data.get('created', 'N/A')}")
    print(f"Email: {order_data.get('email', 'N/A')}")
    
    # Customer details
    customer = order_data.get('customer_details', {})
    print(f"\nCustomer Details:")
    print(f"  Name: {customer.get('firstName', '')} {customer.get('lastName', '')}")
    print(f"  Email: {customer.get('email', '')}")
    print(f"  Phone: {customer.get('phone', '')}")
    
    # Shipping address
    shipping = order_data.get('shipping_address', {})
    print(f"\nShipping Address:")
    print(f"  {shipping.get('address_line1', '')}")
    print(f"  {shipping.get('address_line2', '')}")
    print(f"  {shipping.get('address_line3', '')}")
    print(f"  {shipping.get('city', '')}, {shipping.get('state', '')} {shipping.get('pincode', '')}")
    
    # Order items
    cart_items = order_data.get('cart', [])
    print(f"\nOrder Items ({len(cart_items)} items):")
    
    for idx, item in enumerate(cart_items, 1):
        print(f"\n  Item {idx}:")
        print(f"    Product ID: {item.get('product_id', 'N/A')}")
        print(f"    Name: {item.get('name', 'N/A')}")
        print(f"    Quantity: {item.get('quantity', 'N/A')}")
        print(f"    Price: {item.get('price', 'N/A')}")
        
        # Lens details
        lens = item.get('lens', {})
        if lens:
            print(f"    Lens Category: {lens.get('main_category', 'N/A')}")
            print(f"    Lens Type: {lens.get('lensCategoryDisplay', 'N/A')}")
            print(f"    Lens Index: {lens.get('lensIndex', 'N/A')}")
            print(f"    Coating: {lens.get('coating', 'N/A')}")
            
            if lens.get('tint_color'):
                print(f"    Tint: {lens.get('tint_type', 'N/A')} - {lens.get('tint_color', 'N/A')}")
    
    # Pricing
    print(f"\nPricing:")
    print(f"  Subtotal: {order_data.get('subtotal', 'N/A')}")
    print(f"  Shipping Cost: {order_data.get('shipping_cost', 'N/A')}")
    print(f"  Discount: {order_data.get('discount_amount', 'N/A')}")
    print(f"  Total: {order_data.get('total', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("EMAIL TEMPLATE VARIABLES")
    print("=" * 80)
    print("Use these variables in your MSG91 template:")
    print("\nBasic Order Info:")
    print("  {{order_id}} or {{ORDER_ID}}")
    print("  {{payment_status}}")
    print("  {{order_status}}")
    print("  {{created}}")
    print("  {{email}}")
    print("  {{subtotal}}")
    print("  {{shipping_cost}}")
    print("  {{discount_amount}}")
    print("  {{total}}")
    
    print("\nCustomer Info:")
    print("  {{firstName}} or {{NAME}}")
    print("  {{lastName}}")
    print("  {{customer_details.firstName}}")
    print("  {{customer_details.email}}")
    print("  {{customer_details.phone}}")
    
    print("\nShipping Address:")
    print("  {{shipping_address.address_line1}}")
    print("  {{shipping_address.city}}")
    print("  {{shipping_address.state}}")
    print("  {{shipping_address.pincode}}")
    
    print("\nOrder Items Loop:")
    print("  {{#each cart}} or {{#each orderItems}}")
    print("    {{product_id}}")
    print("    {{name}}")
    print("    {{quantity}}")
    print("    {{price}}")
    print("    {{lens.main_category}}")
    print("    {{lens.lensCategoryDisplay}}")
    print("    {{lens.lensIndex}}")
    print("    {{lens.coating}}")
    print("    {{lens.tint_type}}")
    print("    {{lens.tint_color}}")
    print("  {{/each}}")

def main():
    print("Order Details Variable Extractor")
    print("=" * 50)
    
    # Get order ID from user input or use a test one
    test_order_id = input("Enter Order ID (or press Enter for test): ").strip()
    
    if not test_order_id:
        test_order_id = "TEST-123"  # Use a test order ID
    
    print(f"\nFetching order details for: {test_order_id}")
    
    # Fetch order data
    order_data = get_order_details(test_order_id)
    
    if order_data:
        display_order_variables(order_data)
        
        # Save to file for reference
        with open(f"order_{test_order_id}_variables.json", "w") as f:
            json.dump(order_data, f, indent=2)
        print(f"\nOrder data saved to: order_{test_order_id}_variables.json")
    else:
        print("Failed to fetch order details")

if __name__ == "__main__":
    main()
