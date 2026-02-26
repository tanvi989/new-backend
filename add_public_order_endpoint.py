#!/usr/bin/env python3
"""
Add public order details endpoint to app.py
"""

# Add this endpoint after the existing order endpoints
PUBLIC_ORDER_ENDPOINT_CODE = '''
# Add public order details endpoint (no auth required)
@app.get("/api/v1/public/orders/{order_id}")
async def get_public_order_details(order_id: str):
    """
    Get order details for public access (no authentication required)
    For use in order details pages, thank you pages, etc.
    """
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    try:
        orders_collection = db['orders']
        order = orders_collection.find_one({"order_id": order_id})
        
        if not order:
            return {"status": False, "message": "Order not found"}
        
        # Convert ObjectId to string
        order["_id"] = str(order["_id"])
        
        # Return order data (same as authenticated endpoint but without auth requirement)
        return {
            "status": True,
            "data": {
                "order_id": order.get("order_id"),
                "user_id": str(order.get("user_id", "")),
                "payment_status": order.get("payment_status", ""),
                "order_status": order.get("order_status", ""),
                "created": str(order.get("created", "")),
                "email": order.get("email", ""),
                "total": order.get("total", ""),
                "subtotal": order.get("subtotal", ""),
                "shipping_cost": order.get("shipping_cost", ""),
                "discount_amount": order.get("discount_amount", ""),
                "customer_details": order.get("customer_details", {}),
                "cart": order.get("cart", [])
            }
        }
        
    except Exception as e:
        print(f"Error fetching public order details: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch order")

print("Add this endpoint to app.py after the existing order endpoints:")
print("1. Place this code after line 47 in order_endpoints.py")
print("2. This allows frontend to get order details without authentication")
print("3. Update frontend to use: GET /api/v1/public/orders/{order_id}")
print("4. All variables from authenticated endpoint will be available")
'''

if __name__ == "__main__":
    print("Public Order Endpoint Generator")
    print("=" * 50)
    print("This creates a public order details endpoint")
    print("Copy the code above and add to app.py")
    print("Then update frontend to use the new public endpoint")
    print("=" * 50)
    print(PUBLIC_ORDER_ENDPOINT_CODE)
