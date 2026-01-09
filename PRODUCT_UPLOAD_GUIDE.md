# 📦 Product Upload Guide

This guide explains how to upload new products to the Multifolks backend system.

## 🎯 Methods to Upload Products

There are **3 ways** to upload products:

1. **Using Python Script** (Recommended for single products)
2. **Using API Endpoint** (Recommended for programmatic uploads)
3. **Using CSV Import** (Recommended for bulk uploads)

---

## Method 1: Using Python Script (Easiest for Single Products)

### Step 1: Create or Edit the Script

Use the existing `create_product_entry.py` script as a template. Copy it and modify the product data:

```python
# Create a new file: upload_my_product.py
from pymongo import MongoClient

# Configuration - Update these if needed
MONGO_URI = "mongodb://localhost:27017/"  # Or your MongoDB URI
DB_NAME = "multifolks"  # Or your database name
COLLECTION_NAME = "products"

# YOUR PRODUCT DATA - Fill this in with your product information
product_data = {
    "skuid": "YOUR_SKU_ID",  # REQUIRED: Unique product SKU
    "naming_system": "YOUR_SKU_ID",  # Usually same as skuid
    "name": "Product Name",  # REQUIRED: Product display name
    "images": [
        "https://storage.googleapis.com/your-bucket/images/product1.jpg",
        "https://storage.googleapis.com/your-bucket/images/product2.jpg",
    ],
    "image": "https://storage.googleapis.com/your-bucket/images/product1.jpg",  # Main image URL
    "price": 99.99,  # REQUIRED: Product price
    "list_price": 149.99,  # Optional: Original/list price
    "description": "Product description here",
    "features": ["Feature 1", "Feature 2"],  # Array of features
    "colors": ["#FF0000", "#0000FF"],  # Color codes
    "color_names": ["Red", "Blue"],  # Color names
    "framecolor": "Black",  # Frame color
    "variants": [],  # Product variants (if any)
    "sizes": [],  # Available sizes
    "brand": "Brand Name",
    "gender": "Unisex",  # Options: "Men", "Women", "Unisex", "Kids"
    "material": "Acetate",  # Frame material
    "shape": "Round",  # Frame shape
    "style": "Full Frame",  # Options: "Full Frame", "Half Frame", "Rimless"
    "is_active": True  # Set to False to hide product
}

# Run the script
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

result = collection.update_one(
    {"skuid": product_data["skuid"]},
    {"$set": product_data},
    upsert=True  # Creates new if doesn't exist, updates if exists
)

if result.upserted_id:
    print(f"✅ Created new product: {product_data['skuid']}")
else:
    print(f"✅ Updated existing product: {product_data['skuid']}")

client.close()
```

### Step 2: Run the Script

```bash
python upload_my_product.py
```

---

## Method 2: Using API Endpoint (Best for Programmatic Uploads)

### Endpoint: `POST /api/v1/products/create`

### Authentication Required: Yes (Bearer Token)

### Request Body Example:

```json
{
  "skuid": "PROD001",
  "name": "Classic Black Frames",
  "naming_system": "PROD001",
  "brand": "Multifolks",
  "price": 99.99,
  "list_price": 149.99,
  "description": "Stylish black frames perfect for everyday wear",
  "image": "https://storage.googleapis.com/bucket/images/prod001.jpg",
  "images": [
    "https://storage.googleapis.com/bucket/images/prod001_1.jpg",
    "https://storage.googleapis.com/bucket/images/prod001_2.jpg"
  ],
  "colors": ["#000000"],
  "color_names": ["Black"],
  "framecolor": "Black",
  "style": "Full Frame",
  "gender": "Unisex",
  "size": "Medium",
  "material": "Acetate",
  "shape": "Round",
  "features": ["UV Protection", "Lightweight"],
  "variants": [],
  "sizes": ["Small", "Medium", "Large"],
  "is_active": true
}
```

### cURL Example:

```bash
curl -X POST http://localhost:8000/api/v1/products/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "skuid": "PROD001",
    "name": "Classic Black Frames",
    "price": 99.99,
    "image": "https://example.com/image.jpg"
  }'
```

### Response:

```json
{
  "success": true,
  "message": "Product created successfully",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "skuid": "PROD001",
    "name": "Classic Black Frames",
    ...
  }
}
```

---

## Method 3: Using CSV Import (Best for Bulk Uploads)

### Step 1: Prepare CSV File

Create a CSV file named `mapped_products.csv` with the following columns:

| skuid | name | naming_system | brand | price | list_price | image | images | colors | color_names | framecolor | style | gender | size | material | shape | description | features |
|-------|------|---------------|-------|-------|------------|-------|--------|--------|-------------|------------|-------|--------|------|----------|-------|-------------|----------|
| PROD001 | Classic Frames | PROD001 | Brand1 | 99.99 | 149.99 | url1 | url1,url2 | #000 | Black | Full Frame | Unisex | Medium | Acetate | Round | Description | Feature1\|Feature2 |

**Notes:**
- `images`: Comma-separated URLs
- `colors`: Comma-separated color codes
- `color_names`: Comma-separated color names
- `features`: Pipe-separated (`|`) features

### Step 2: Run Import Script

```bash
python import_products.py
```

The script will:
- Read from `mapped_products.csv`
- Insert products in batches of 100
- Show progress and final count

---

## 📋 Complete Product Schema Reference

### Required Fields:
- `skuid` (string): Unique product identifier
- `name` (string): Product display name
- `price` (number): Product price

### Optional Fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `naming_system` | string | Product naming code | "PROD001" |
| `brand` | string | Brand name | "Ray-Ban" |
| `list_price` | number | Original/list price | 149.99 |
| `description` | string | Product description | "Stylish frames..." |
| `image` | string | Main image URL | "https://..." |
| `images` | array | Array of image URLs | ["url1", "url2"] |
| `colors` | array | Color codes | ["#000000", "#FFFFFF"] |
| `color_names` | array | Color names | ["Black", "White"] |
| `framecolor` | string | Frame color | "Black" |
| `style` | string | Frame style | "Full Frame", "Half Frame", "Rimless" |
| `gender` | string | Target gender | "Men", "Women", "Unisex", "Kids" |
| `size` | string | Product size | "Small", "Medium", "Large" |
| `material` | string | Frame material | "Acetate", "Metal", "Plastic" |
| `shape` | string | Frame shape | "Round", "Square", "Aviator" |
| `features` | array | Product features | ["UV Protection", "Lightweight"] |
| `variants` | array | Product variants | [] |
| `sizes` | array | Available sizes | ["S", "M", "L"] |
| `is_active` | boolean | Product visibility | true/false |
| `primary_category` | string | Primary category | "Eyeglasses" |
| `secondary_category` | string | Secondary category | "Sunglasses" |
| `comfort` | array | Comfort features | ["Lightweight", "Flexible"] |

---

## 🖼️ Image Upload to Google Cloud Storage

If you need to upload images to GCS first, see `GCS_UPLOAD_GUIDE.md` for instructions.

**Quick Steps:**
1. Upload images to your GCS bucket
2. Get the public URLs
3. Use those URLs in the `image` and `images` fields

---

## ✅ Verification

After uploading, verify your product:

### Using API:
```bash
# Get product by SKU
curl http://localhost:8000/api/v1/products/sku/YOUR_SKU_ID

# Get all products
curl http://localhost:8000/api/v1/products
```

### Using MongoDB:
```javascript
// Connect to MongoDB
use multifolks
db.products.findOne({skuid: "YOUR_SKU_ID"})
```

---

## 🐛 Troubleshooting

### Product not showing up?
- Check `is_active` is set to `true`
- Verify the product exists: `GET /api/v1/products/sku/YOUR_SKU_ID`
- Check MongoDB connection

### Image not loading?
- Verify image URLs are publicly accessible
- Check GCS bucket permissions
- Ensure URLs are complete (include `https://`)

### Price not displaying?
- Ensure `price` field is a number (not string)
- Check for negative values

### Duplicate SKU?
- The system uses `upsert` - it will update existing products with the same SKU
- To create a new product, use a different SKU

---

## 📞 Need Help?

- Check existing products: `GET /api/v1/products`
- View product details: `GET /api/v1/products/sku/{sku}`
- Check database connection: `GET /api/health`

---

## 🎯 Quick Start Example

**Fastest way to add ONE product:**

1. Copy `create_product_entry.py` to `upload_product.py`
2. Edit the `product_data` dictionary with your product info
3. Run: `python upload_product.py`
4. Done! ✅

**Example minimal product:**
```python
product_data = {
    "skuid": "MYPROD001",
    "name": "My Product",
    "price": 50.00,
    "image": "https://example.com/image.jpg",
    "is_active": True
}
```

