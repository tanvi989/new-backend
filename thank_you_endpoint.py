# Add this endpoint to app.py after the other order endpoints

@app.get("/api/v1/orders/thank-you/{order_id}")
async def get_thank_you_page_data(order_id: str):
    """
    Get order data for thank you page (public - no auth required for Stripe redirect)
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
        
        # Format response to match frontend expectations
        return {
            "status": True,
            "payment_status": "Success" if order.get("payment_status") == "paid" else "Pending",
            "order": order,
            "shipping_address": order.get("shipping_address", ""),
            "billing_address": order.get("billing_address", "")
        }
    except Exception as e:
        print(f"Error fetching thank you data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch order data")
