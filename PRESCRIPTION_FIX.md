# Prescription Upload Fix - Product Page to Cart

## Problem
When a user uploads a prescription on the product page (`/product/E21A8529/upload-prescription`), the prescription was not automatically visible on the cart page. The cart was still showing "Add Prescription" instead of showing the uploaded prescription.

## Solution
Modified the backend to:
1. **Store prescription temporarily** when uploaded on product page with `product_id`
2. **Automatically include prescription** when adding product to cart
3. **Clear pending prescription** after adding to cart

## Changes Made

### 1. Enhanced `/api/v1/prescriptions/upload-image` Endpoint
- Added `product_id` parameter (optional)
- When `product_id` is provided, the prescription is stored as a "pending prescription" in the user document
- Structure: `user.pending_prescriptions.{product_id} = prescription_data`

### 2. Enhanced `/api/v1/cart/add` Endpoint
- Before adding item to cart, checks for pending prescription for that `product_id`
- If found, automatically includes prescription in the cart item
- Clears the pending prescription after adding to cart

## How It Works

### Flow:
1. **User uploads prescription on product page:**
   ```
   POST /api/v1/prescriptions/upload-image
   Form Data:
   - file: <prescription_file>
   - product_id: "E21A8529"  ← NEW: Link to product
   - user_id: <user_id> (or from auth token)
   ```

2. **Backend stores as pending:**
   ```javascript
   user.pending_prescriptions = {
     "E21A8529": {
       mode: "upload",
       gcs_url: "https://...",
       fileName: "prescription.pdf",
       // ... other prescription data
     }
   }
   ```

3. **User adds product to cart:**
   ```
   POST /api/v1/cart/add
   {
     "product_id": "E21A8529",
     "product": {...},
     // prescription will be automatically added here
   }
   ```

4. **Backend automatically includes prescription:**
   - Checks `user.pending_prescriptions["E21A8529"]`
   - Adds to cart item: `data.prescription = prescription_data`
   - Clears pending prescription

5. **Cart now shows prescription:**
   - Cart item has `prescription` field populated
   - Frontend can display "Prescription Uploaded" instead of "Add Prescription"

## Frontend Integration

### Upload Prescription (Product Page)
When uploading prescription on product page, include `product_id`:

```javascript
const formData = new FormData();
formData.append('prescription_file', file);
formData.append('product_id', productSkuid); // ← ADD THIS
formData.append('user_id', userId); // or use auth token

const response = await fetch('/api/v1/prescriptions/upload-image', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}` // Optional but recommended
  },
  body: formData
});
```

### Add to Cart
No changes needed! The prescription will be automatically included:

```javascript
// Just add product to cart as usual
const response = await fetch('/api/v1/cart/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    product_id: productSkuid,
    product: productData,
    // prescription will be added automatically
  })
});
```

## Testing

1. **Upload prescription on product page:**
   ```bash
   curl -X POST http://localhost:5000/api/v1/prescriptions/upload-image \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "file=@prescription.pdf" \
     -F "product_id=E21A8529"
   ```

2. **Add product to cart:**
   ```bash
   curl -X POST http://localhost:5000/api/v1/cart/add \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "product_id": "E21A8529",
       "product": {...}
     }'
   ```

3. **Check cart:**
   ```bash
   curl http://localhost:5000/api/v1/cart \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

   The cart item should have `prescription` field populated.

## Database Structure

### User Document (pending_prescriptions)
```javascript
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "pending_prescriptions": {
    "E21A8529": {
      "mode": "upload",
      "gcs_url": "https://storage.googleapis.com/...",
      "blob_name": "prescriptions/user_id/file.pdf",
      "fileName": "prescription.pdf",
      "fileType": "application/pdf",
      "fileSize": 12345,
      "uploadedAt": "2025-12-25T10:00:00Z"
    }
  }
}
```

### Cart Item (with prescription)
```javascript
{
  "cart_id": 1234567890,
  "product_id": "E21A8529",
  "product": {...},
  "prescription": {
    "mode": "upload",
    "gcs_url": "https://storage.googleapis.com/...",
    // ... prescription data
  }
}
```

## Notes

- **Pending prescriptions are cleared** after adding to cart
- **Prescription is only stored** if user is authenticated (has user_id or valid token)
- **Multiple products** can have pending prescriptions simultaneously
- **If prescription already exists** in cart item, pending prescription won't overwrite it

## Troubleshooting

### Prescription not showing in cart?
1. Check if `product_id` was included in upload request
2. Verify user is authenticated (has valid token)
3. Check backend logs for "Found pending prescription" message
4. Verify cart item has `prescription` field in database

### Prescription not being stored?
1. Check MongoDB connection
2. Verify user document exists
3. Check backend logs for errors
4. Ensure `product_id` is provided in upload request

---

**Last Updated:** December 2025

