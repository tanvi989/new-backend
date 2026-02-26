#!/usr/bin/env python3
"""
Corrected MSG91 order confirmation template
"""
import requests
import json

# MSG91 Configuration
AUTH_KEY = "482085AD1VnJzkrUX6937ff86P1"
DOMAIN = "email.multifolks.com"
TEMPLATE_ID = "order_placed_23"

# CORRECTED HTML template content using orderItems
CORRECTED_TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width,initial-scale=1">
	<meta name="x-apple-disable-message-reformatting">
	<title>Order Confirmed — Multifolks</title>
	<style>
		body {
			margin: 0; padding: 0; background: #f6f3f5; font-size: 14px;
		}
		
		@media (max-width:600px) {
			.container {
				width: 100% !important;
			}
			.px {
				padding-left: 18px !important; padding-right: 18px !important;
			}
			.stack {
				display: block !important; width: 100% !important;
			}
			.center {
				text-align: center !important;
			}
		}
	</style>
</head>
<body style="margin: 0px; padding: 0px; background: rgb(246, 243, 245);">

	<!-- Preheader -->
	<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;">Welcome to the life-enhancing power of multifocals.</div>

	<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f6f3f5;width:100%;">
		<tbody>
			<tr>
				<td align="center" style="padding:24px 12px;">

					<table class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#ffffff;border-radius:16px;overflow:hidden;">
						<!-- Hero -->
						<tbody>
							<tr>
								<td style="background:#563049;"><img src="https://storage.googleapis.com/myapp-image-bucket-001/emailer/Email%20Banner.jpg" width="600" alt="Multifolks — Made for real life. Made for you." style="width: 100%; max-width: 600px; height: auto; border: 0px; line-height: 100%; outline: none; text-decoration: none;" class="fr-fil fr-dib"></td>
							</tr>
							<!-- Intro -->
							<tr>
								<td class="px" style="padding:22px 28px 6px 28px;font-family:Arial,Helvetica,sans-serif;color:#111;">
									<div style="font-size:16px;line-height:24px;">Hi {{NAME}},<br><br><strong>Your order is confirmed.</strong><br><br>Your order will now move to production soon.<br><br>We'll keep you informed every step of the way.<br>And if anything comes up, we're always within reach.<br><br>Not long now until you experience the life-enhancing power of multifocals.</div>
									<div style="margin-top:14px;font-size:14px;line-height:20px;">Your order details are as below</div>
								</td>
							</tr>
							<!-- Order details -->
							<tr>
								<td class="px" style="padding:14px 28px 8px 28px;font-family:Arial,Helvetica,sans-serif;">
									<div style="font-size:14px;color:#111;font-weight:700;margin-bottom:8px;">
										Customer order details
									</div>
									
									<table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#111;width:100%;">
										<tbody>
											<!-- DYNAMIC LOOP START -->
											{{#each orderItems}}
											<tr>
												<td style="padding:12px 0;border-top:1px solid #eee;vertical-align:top;">
													<div style="font-weight:700;color:#111;margin-bottom:4px;">
														{{name}} (Qty: {{quantity}})
													</div>
													<div style="color:#555;font-size:13px;line-height:18px;">
														Price: {{price}}
													</div>
											</tr>
											{{/each}}
											<!-- DYNAMIC LOOP END -->

											<!-- Shipping -->
											<tr>
												<td colspan="1" style="padding:10px 0;border-top:1px solid #eee;color:#444;text-align:right;">
													Shipping
												</td>
											</tr>
											
											<tr>
												<td colspan="1" style="padding:10px 0;border-top:1px solid #eee;font-weight:700;text-align:right;">
													Shipping Cost: {{shippingCost}}
												</td>
											</tr>

											<!-- Total -->
											<tr>
												<td colspan="1" style="padding:12px 0;border-top:2px solid #111;font-weight:700;font-size:16px;text-align:right;">
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

							<!-- Footer -->
							<tr>
								<td style="padding:18px 28px 24px 28px;font-family:Arial,Helvetica,sans-serif;">
									<div style="font-size:14px;color:#111;">— Team Multifolks</div>
									<div style="font-size:12px;color:#777;margin-top:10px;">
										Multifolks • 2 Leman Street, London E1W 9US
									</div>
								</td>
							</tr>

						</tbody>
					</table>
				</td>
			</tr>
		</tbody>
	</table>

</body>
</html>"""

def test_corrected_template():
    """
    Test corrected order template
    """
    print("=" * 80)
    print("TESTING CORRECTED ORDER TEMPLATE")
    print("=" * 80)
    
    test_email = "paradkartanvii@gmail.com"
    url = "https://control.msg91.com/api/v5/email/send"
    
    headers = {
        "authkey": AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "recipients": [{
            "to": [{
                "name": "Test Customer",
                "email": test_email
            }],
            "variables": {
                "NAME": "Test Customer",
                "order_id": "TEST-456",
                "ORDER_ID": "TEST-456",
                "order_total": "99.99",
                "ORDER_TOTAL": "99.99",
                "orderDate": "26 Feb 2026",
                "shippingCost": "4.99",
                "orderItems": [
                    {
                        "name": "Test Multifocal Glasses",
                        "quantity": 1,
                        "price": "£49.99"
                    },
                    {
                        "name": "Test Reading Glasses", 
                        "quantity": 2,
                        "price": "£24.99"
                    }
                ]
            }
        }],
        "from": {
            "email": "support@multifolks.com",
            "name": "Multifolks"
        },
        "domain": DOMAIN,
        "template_id": TEMPLATE_ID
    }
    
    try:
        print(f"Sending corrected template test...")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Test email sent successfully!")
            print(f"Unique ID: {response_data.get('data', {}).get('unique_id', 'N/A')}")
            print(f"\nCheck your email for:")
            print(f"- Order ID: TEST-456")
            print(f"- Customer name: Test Customer")
            print(f"- 2 items should appear:")
            print(f"  * Test Multifocal Glasses (Qty: 1) - £49.99")
            print(f"  * Test Reading Glasses (Qty: 2) - £24.99")
            print(f"- Total: £99.99")
            print(f"- Shipping: £4.99")
        else:
            print(f"Failed to send test email: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("MSG91 Corrected Order Template")
    print("This script tests the corrected template with proper variables")
    
    test_corrected_template()
    
    print("\n" + "=" * 80)
    print("TEMPLATE UPDATE INSTRUCTIONS")
    print("=" * 80)
    print("1. Go to: https://control.msg91.com/")
    print("2. Navigate: Email -> Templates")
    print(f"3. Find template: {TEMPLATE_ID}")
    print("4. Click 'Edit' and paste the CORRECTED_TEMPLATE_HTML content")
    print("5. Save the template")
    print("\nKEY CHANGES:")
    print("- Changed {{#each cart}} to {{#each orderItems}}")
    print("- Simplified product display")
    print("- Uses correct variable names from backend")
