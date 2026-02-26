# MSG91 Template Cache Refresh Fix

## Problem
MSG91 is still showing cached template content even though backend is sending correct data.

## Solution: Force Cache Refresh

### Step 1: Go to MSG91 Dashboard
1. Go to: https://control.msg91.com/
2. Navigate: Email → Templates
3. Find template: `order_placed_v1_3`
4. Click 'Edit'

### Step 2: Make Tiny Change to Force Cache Refresh
In the template editor, find this line:
```html
<title>Order Confirmed — Multifolks</title>
```

Change it to:
```html
<title>Order Confirmed — Multifolks </title>
```
(Just add a space at the end)

### Step 3: Save Template
Click 'Save' to save the template.

### Step 4: Wait 2-3 Minutes
MSG91 cache should clear within 2-3 minutes.

### Step 5: Test
Place a new order to test if the updated template content is now showing.

## Why This Works
MSG91 treats any template change as "content update" and clears the cache, forcing the new template content to be used immediately.

## Expected Result
After this change, your order confirmation emails should show:
- BERG (E45A8506)
- Sunglasses • Sunglasses Tint • 1.61
- Coating: Mirror Tints - Purple
- Total: £248.00
- All product details correctly

This is the fastest way to force MSG91 to clear the template cache and use your updated template content.
