#!/usr/bin/env python3
"""
Debug why the order confirmation email is empty
"""

def debug_empty_email():
    """
    Debug the empty email issue
    """
    print("=" * 80)
    print("DEBUGGING EMPTY ORDER CONFIRMATION EMAIL")
    print("=" * 80)
    
    print("\n1. CURRENT BACKEND DATA STRUCTURE:")
    print("=" * 40)
    print("Backend sends:")
    print("{")
    print("  variables: {")
    print("    NAME: 'Customer',")
    print("    ORDER_NUMBER: 'E45A8506',")
    print("    ORDER_DATE: '26/02/2026',")
    print("    order_total: '£193.00',")
    print("    shipping_cost: '£0.00',")
    print("    orderItems: [")
    print("      {")
    print("        name: 'BERG',")
    print("        quantity: 1,")
    print("        price: '£193.00'")
    print("      }")
    print("    ]")
    print("  }")
    print("}")
    
    print("\n2. TEMPLATE EXPECTS:")
    print("=" * 40)
    print("Template uses:")
    print("{{#each cart}} or {{#each orderItems}}")
    print("  {{name}} ({{product_id}})")
    print("  {{lens.main_category}} • {{lens.lensCategoryDisplay}} • {{lens.lensIndex}}")
    print("  {{lens.coating}}")
    print("  {{#if lens.tint_color}}")
    print("    Tint: {{lens.tint_type}} - {{lens.tint_color}}")
    print("  {{/if}}")
    print("  Qty: {{quantity}}")
    print("{{/each}}")
    
    print("\n3. THE PROBLEM:")
    print("=" * 40)
    print("❌ Backend sends: name, quantity, price")
    print("❌ Template expects: name, product_id, lens details")
    print("❌ Missing: product_id, lens.main_category, lens.lensCategoryDisplay, etc.")
    print("❌ Template loop shows nothing because required variables are missing")
    
    print("\n4. SOLUTION OPTIONS:")
    print("=" * 40)
    print("Option 1: Update template to use available variables")
    print("Change template to:")
    print("{{#each orderItems}}")
    print("  {{name}}")
    print("  Qty: {{quantity}}")
    print("  Price: {{price}}")
    print("{{/each}}")
    print()
    print("Option 2: Update backend to send lens details")
    print("Add product_id and lens object to orderItems")
    print()
    print("Option 3: Use simple template")
    print("Remove the complex product details section")
    
    print("\n5. QUICK FIX - SIMPLE TEMPLATE:")
    print("=" * 40)
    simple_template = '''
<!-- Order details -->
<tr>
  <td class="px" style="padding:14px 28px 8px 28px;font-family:Arial,Helvetica,sans-serif;">
    <div style="font-size:14px;color:#111;font-weight:700;margin-bottom:8px;">
      Customer order details
    </div>
    
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#111;width:100%;">
      <tbody>
        {{#each orderItems}}
        <tr>
          <td style="padding:12px 0;border-top:1px solid #eee;vertical-align:top;">
            <div style="font-weight:700;color:#111;">
              {{name}}
            </div>
            <div style="color:#777;font-size:12px;margin-top:4px;">
              Qty: {{quantity}}
            </div>
            <div style="color:#555;font-size:13px;margin-top:4px;">
              Price: {{price}}
            </div>
          </td>
        </tr>
        {{/each}}
        
        <!-- Shipping -->
        <tr>
          <td style="padding:10px 0;border-top:1px solid #eee;color:#444;text-align:right;">
            Shipping
          </td>
        </tr>
        
        <tr>
          <td style="padding:10px 0;border-top:1px solid #eee;font-weight:700;text-align:right;">
            Shipping Cost: {{shipping_cost}}
          </td>
        </tr>

        <!-- Total -->
        <tr>
          <td style="padding:12px 0;border-top:2px solid #111;font-weight:700;font-size:16px;text-align:right;">
            Total paid: {{order_total}}
          </td>
        </tr>

      </tbody>
    </table>

    <div style="font-size:12px;color:#666;margin-top:8px;">
      Price includes VAT
    </div>
  </td>
</tr>
'''
    print("Replace the product details section in your MSG91 template with this simple version")
    
    print("\n6. IMMEDIATE ACTION:")
    print("=" * 40)
    print("1. Go to MSG91 Dashboard")
    print("2. Find template: order_placed_v1_3")
    print("3. Replace the product details section with the simple template above")
    print("4. Save and test")

if __name__ == "__main__":
    debug_empty_email()
