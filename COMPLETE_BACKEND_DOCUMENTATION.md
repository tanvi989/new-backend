# 📚 Complete Multifolks Backend Documentation

**Version:** 1.0  
**Last Updated:** 2025  
**Framework:** FastAPI (Python)  
**Database:** MongoDB

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [API Endpoints](#api-endpoints)
3. [Service Files](#service-files)
4. [Utility Scripts](#utility-scripts)
5. [Configuration Files](#configuration-files)
6. [Database Schema](#database-schema)
7. [Authentication](#authentication)
8. [Error Handling](#error-handling)

---

## 🎯 Overview

The Multifolks backend is a FastAPI-based REST API that handles:
- User authentication and registration
- Product catalog management
- Shopping cart operations
- Order processing
- Payment integration (Stripe)
- Delivery/shipping (BlueDart)
- Prescription management
- Email notifications (MSG91)

**Base URL:** `http://localhost:8000` (or configured host/port)

---

## 🔌 API Endpoints

### 🔐 Authentication Endpoints

#### 1. **POST** `/api/v1/auth/login`
Login with email and password.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "status": 200,
  "msg": "Welcome back! You are successfully logged in",
  "data": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "user@example.com",
    "mobile": "+447123456789",
    "mobile_international": "+447123456789",
    "is_verified": true,
    "refer_code": "ABC123",
    "id": "507f1f77bcf86cd799439011",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "is_new_user": false
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid credentials
- `403`: Account deactivated
- `503`: Database unavailable

---

#### 2. **POST** `/api/v1/auth/simple-register`
#### 3. **POST** `/api/v1/auth/unified`
#### 4. **POST** `/api/v1/auth/auth`
Register a new user (multiple routes supported).

**Request Body (Form Data or JSON):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "user@example.com",  // Optional, auto-generated if not provided
  "mobile": "+447123456789",     // Required
  "password": "password123",     // Required
  "country_code": "44",
  "is_subscribed_whatsapp": true,
  "otp": "0000"  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "status": 2019,
  "msg": "Registration successful",
  "data": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "user@example.com",
    "mobile": "+447123456789",
    "mobile_international": "+447123456789",
    "is_verified": false,
    "refer_code": "",
    "id": "507f1f77bcf86cd799439011",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "is_new_user": true
  }
}
```

**Status Codes:**
- `201`: Success
- `400`: Missing fields, invalid mobile, or account exists
- `503`: Database unavailable

---

#### 5. **POST** `/api/v1/auth/request-pin`
Request a 6-digit PIN for PIN-based login.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "msg": "PIN sent successfully"
}
```

**Status Codes:**
- `200`: Success (always returns success for security)
- `503`: Database unavailable

---

#### 6. **POST** `/api/v1/auth/login-with-pin`
Login using PIN instead of password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "pin": "123456"
}
```

**Response:** Same as login endpoint

**Status Codes:**
- `200`: Success
- `400`: Invalid PIN or expired
- `503`: Database unavailable

---

#### 7. **POST** `/api/v1/auth/forgot-password`
Request password reset PIN.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "msg": "Reset instructions sent successfully"
}
```

**Status Codes:**
- `200`: Success
- `500`: Failed to generate reset code
- `503`: Database unavailable

---

#### 8. **POST** `/api/v1/auth/reset-password`
Reset password using PIN.

**Request Body:**
```json
{
  "email": "user@example.com",
  "pin": "123456",
  "new_password": "newpassword123"
}
```

**Response:**
```json
{
  "success": true,
  "msg": "Password reset successfully. Please login."
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid PIN or expired
- `503`: Database unavailable

---

#### 9. **GET** `/api/v1/accounts/check-email`
Check if email is registered.

**Query Parameters:**
- `email` (required): Email address to check

**Response:**
```json
{
  "success": true,
  "data": {
    "is_registered": true
  }
}
```

---

### 👤 User Profile Endpoints

#### 10. **GET** `/api/profile`
Get current user's profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "507f1f77bcf86cd799439011",
    "first_name": "John",
    "last_name": "Doe",
    "email": "user@example.com",
    "contact_number": "7123456789",
    "mobile": "7123456789",
    "mobile_international": "+447123456789",
    "is_verified": true,
    "country_code": 44,
    "birth_date": "15",
    "birth_month": "06",
    "birth_year": "1990",
    "gender": "Male",
    "billing_address": "123 Main St, London",
    "shipping_address": "123 Main St, London"
  }
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `503`: Database unavailable

---

#### 11. **PUT** `/api/v1/user/profile`
Update user profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "mobile": "+447123456789",
  "country_code": 44,
  "gender": "Male",
  "birth_date": "15",
  "birth_month": "06",
  "birth_year": "1990",
  "billing_address": "123 Main St, London",
  "shipping_address": "123 Main St, London",
  "email": "newemail@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "msg": "Profile updated successfully",
  "data": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "newemail@example.com",
    "mobile": "7123456789",
    "mobile_international": "+447123456789",
    "country_code": 44
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid mobile number
- `401`: Unauthorized
- `500`: Update failed

---

### 📦 Product Endpoints

#### 12. **GET** `/api/v1/products`
Get products with filtering and pagination.

**Query Parameters:**
- `page` (default: 1): Page number
- `limit` (default: 20): Items per page
- `category`: Filter by primary category
- `brand`: Filter by brand
- `gender`: Filter by gender (Men, Women, Unisex, Kids)
- `search`: Search in name, SKU, brand, naming_system
- `material`: Filter by material
- `style`: Filter by style (Full Frame, Half Frame, Rimless)
- `comfort`: Filter by comfort features
- `size`: Filter by size
- `min_price`: Minimum price
- `max_price`: Maximum price
- `frame_color`: Filter by frame color
- `shape`: Filter by shape

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "skuid": "PROD001",
      "name": "Classic Black Frames",
      "brand": "Multifolks",
      "price": 99.99,
      "list_price": 149.99,
      "image": "https://example.com/image.jpg",
      "images": ["https://example.com/image1.jpg"],
      "description": "Stylish frames",
      "gender": "Unisex",
      "material": "Acetate",
      "style": "Full Frame",
      "shape": "Round",
      "is_active": true
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

**Status Codes:**
- `200`: Success
- `503`: Database unavailable

---

#### 13. **GET** `/api/v1/products/{product_id}`
Get product by MongoDB ObjectId.

**Path Parameters:**
- `product_id`: MongoDB ObjectId

**Response:**
```json
{
  "success": true,
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "skuid": "PROD001",
    "name": "Classic Black Frames",
    ...
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid product ID
- `404`: Product not found
- `503`: Database unavailable

---

#### 14. **GET** `/api/v1/products/sku/{sku}`
Get product by SKU.

**Path Parameters:**
- `sku`: Product SKU

**Response:** Same as above

**Status Codes:**
- `200`: Success
- `404`: Product not found
- `503`: Database unavailable

---

#### 15. **POST** `/api/v1/products/create`
Create or update a product (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "skuid": "PROD001",
  "name": "Classic Black Frames",
  "naming_system": "PROD001",
  "brand": "Multifolks",
  "price": 99.99,
  "list_price": 149.99,
  "description": "Stylish frames",
  "image": "https://example.com/image.jpg",
  "images": ["https://example.com/image1.jpg"],
  "colors": ["#000000"],
  "color_names": ["Black"],
  "framecolor": "Black",
  "style": "Full Frame",
  "gender": "Unisex",
  "size": "Medium",
  "material": "Acetate",
  "shape": "Round",
  "features": ["UV Protection"],
  "variants": [],
  "sizes": ["Small", "Medium", "Large"],
  "primary_category": "Eyeglasses",
  "secondary_category": "Prescription Glasses",
  "comfort": ["Lightweight"],
  "is_active": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Product created successfully",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "skuid": "PROD001",
    ...
  }
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `500`: Creation failed
- `503`: Database unavailable

---

#### 16. **GET** `/api/v1/products/all`
Get all products with advanced filtering (uses ProductService).

**Query Parameters:**
- `gender`: Filter by gender
- `price_min`: Minimum price
- `price_max`: Maximum price
- `shape`: Array of shapes
- `colors`: Array of colors
- `material`: Array of materials
- `collections`: Array of collections
- `comfort`: Array of comfort features
- `size`: Array of sizes
- `brand`: Array of brands
- `style`: Array of styles
- `limit`: Limit results

**Response:** Similar to `/api/v1/products`

---

#### 17. **GET** `/api/v1/public/products`
Public endpoint for products (no authentication required).

**Query Parameters:** Same as `/api/v1/products`

---

#### 18. **GET** `/retailer/product-inventory`
Retailer-specific product inventory endpoint.

**Query Parameters:** Same as `/api/v1/products`

---

#### 19. **GET** `/api/v1/products/filters/options`
Get all available filter options.

**Response:**
```json
{
  "success": true,
  "data": {
    "brands": ["Brand1", "Brand2"],
    "genders": ["Men", "Women", "Unisex"],
    "materials": ["Acetate", "Metal"],
    "styles": ["Full Frame", "Half Frame"],
    "sizes": ["Small", "Medium", "Large"],
    "frame_colors": ["Black", "Brown"],
    "comfort": ["Lightweight", "Flexible"],
    "price_range": {
      "min": 0,
      "max": 500
    }
  }
}
```

---

#### 20. **GET** `/api/v1/products/recently-viewed`
Get user's recently viewed products.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": ["PROD001", "PROD002"]
}
```

---

#### 21. **POST** `/api/v1/products/recently-viewed`
Add product to recently viewed.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "product_id": "PROD001"
}
```

**Response:**
```json
{
  "success": true,
  "msg": "Added to recently viewed"
}
```

---

### 🛒 Cart Endpoints

#### 22. **GET** `/api/v1/cart`
Get user's cart summary.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "cart": [
    {
      "cart_id": 1,
      "product_id": "PROD001",
      "name": "Classic Black Frames",
      "image": "https://example.com/image.jpg",
      "price": 99.99,
      "quantity": 1,
      "total_price": 99.99,
      "product": {
        "products": {
          "skuid": "PROD001",
          "name": "Classic Black Frames",
          ...
        }
      },
      "lens": {
        "type": "Single Vision",
        "selling_price": 50.00,
        ...
      },
      "prescription": {
        "mode": "upload",
        "gcs_url": "https://storage.googleapis.com/...",
        ...
      }
    }
  ],
  "subtotal": 149.99,
  "discount_amount": 10.00,
  "shipping_cost": 5.00,
  "total": 144.99,
  "coupon": {
    "code": "SAVE10",
    "discount": 10.00
  },
  "shipping_method": {
    "id": "standard",
    "name": "Standard Shipping",
    "cost": 5.00
  }
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `503`: Cart service unavailable

---

#### 23. **POST** `/api/v1/cart/add`
Add item to cart.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "product_id": "PROD001",
  "name": "Classic Black Frames",
  "image": "https://example.com/image.jpg",
  "price": 99.99,
  "quantity": 1,
  "product": {
    "products": {
      "skuid": "PROD001",
      ...
    }
  },
  "lens": {
    "type": "Single Vision",
    "selling_price": 50.00,
    ...
  },
  "prescription": {
    "mode": "upload",
    "gcs_url": "https://storage.googleapis.com/...",
    ...
  },
  "flag": "normal"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Item added to cart",
  "cart_id": 1
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid data
- `401`: Unauthorized
- `503`: Cart service unavailable

---

#### 24. **PUT** `/api/v1/cart/quantity`
Update item quantity.

**Query Parameters:**
- `cart_id` (required): Cart item ID
- `quantity` (required): New quantity (min: 1)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Quantity updated"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid quantity
- `401`: Unauthorized
- `404`: Cart item not found
- `503`: Cart service unavailable

---

#### 25. **DELETE** `/api/v1/cart/item/{cart_id}`
Remove item from cart.

**Path Parameters:**
- `cart_id`: Cart item ID

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Item removed from cart"
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `404`: Cart item not found
- `503`: Cart service unavailable

---

#### 26. **DELETE** `/api/v1/cart/clear`
Clear entire cart.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Cart cleared"
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `503`: Cart service unavailable

---

#### 27. **POST** `/api/v1/cart/coupon`
Apply coupon code.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "code": "SAVE10"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Coupon applied",
  "discount": 10.00
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid coupon
- `401`: Unauthorized
- `503`: Cart service unavailable

---

#### 28. **DELETE** `/api/v1/cart/coupon`
Remove coupon from cart.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Coupon removed"
}
```

---

#### 29. **PUT** `/api/v1/cart/shipping`
Update shipping method.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "method_id": "standard"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Shipping method updated"
}
```

---

#### 30. **PUT** `/api/v1/cart/lens`
Update lens configuration for cart item.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "cart_id": 1,
  "lens_data": {
    "type": "Progressive",
    "selling_price": 100.00,
    ...
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Lens updated"
}
```

---

#### 31. **PUT** `/api/v1/cart/prescription`
Update prescription for cart item.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Form Data:**
- `cart_id` (required): Cart item ID
- `mode` (required): "upload" or "manual"
- `prescription_file` (if mode="upload"): File to upload
- `prescription_data` (if mode="manual"): JSON string with prescription details

**Response:**
```json
{
  "success": true,
  "message": "Prescription updated",
  "gcs_url": "https://storage.googleapis.com/..." // if uploaded
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid mode or missing data
- `401`: Unauthorized
- `500`: Upload failed
- `503`: Cart service unavailable

---

#### 32. **POST** `/api/v1/cart/merge-guest-cart`
Merge guest cart into authenticated user's cart after login.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "guest_id": "guest_12345"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully merged 3 items",
  "items_merged": 3
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `500`: Merge failed
- `503`: Cart service unavailable

---

### 📋 Prescription Endpoints

#### 33. **GET** `/api/v1/user/prescriptions`
Get all saved prescriptions for user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "type": "upload",
      "data": {},
      "name": "My Prescription",
      "image_url": "https://storage.googleapis.com/...",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `503`: Database unavailable

---

#### 34. **POST** `/api/v1/user/prescriptions`
Save a new prescription.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "type": "upload",
  "data": {},
  "name": "My Prescription",
  "image_url": "https://storage.googleapis.com/..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Prescription saved successfully",
  "data": {
    "type": "upload",
    "data": {},
    "name": "My Prescription",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `500`: Save failed
- `503`: Database unavailable

---

#### 35. **POST** `/api/v1/prescriptions/upload-image`
Upload prescription image to Google Cloud Storage.

**Form Data:**
- `file` (required): Image/PDF file
- `user_id` (optional): User ID
- `guest_id` (optional): Guest ID
- `product_id` (optional): Link prescription to product

**Response:**
```json
{
  "success": true,
  "url": "https://storage.googleapis.com/myapp-image-bucket-001/prescriptions/...",
  "filename": "20250101_123456_abc123.jpg",
  "path": "prescriptions/user123/20250101_123456_abc123.jpg",
  "message": "Prescription uploaded and will be included when adding to cart"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid file type or empty file
- `500`: Upload failed
- `503`: GCS unavailable

---

### 📦 Order Endpoints

#### 36. **POST** `/api/v1/orders`
Create a new order.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "cart_items": [
    {
      "cart_id": 1,
      "product_id": "PROD001",
      "quantity": 1,
      "total_price": 149.99,
      ...
    }
  ],
  "payment_data": {
    "pay_mode": "Stripe / Online",
    "payment_status": "Success",
    "transaction_id": "txn_xxx",
    "payment_intent_id": "pi_xxx",
    "is_partial": false
  },
  "shipping_address": "123 Main St, London, UK",
  "billing_address": "123 Main St, London, UK",
  "metadata": {}
}
```

**Response:**
```json
{
  "success": true,
  "order_id": "ORD-1765891114486",
  "message": "Order created successfully",
  "order": {
    "order_id": "ORD-1765891114486",
    "user_id": "507f1f77bcf86cd799439011",
    "status": "confirmed",
    "items": [...],
    "total": 144.99,
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `500`: Order creation failed
- `503`: Order service unavailable

---

#### 37. **GET** `/api/v1/orders`
Get all orders for authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "orders": [
    {
      "order_id": "ORD-1765891114486",
      "status": "confirmed",
      "total": 144.99,
      "created_at": "2025-01-01T00:00:00Z",
      ...
    }
  ]
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `500`: Fetch failed
- `503`: Order service unavailable

---

#### 38. **GET** `/api/v1/orders/{order_id}`
Get order details by ID.

**Path Parameters:**
- `order_id`: Order ID

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "order": {
    "order_id": "ORD-1765891114486",
    "user_id": "507f1f77bcf86cd799439011",
    "status": "confirmed",
    "items": [...],
    "payment": {...},
    "shipping_address": "123 Main St, London",
    "billing_address": "123 Main St, London",
    "total": 144.99,
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `404`: Order not found
- `500`: Fetch failed
- `503`: Order service unavailable

---

#### 39. **GET** `/api/v1/orders/thank-you/{order_id}`
Get order data for thank you page.

**Path Parameters:**
- `order_id`: Order ID

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "status": true,
  "order": {...},
  "shipping_address": "123 Main St, London",
  "billing_address": "123 Main St, London"
}
```

**Status Codes:**
- `200`: Success
- `401`: Unauthorized
- `404`: Order not found
- `503`: Order service unavailable

---

### 💳 Payment Endpoints

#### 40. **POST** `/api/v1/payment/create-session`
Create Stripe checkout session and pending order.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "order_id": "ORD-1765891114486",
  "amount": 144.99,
  "currency": "GBP",
  "metadata": {
    "address": "{\"addressLine\":\"123 Main St\",\"city\":\"London\",\"zip\":\"SW1A 1AA\",\"country\":\"UK\"}",
    "customer_id": "507f1f77bcf86cd799439011"
  }
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "cs_test_xxx",
  "payment_url": "https://checkout.stripe.com/pay/cs_test_xxx",
  "order_id": "ORD-1765891114486"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request
- `401`: Unauthorized
- `500`: Session creation failed
- `503`: Payment service unavailable

---

#### 41. **POST** `/api/v1/payment/webhook`
Stripe webhook endpoint (no authentication).

**Headers:**
```
stripe-signature: <signature>
```

**Request Body:** Raw Stripe event payload

**Response:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid payload or signature
- `503`: Payment service unavailable

---

### 🚚 Delivery Endpoints

#### 42. **POST** `/api/v1/delivery/check-pincode`
Check if pincode is serviceable.

**Request Body:**
```json
{
  "pincode": "122001"
}
```

**Response:**
```json
{
  "success": true,
  "serviceable": true,
  "message": "Serviceable"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid pincode
- `503`: Delivery service unavailable

---

#### 43. **POST** `/api/v1/delivery/create-shipment`
Create shipment for order.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "order_id": "ORD-1765891114486",
  "customer_details": {
    "name": "John Doe",
    "address": "123 Main St",
    "city": "London",
    "pincode": "SW1A 1AA",
    "phone": "+447123456789"
  }
}
```

**Response:**
```json
{
  "success": true,
  "awb_number": "BD123456789",
  "shipment_id": "SHIP123"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid data
- `401`: Unauthorized
- `500`: Shipment creation failed
- `503`: Delivery service unavailable

---

#### 44. **GET** `/api/v1/delivery/track/{awb_number}`
Track shipment by AWB number.

**Path Parameters:**
- `awb_number`: BlueDart AWB number

**Response:**
```json
{
  "success": true,
  "status": "SHIPMENT IN TRANSIT",
  "status_code": 72,
  "tracking_history": [
    {
      "status": "SHIPMENT PICKED UP",
      "date": "2025-01-01T00:00:00Z",
      "location": "Warehouse"
    }
  ]
}
```

**Status Codes:**
- `200`: Success
- `404`: AWB not found
- `503`: Delivery service unavailable

---

### 🏥 Health & Debug Endpoints

#### 45. **GET** `/api/health`
#### 46. **GET** `/health`
Health check endpoint.

**Response:**
```json
{
  "success": true,
  "message": "API is running",
  "mongodb": "connected",
  "total_users": 1000,
  "timestamp": "2025-01-01T00:00:00Z"
}
```

**Status Codes:**
- `200`: Success

---

#### 47. **GET** `/api/v1/auth/debug/reset-status/{email}`
Debug endpoint for password reset status (remove in production).

**Path Parameters:**
- `email`: Email address

**Response:**
```json
{
  "found": true,
  "has_reset_pin": true,
  "has_reset_expiry": true,
  "pin_expired": false,
  "fields": ["_id", "email", "reset_pin", ...]
}
```

---

## 📁 Service Files

### Core Services

#### `app.py`
**Purpose:** Main FastAPI application file containing all API endpoints and route handlers.

**Key Components:**
- FastAPI app initialization
- CORS middleware configuration
- Request logging middleware
- Database connection setup
- Service initialization (Payment, Cart, Order, Delivery, Notification, Product)
- All API endpoint definitions
- Authentication and authorization logic
- JWT token generation and verification

**Dependencies:**
- FastAPI
- MongoDB (PyMongo)
- JWT (PyJWT)
- Passlib (password hashing)
- Google Cloud Storage

---

#### `cart_service.py`
**Purpose:** Shopping cart management service.

**Key Methods:**
- `get_cart(user_id)`: Get user's cart with all items
- `get_cart_summary(user_id)`: Get cart summary with totals, discounts, shipping
- `add_to_cart(user_id, item_data)`: Add item to cart
- `update_quantity(user_id, cart_id, quantity)`: Update item quantity
- `remove_item(user_id, cart_id)`: Remove item from cart
- `clear_cart(user_id)`: Clear entire cart
- `apply_coupon(user_id, code)`: Apply coupon code
- `remove_coupon(user_id)`: Remove coupon
- `update_shipping_method(user_id, method_id)`: Update shipping method
- `update_lens(user_id, cart_id, lens_data)`: Update lens configuration
- `update_prescription(user_id, cart_id, prescription_data)`: Update prescription

**Database Collection:** `cart`

**Features:**
- Automatic cart ID generation
- Price calculations (frame + lens + tint + coating)
- Discount calculations
- Shipping cost calculations (free shipping over £75)
- Coupon validation and application

---

#### `order_service.py`
**Purpose:** Order management service.

**Key Methods:**
- `create_order(...)`: Create new order from cart items
- `get_user_orders(user_id)`: Get all orders for user
- `get_order_by_id(order_id, user_id)`: Get specific order details
- `update_order_status(order_id, status)`: Update order status
- `_generate_order_id()`: Generate unique order ID (ORD-{timestamp})

**Database Collection:** `orders`

**Features:**
- Order ID generation
- Order status tracking
- Payment integration
- Shipping address management
- Discount and shipping cost tracking

---

#### `payment_service.py`
**Purpose:** Stripe payment integration service.

**Key Methods:**
- `create_checkout_session(...)`: Create Stripe checkout session
- `confirm_payment(session_id)`: Confirm payment after webhook
- `refund_payment(payment_id, amount)`: Process refunds
- `get_payment_status(payment_id)`: Get payment status

**Database Collections:** `payments`, `orders`

**Features:**
- Stripe Checkout integration
- Webhook handling
- Payment confirmation
- Refund processing
- Payment status tracking

---

#### `delivery_service.py`
**Purpose:** BlueDart courier integration service.

**Key Classes:**
- `BlueDartService`: BlueDart API integration
- `DeliveryService`: High-level delivery management

**Key Methods:**
- `check_pincode_serviceability(pincode)`: Check if pincode is serviceable
- `create_shipment(order_id, customer_details)`: Create shipment
- `get_shipment_status(awb_number)`: Track shipment
- `cancel_shipment(awb_number)`: Cancel shipment

**Features:**
- BlueDart API integration
- Pincode serviceability check
- Shipment creation
- Real-time tracking
- Status mapping (BlueDart → Internal status codes)

---

#### `product_service.py`
**Purpose:** Product catalog service with advanced filtering.

**Key Methods:**
- `get_all_products(filters)`: Get products with filters
- `construct_image_url(skuid, position)`: Construct CDN image URLs
- `get_product_by_sku(sku)`: Get product by SKU

**Database Collection:** `products`

**Features:**
- Advanced filtering (gender, price, shape, colors, material, etc.)
- Image URL construction
- Pagination support
- CDN integration

---

#### `notification_service.py`
**Purpose:** MSG91 email notification service.

**Key Methods:**
- `send_email(to_email, template_id, variables)`: Send email via MSG91
- `send_welcome_email(email, name, password)`: Send welcome email
- `send_order_confirmation(email, order_id, total, name)`: Send order confirmation
- `send_password_reset_pin(email, pin, name)`: Send password reset PIN
- `send_login_pin(email, pin, name)`: Send login PIN

**Features:**
- MSG91 API integration
- Template-based emails
- Welcome emails
- Order confirmations
- Password reset emails
- Login PIN emails

---

#### `prescription_gcs_service.py`
**Purpose:** Google Cloud Storage service for prescription uploads.

**Key Methods:**
- `upload_prescription_to_gcs(file, user_id, cart_id, filename)`: Upload prescription to GCS
- `delete_prescription_from_gcs(blob_name)`: Delete prescription from GCS
- `get_prescription_url(blob_name)`: Get public URL for prescription

**Features:**
- GCS integration
- Prescription file uploads
- Public URL generation
- File validation

---

### Utility Scripts

#### `create_product_entry.py`
**Purpose:** Script to create/update a single product entry in MongoDB.

**Usage:**
```bash
python create_product_entry.py
```

**Features:**
- Creates or updates product by SKU
- Validates product data
- Prints product summary

---

#### `import_products.py`
**Purpose:** Bulk import products from CSV file.

**Usage:**
```bash
python import_products.py
```

**Features:**
- Reads from `mapped_products.csv`
- Batch inserts (100 products at a time)
- Progress tracking
- Product count summary

---

#### `upload_product_template.py`
**Purpose:** Template script for easy product uploads.

**Usage:**
1. Edit `product_data` dictionary
2. Run: `python upload_product_template.py`

**Features:**
- User-friendly template
- Field validation
- Success/error messages
- Product verification

---

#### `check_db.py`
**Purpose:** Database connection and collection checker.

**Usage:**
```bash
python check_db.py
```

**Features:**
- Tests MongoDB connection
- Lists all collections
- Shows collection counts

---

#### `check_orders_db.py`
**Purpose:** Check orders collection and order data.

**Usage:**
```bash
python check_orders_db.py
```

**Features:**
- Lists all orders
- Shows order details
- Order count summary

---

#### `check_prescriptions.py`
**Purpose:** Check user prescriptions in database.

**Usage:**
```bash
python check_prescriptions.py
```

**Features:**
- Lists user prescriptions
- Shows prescription details
- Validates prescription data

---

#### `check_product_prices.py`
**Purpose:** Check product prices in database.

**Usage:**
```bash
python check_product_prices.py
```

**Features:**
- Lists products with prices
- Price validation
- Price range summary

---

#### `debug_cart_manual.py`
**Purpose:** Manual cart debugging script.

**Usage:**
```bash
python debug_cart_manual.py
```

**Features:**
- Cart data inspection
- Cart item validation
- Price calculation debugging

---

#### `debug_product_price.py`
**Purpose:** Debug product price calculations.

**Usage:**
```bash
python debug_product_price.py
```

**Features:**
- Product price inspection
- Price calculation validation
- Price comparison

---

#### `debug_msg91.py`
**Purpose:** Test MSG91 email integration.

**Usage:**
```bash
python debug_msg91.py
```

**Features:**
- Test email sending
- Template validation
- API response debugging

---

#### `test_registration.py`
**Purpose:** Test user registration flow.

**Usage:**
```bash
python test_registration.py
```

**Features:**
- Registration testing
- Email validation
- Mobile validation

---

#### `test_gcs_upload.py`
**Purpose:** Test Google Cloud Storage uploads.

**Usage:**
```bash
python test_gcs_upload.py
```

**Features:**
- GCS connection testing
- File upload testing
- URL generation testing

---

#### `test_webhook.py`
**Purpose:** Test Stripe webhook handling.

**Usage:**
```bash
python test_webhook.py
```

**Features:**
- Webhook simulation
- Event handling testing
- Payment confirmation testing

---

#### `create_test_order.py`
**Purpose:** Create test orders for development.

**Usage:**
```bash
python create_test_order.py
```

**Features:**
- Test order creation
- Order data validation
- Order status testing

---

#### `fix_all_product_images.py`
**Purpose:** Fix product image URLs in database.

**Usage:**
```bash
python fix_all_product_images.py
```

**Features:**
- Batch image URL updates
- Image URL validation
- CDN URL construction

---

#### `update_product_images.py`
**Purpose:** Update product images from local files to GCS.

**Usage:**
```bash
python update_product_images.py
```

**Features:**
- Local to GCS upload
- Image URL updates
- Batch processing

---

#### `fix_db_prices.py`
**Purpose:** Fix product prices in database.

**Usage:**
```bash
python fix_db_prices.py
```

**Features:**
- Price updates
- Price validation
- Batch price fixes

---

#### `fix_faceaface_images.py`
**Purpose:** Fix face-to-face product images.

**Usage:**
```bash
python fix_faceaface_images.py
```

**Features:**
- Image URL fixes
- Face-to-face product handling

---

#### `get_item_details.py`
**Purpose:** Get detailed item information.

**Usage:**
```bash
python get_item_details.py
```

**Features:**
- Item data retrieval
- Product details inspection

---

#### `list_collections.py`
**Purpose:** List all MongoDB collections.

**Usage:**
```bash
python list_collections.py
```

**Features:**
- Collection listing
- Collection count summary

---

#### `manual_insert_order.py`
**Purpose:** Manually insert order into database.

**Usage:**
```bash
python manual_insert_order.py
```

**Features:**
- Manual order creation
- Order data validation
- Database insertion

---

#### `repro_registration.py`
**Purpose:** Reproduce registration issues.

**Usage:**
```bash
python repro_registration.py
```

**Features:**
- Registration flow testing
- Issue reproduction
- Debug logging

---

#### `verify_msg91_templates.py`
**Purpose:** Verify MSG91 email templates.

**Usage:**
```bash
python verify_msg91_templates.py
```

**Features:**
- Template validation
- Template variable checking
- API response verification

---

#### `verify_prescription_lens_data.py`
**Purpose:** Verify prescription and lens data.

**Usage:**
```bash
python verify_prescription_lens_data.py
```

**Features:**
- Prescription validation
- Lens data validation
- Data integrity checking

---

### Configuration & Deployment Files

#### `config.py` (Not in repo - must be created)
**Purpose:** Application configuration file.

**Required Variables:**
```python
MONGO_URI = "mongodb://localhost:27017/"  # MongoDB connection string
DATABASE_NAME = "multifolks"  # Database name
COLLECTION_NAME = "accounts_login"  # Users collection name
SECRET_KEY = "your-secret-key"  # JWT secret key
HOST = "0.0.0.0"  # Server host
PORT = 5000  # Server port
STRIPE_SECRET_KEY = "sk_test_..."  # Stripe secret key
STRIPE_WEBHOOK_SECRET = "whsec_..."  # Stripe webhook secret
MSG91_AUTH_KEY = "your-auth-key"  # MSG91 auth key
MSG91_DOMAIN = "your-domain"  # MSG91 domain
MSG91_SENDER_EMAIL = "noreply@example.com"  # Sender email
MSG91_SENDER_NAME = "Multifolks"  # Sender name
BLUEDART_BASE_URL = "https://netconnect.bluedart.com/Ver1.10/"
BLUEDART_CUSTOMER_CODE = "940553"
BLUEDART_LOGIN_ID = "GG940553"
BLUEDART_LICENSE_KEY = "your-license-key"
WAREHOUSE_PINCODE = "122001"
WAREHOUSE_ADDRESS = {...}
```

---

#### `requirements.txt`
**Purpose:** Python dependencies list.

**Key Dependencies:**
- fastapi
- uvicorn
- pymongo
- pyjwt
- passlib
- python-dotenv
- stripe
- google-cloud-storage
- requests

---

#### `start_server.py`
**Purpose:** Server startup script.

**Usage:**
```bash
python start_server.py
```

**Features:**
- Server initialization
- Environment setup
- Logging configuration

---

#### `run.bat`
**Purpose:** Windows batch file to run server.

**Usage:**
```bash
run.bat
```

---

#### `start_backend.sh`
**Purpose:** Linux/Mac shell script to start backend.

**Usage:**
```bash
bash start_backend.sh
```

---

#### `restart_backend.sh`
**Purpose:** Restart backend server script.

**Usage:**
```bash
bash restart_backend.sh
```

---

#### `deploy.sh`
**Purpose:** Deployment script.

**Usage:**
```bash
bash deploy.sh
```

**Features:**
- Server deployment
- Service restart
- Health checks

---

#### `multifolks-backend.service`
**Purpose:** Systemd service file for Linux.

**Usage:**
```bash
sudo systemctl enable multifolks-backend.service
sudo systemctl start multifolks-backend.service
```

---

#### `nginx-config.conf`
**Purpose:** Nginx configuration for reverse proxy.

**Usage:**
Copy to `/etc/nginx/sites-available/` and enable.

**Features:**
- Reverse proxy configuration
- SSL termination
- Load balancing

---

### Documentation Files

#### `README.md`
**Purpose:** Main project README with setup instructions.

---

#### `PRODUCT_UPLOAD_GUIDE.md`
**Purpose:** Guide for uploading products.

**Contents:**
- Product upload methods
- API endpoint usage
- Script usage
- Product schema reference

---

#### `GCS_UPLOAD_GUIDE.md`
**Purpose:** Guide for Google Cloud Storage uploads.

**Contents:**
- GCS setup
- Upload instructions
- URL generation
- File management

---

#### `GCS_UPLOAD_INSTRUCTIONS.md`
**Purpose:** Detailed GCS upload instructions.

---

#### `SETUP_GUIDE.md`
**Purpose:** Setup and installation guide.

---

#### `QUICK_START.md`
**Purpose:** Quick start guide.

---

#### `VPS_DEPLOYMENT_GUIDE.md`
**Purpose:** VPS deployment instructions.

---

#### `VPS_QUICK_START.md`
**Purpose:** Quick VPS deployment guide.

---

#### `PRESCRIPTION_FIX.md`
**Purpose:** Prescription system fixes and notes.

---

### Data Files

#### `mapped_products.csv`
**Purpose:** CSV file for bulk product import.

**Format:**
- Columns: skuid, name, naming_system, brand, price, list_price, image, images, colors, color_names, framecolor, style, gender, size, material, shape, description, features

---

#### `product_example.json`
**Purpose:** Example product JSON for reference.

---

#### `output.json`
**Purpose:** Output file for various scripts.

---

#### `cart_dump.txt`
**Purpose:** Cart data dump for debugging.

---

#### `prescription_endpoints.txt`
**Purpose:** Prescription endpoint documentation.

---

## 🗄️ Database Schema

### Collections

#### `accounts_login` (Users)
```javascript
{
  "_id": ObjectId("..."),
  "firstName": "John",
  "lastName": "Doe",
  "email": "user@example.com",
  "primaryContact": 7123456789,
  "international_mobile": "+447123456789",
  "password": "hashed_password",
  "country_code": 44,
  "is_verified": false,
  "is_active": true,
  "is_staff": false,
  "is_superuser": false,
  "gender": "Male",
  "birthDate": "15",
  "birthMonth": "06",
  "birthYear": "1990",
  "billing_address": "123 Main St, London",
  "shipping_address": "123 Main St, London",
  "prescriptions": [...],
  "pending_prescriptions": {...},
  "recently_viewed": ["PROD001", "PROD002"],
  "pin": "123456",
  "pin_expiry": ISODate("..."),
  "reset_pin": "123456",
  "reset_pin_expiry": ISODate("..."),
  "updateTime": ISODate("..."),
  "date_joined": ISODate("..."),
  "last_login": ISODate("...")
}
```

---

#### `products`
```javascript
{
  "_id": ObjectId("..."),
  "skuid": "PROD001",
  "naming_system": "PROD001",
  "name": "Classic Black Frames",
  "brand": "Multifolks",
  "price": 99.99,
  "list_price": 149.99,
  "description": "Stylish frames",
  "image": "https://example.com/image.jpg",
  "images": ["https://example.com/image1.jpg"],
  "colors": ["#000000"],
  "color_names": ["Black"],
  "framecolor": "Black",
  "style": "Full Frame",
  "gender": "Unisex",
  "size": "Medium",
  "material": "Acetate",
  "shape": "Round",
  "features": ["UV Protection"],
  "variants": [],
  "sizes": ["Small", "Medium", "Large"],
  "primary_category": "Eyeglasses",
  "secondary_category": "Prescription Glasses",
  "comfort": ["Lightweight"],
  "is_active": true
}
```

---

#### `cart`
```javascript
{
  "_id": ObjectId("..."),
  "user_id": "507f1f77bcf86cd799439011",
  "items": [
    {
      "cart_id": 1,
      "product_id": "PROD001",
      "name": "Classic Black Frames",
      "image": "https://example.com/image.jpg",
      "price": 99.99,
      "quantity": 1,
      "total_price": 149.99,
      "product": {
        "products": {
          "skuid": "PROD001",
          "name": "Classic Black Frames",
          ...
        }
      },
      "lens": {
        "type": "Single Vision",
        "selling_price": 50.00,
        "tint_price": 0.00,
        "coating_price": 0.00
      },
      "prescription": {
        "mode": "upload",
        "gcs_url": "https://storage.googleapis.com/...",
        ...
      },
      "flag": "normal"
    }
  ],
  "coupon": {
    "code": "SAVE10",
    "discount": 10.00
  },
  "shipping_method": {
    "id": "standard",
    "name": "Standard Shipping",
    "cost": 5.00
  },
  "updated_at": ISODate("...")
}
```

---

#### `orders`
```javascript
{
  "_id": ObjectId("..."),
  "order_id": "ORD-1765891114486",
  "user_id": "507f1f77bcf86cd799439011",
  "user_email": "user@example.com",
  "status": "confirmed",
  "items": [...],
  "payment": {
    "pay_mode": "Stripe / Online",
    "payment_status": "Success",
    "transaction_id": "txn_xxx",
    "payment_intent_id": "pi_xxx",
    "is_partial": false
  },
  "shipping_address": "123 Main St, London, UK",
  "billing_address": "123 Main St, London, UK",
  "subtotal": 149.99,
  "discount_amount": 10.00,
  "shipping_cost": 5.00,
  "total": 144.99,
  "metadata": {},
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

---

#### `payments`
```javascript
{
  "_id": ObjectId("..."),
  "session_id": "cs_test_xxx",
  "order_id": "ORD-1765891114486",
  "user_id": "507f1f77bcf86cd799439011",
  "amount": 144.99,
  "currency": "GBP",
  "status": "completed",
  "payment_intent_id": "pi_xxx",
  "transaction_id": "txn_xxx",
  "created_at": ISODate("..."),
  "completed_at": ISODate("...")
}
```

---

## 🔐 Authentication

### JWT Token Structure

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "user_id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "exp": 1735689600,
  "iat": 1735603200
}
```

**Token Expiry:** 24 hours

---

### Authentication Flow

1. **Registration/Login:**
   - User provides credentials
   - Server validates and generates JWT token
   - Token returned to client

2. **Protected Endpoints:**
   - Client sends token in `Authorization: Bearer <token>` header
   - Server verifies token
   - Server extracts user data from token
   - Request processed with user context

3. **Guest Access:**
   - Some endpoints support `X-Guest-ID` header
   - Guest ID used for cart operations
   - No authentication required

---

## ⚠️ Error Handling

### Standard Error Response Format

```json
{
  "success": false,
  "status": 4001,
  "msg": "Error message",
  "detail": "Detailed error information"
}
```

### Common Status Codes

- `200`: Success
- `400`: Bad Request (validation errors, invalid data)
- `401`: Unauthorized (missing/invalid token)
- `403`: Forbidden (account deactivated)
- `404`: Not Found (resource doesn't exist)
- `500`: Internal Server Error
- `503`: Service Unavailable (database/service down)

### Error Categories

1. **Authentication Errors:**
   - `4001`: Invalid username or password
   - `4002`: Account deactivated
   - `4003`: Account already exists
   - `4004`: Invalid UK mobile number
   - `4005`: Invalid OTP

2. **Validation Errors:**
   - Missing required fields
   - Invalid data format
   - Invalid email/mobile format

3. **Service Errors:**
   - Database unavailable
   - External service unavailable
   - Payment processing failed

---

## 📝 Notes

- All timestamps are in UTC (ISO 8601 format)
- Prices are in GBP (British Pounds)
- Mobile numbers are validated for UK format (+44 or 07XXXXXXXXX)
- Product images are stored in Google Cloud Storage
- Prescriptions are uploaded to GCS bucket: `myapp-image-bucket-001`
- Stripe webhook secret must be configured for payment confirmation
- MSG91 credentials required for email notifications
- BlueDart credentials required for shipping

---

## 🔗 External Services

1. **MongoDB Atlas:** Database hosting
2. **Stripe:** Payment processing
3. **Google Cloud Storage:** File storage (prescriptions, images)
4. **MSG91:** Email notifications
5. **BlueDart:** Shipping and delivery

---

## 📞 Support

For issues or questions:
1. Check logs in console output
2. Review error messages in API responses
3. Check database connection status via `/api/health`
4. Verify external service configurations

---

**End of Documentation**

