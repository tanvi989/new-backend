#!/usr/bin/env python3
"""
Compare email data structure between admin and backend
"""

print("COMPARING EMAIL DATA STRUCTURES")
print("=" * 60)

print("\n1. ADMIN (Next.js) sends this data:")
print("=" * 40)
admin_data = """
{
  "variables": {
    "name": "Test Customer",
    "NAME": "Test Customer", 
    "ORDER_NUMBER": "TEST-001",
    "ORDER_DATE": "26/02/2026",
    "order_total": "£183.00",
    "shipping_cost": "4.99",
    "status": "Processing",
    "cart": [
      {
        "product_id": "MF001",
        "name": "Multifolks Premium Glasses",
        "quantity": 1,
        "lens": {
          "main_category": "Eyewear",
          "lensCategoryDisplay": "Progressive Glasses", 
          "lensIndex": "1.67 High Index",
          "coating": "Anti-Reflective Premium"
        }
      }
    ]
  }
}
"""

print(admin_data)

print("\n2. BACKEND (Python) sends this data:")
print("=" * 40)
backend_data = """
{
  "variables": {
    "NAME": "Test Customer",
    "order_id": "TEST-001",
    "ORDER_ID": "TEST-001", 
    "ORDER_NUMBER": "TEST-001",
    "order_total": "£183.00",
    "ORDER_TOTAL": "£183.00",
    "shipping_cost": "£4.99",
    "orderItems": [  # DIFFERENT KEY!
      {
        "name": "Test Multifocal Glasses",
        "quantity": 1,
        "price": "£89.00",
        "product_id": "MF001"
      }
    ]
  }
}
"""

print(backend_data)

print("\n3. KEY DIFFERENCES:")
print("=" * 40)
print("ADMIN uses: {{#each cart}}")
print("BACKEND uses: {{#each orderItems}}")
print("")
print("ADMIN sends: lens.main_category, lens.lensCategoryDisplay, lens.lensIndex")
print("BACKEND sends: name, quantity, price, product_id (no lens details)")
print("")
print("ADMIN sends: ORDER_DATE")
print("BACKEND sends: created (but not ORDER_DATE)")

print("\n4. SOLUTION:")
print("=" * 40)
print("Option 1: Update backend to send same data as admin")
print("Option 2: Update template to use orderItems instead of cart")
print("Option 3: Add lens details to backend orderItems")

print("\n5. CURRENT BACKEND NOTIFICATION_SERVICE.PY:")
print("=" * 40)
backend_notification = """
# Line 221-242 in notification_service.py
items_for_template = []
if order_items:
    for it in order_items:
        qty = int(it.get("quantity", 1))
        price_str = str(it.get("price", "£0.00"))
        item_row = {
            "name": str(it.get("name", "Item")),
            "quantity": qty,
            "price": price_str,
        }
        items_for_template.append(item_row)
variables["orderItems"] = items_for_template
"""

print(backend_notification)

print("\n6. MISSING DATA IN BACKEND:")
print("=" * 40)
print("❌ No lens details (main_category, lensCategoryDisplay, lensIndex)")
print("❌ No coating information")
print("❌ No tint information")
print("❌ No ORDER_DATE variable")
print("❌ Uses 'orderItems' instead of 'cart'")

print("\n7. RECOMMENDED FIX:")
print("=" * 40)
print("Update notification_service.py to include lens details:")
print("""
item_row = {
    "name": str(it.get("name", "Item")),
    "quantity": qty,
    "price": price_str,
    "product_id": str(it.get("product_id", "")),
    "lens": {
        "main_category": it.get("lens", {}).get("main_category", "Eyewear"),
        "lensCategoryDisplay": it.get("lens", {}).get("lensCategoryDisplay", "Glasses"),
        "lensIndex": it.get("lens", {}).get("lensIndex", "Standard"),
        "coating": it.get("lens", {}).get("coating", "Standard"),
        "tint_type": it.get("lens", {}).get("tint_type", ""),
        "tint_color": it.get("lens", {}).get("tint_color", "")
    }
}

# Also add ORDER_DATE
variables["ORDER_DATE"] = order_date.strftime("%d/%m/%Y") if order_date else datetime.now().strftime("%d/%m/%Y")
""")
