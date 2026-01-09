"""
Order Management Endpoints for Multifolks API
Add these endpoints to app.py before the if __name__ == "__main__" block
"""

from fastapi import HTTPException, Depends
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel

# ---------- ORDER ENDPOINTS ----------
@app.get("/api/v1/orders")
async def get_user_orders(
    current_user: dict = Depends(verify_token),
    page: int = 1,
    limit: int = 10,
    status: Optional[str] = None
):
    """Get all orders for the logged-in user"""
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    try:
        orders_collection = db['orders']
        user_id = str(current_user['_id'])
        
        query = {"user_id": user_id}
        if status:
            query["order_status"] = status
        
        total = orders_collection.count_documents(query)
        orders = list(orders_collection.find(query).sort("created_at", -1).skip((page - 1) * limit).limit(limit))
        
        for order in orders:
            order["_id"] = str(order["_id"])
        
        return {
            "success": True,
            "data": orders,
            "pagination": {"page": page, "limit": limit, "total": total, "pages": (total + limit - 1) // limit}
        }
    except Exception as e:
        print(f"Error fetching orders: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch orders")

@app.get("/api/v1/orders/{order_id}")
async def get_order_details(order_id: str, current_user: dict = Depends(verify_token)):
    """Get specific order details"""
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    try:
        orders_collection = db['orders']
        order = orders_collection.find_one({"order_id": order_id, "user_id": str(current_user['_id'])})
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order["_id"] = str(order["_id"])
        return {"success": True, "data": order}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching order: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch order")

# ---------- ADMIN ORDER ENDPOINTS ----------
@app.get("/api/v1/admin/orders")
async def get_all_orders(
    current_user: dict = Depends(verify_token),
    page: int = 1,
    limit: int = 20,
    status: Optional[str] = None,
    search: Optional[str] = None
):
    """Get all orders (admin only)"""
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    if not current_user.get("is_staff") and not current_user.get("is_superuser"):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        orders_collection = db['orders']
        query = {}
        if status:
            query["order_status"] = status
        if search:
            query["$or"] = [
                {"order_id": {"$regex": search, "$options": "i"}},
                {"user_email": {"$regex": search, "$options": "i"}},
                {"user_name": {"$regex": search, "$options": "i"}}
            ]
        
        total = orders_collection.count_documents(query)
        orders = list(orders_collection.find(query).sort("created_at", -1).skip((page - 1) * limit).limit(limit))
        
        for order in orders:
            order["_id"] = str(order["_id"])
        
        return {
            "success": True,
            "data": orders,
            "pagination": {"page": page, "limit": limit, "total": total, "pages": (total + limit - 1) // limit}
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching orders: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch orders")

class UpdateOrderStatusRequest(BaseModel):
    status: str
    tracking_number: Optional[str] = None
    notes: Optional[str] = None

@app.put("/api/v1/admin/orders/{order_id}/status")
async def update_order_status(order_id: str, request: UpdateOrderStatusRequest, current_user: dict = Depends(verify_token)):
    """Update order status (admin only)"""
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    if not current_user.get("is_staff") and not current_user.get("is_superuser"):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        orders_collection = db['orders']
        update_data = {"order_status": request.status, "updated_at": datetime.now(timezone.utc)}
        
        if request.tracking_number:
            update_data["tracking_number"] = request.tracking_number
        if request.notes:
            update_data["admin_notes"] = request.notes
        
        result = orders_collection.update_one({"order_id": order_id}, {"$set": update_data})
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order = orders_collection.find_one({"order_id": order_id})
        order["_id"] = str(order["_id"])
        
        return {"success": True, "message": "Order status updated", "data": order}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating order: {e}")
        raise HTTPException(status_code=500, detail="Failed to update order")
