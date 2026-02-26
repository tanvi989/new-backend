#!/usr/bin/env python3
"""
Update MSG91 order confirmation template to order_placed_v1_3
"""
import requests
import json

# MSG91 Configuration
AUTH_KEY = "482085AD1VnJzkrUX6937ff86P1"
DOMAIN = "email.multifolks.com"
TEMPLATE_ID = "order_placed_v1_3"

# Clean HTML template content (removed duplicate styles)
NEW_TEMPLATE_HTML = """<!DOCTYPE html>
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
							<!-- Status card -->
							<tr>
								<td class="px " style="padding:14px 28px 6px 28px;font-family:Arial,Helvetica,sans-serif;">

									<table width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid #eee;border-radius:14px;width:100%;">
										<tbody>
											<tr>
												<td style="padding:14px 14px 10px 14px;">
													<div style="font-size:13px;color:#444;margin-bottom:10px;">Order <strong>#{{ORDER_NUMBER}}</strong> {{ORDER_DATE}}</div>

														<table width="100%" cellpadding="0" cellspacing="0" border="0">
															<tbody>
																<tr>
																	<!-- Order Confirmed (Green) -->
																	<td class="stack center" align="center" style="padding:6px 4px;width:25%;">
																		<div style="width:28px;height:28px;line-height:28px;border-radius:50%;background:#2e7d32;color:#ffffff;font-weight:700;font-size:16px;display:inline-block;">✓</div>
																		<div style="font-size:12px;color:#111;margin-top:6px;font-weight:700;">Order Confirmed</div>
																	</td>
																	<!-- Processing (Grey ?) -->
																	<td class="stack center" align="center" style="padding:6px 4px;width:25%;">
																		<div style="width:28px;height:28px;line-height:28px;border-radius:50%;background:#e0e0e0;color:#777;font-weight:700;font-size:16px;display:inline-block;">?</div>
																		<div style="font-size:12px;color:#777;margin-top:6px;font-weight:700;">Processing</div>
																	</td>
																	<!-- Shipped (Grey ?) -->
																	<td class="stack center" align="center" style="padding:6px 4px;width:25%;">
																		<div style="width:28px;height:28px;line-height:28px;border-radius:50%;background:#e0e0e0;color:#777;font-weight:700;font-size:16px;display:inline-block;">?</div>
																		<div style="font-size:12px;color:#777;margin-top:6px;font-weight:700;">Shipped</div>
																	</td>
																	<!-- Delivered (Grey ?) -->
																	<td class="stack center" align="center" style="padding:6px 4px;width:25%;">
																		<div style="width:28px;height:28px;line-height:28px;border-radius:50%;background:#e0e0e0;color:#777;font-weight:700;font-size:16px;display:inline-block;">?</div>
																		<div style="font-size:12px;color:#777;margin-top:6px;font-weight:700;">Delivered</div>
																	</td>
																</tr>
															</tbody>
														</table>
														<div style="font-size:14px;line-height:22px;color:#444;margin-top:12px;">Need help adjusting or refining? Just reply to this email — we're here.</div>
												</td>
											</tr>
										</tbody>
									</table>
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
												<!-- Product Image -->
												<td style="padding:12px 0;border-top:1px solid #eee;width:90px;vertical-align:top;">
													<img 
														src="https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/{{product_id}}/{{product_id}}.png"
														alt="{{name}}"
														width="80"
														style="width:80px;height:auto;border-radius:8px;display:block;"
														onerror="this.style.display='none';">
												</td>

												<!-- Product Details -->
												<td style="padding:12px 0;border-top:1px solid #eee;vertical-align:top;">
													<div style="font-weight:700;color:#111;">
														{{name}} ({{product_id}})
													</div>

													<div style="color:#555;font-size:13px;line-height:18px;margin-top:4px;">
														{{lens.main_category}} • {{lens.lensCategoryDisplay}} • {{lens.lensIndex}}
													</div>

													<div style="color:#555;font-size:13px;line-height:18px;margin-top:4px;">
														Coating: {{lens.coating}}
													</div>

													{{#if lens.tint_color}}
													<div style="color:#555;font-size:13px;margin-top:4px;">
														Tint: {{lens.tint_type}} - {{lens.tint_color}}
													</div>
													{{/if}}

													<div style="color:#777;font-size:12px;margin-top:4px;">
														Qty: {{quantity}}
													</div>
												</td>
											</tr>
											{{/each}}
											<!-- DYNAMIC LOOP END -->

											<!-- Shipping -->
											<tr>
												<td colspan="2" style="padding:10px 0;border-top:1px solid #eee;color:#444;text-align:right;">
													Shipping
												</td>
											</tr>
											
											<tr>
												<td colspan="2" style="padding:10px 0;border-top:1px solid #eee;font-weight:700;text-align:right;">
													Shipping Cost: £{{shipping_cost}}
												</td>
											</tr>

											<!-- Total -->
											<tr>
												<td colspan="2" style="padding:12px 0;border-top:2px solid #111;font-weight:700;font-size:16px;text-align:right;">
													Total paid: £{{order_total}}
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

def update_template():
    """
    Update the new template in MSG91
    """
    print("=" * 80)
    print("UPDATING ORDER TEMPLATE TO order_placed_v1_3")
    print("=" * 80)
    
    # MSG91 API to create/update template
    url = f"https://control.msg91.com/api/v5/email/template/{TEMPLATE_ID}"
    
    headers = {
        "authkey": AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "template_name": "Order Confirmation Template v1.3",
        "template_html": NEW_TEMPLATE_HTML,
        "template_text": "Your order has been confirmed. Order ID: {{ORDER_NUMBER}}",
        "category": "transactional",
        "variables": [
            {
                "name": "ORDER_NUMBER",
                "type": "string",
                "required": True,
                "display_name": "Order Number"
            },
            {
                "name": "ORDER_DATE", 
                "type": "string",
                "required": True,
                "display_name": "Order Date"
            },
            {
                "name": "order_total",
                "type": "string", 
                "required": True,
                "display_name": "Order Total"
            },
            {
                "name": "shipping_cost",
                "type": "string",
                "required": True,
                "display_name": "Shipping Cost"
            },
            {
                "name": "NAME",
                "type": "string",
                "required": True,
                "display_name": "Customer Name"
            },
            {
                "name": "orderItems",
                "type": "array",
                "required": True,
                "display_name": "Order Items"
            }
        ]
    }
    
    try:
        print(f"Updating template: {TEMPLATE_ID}")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Template updated successfully!")
            print(f"Response: {json.dumps(response_data, indent=2)}")
        else:
            print(f"Failed to update template")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

def test_new_template():
    """
    Test the new template
    """
    print("\n" + "=" * 80)
    print("TESTING NEW TEMPLATE")
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
                "ORDER_NUMBER": "TEST-789",
                "ORDER_DATE": "26 Feb 2026",
                "order_total": "99.99",
                "shipping_cost": "4.99",
                "orderItems": [
                    {
                        "name": "Test Multifocal Glasses",
                        "quantity": 1,
                        "product_id": "MF001"
                    },
                    {
                        "name": "Test Reading Glasses", 
                        "quantity": 2,
                        "product_id": "MF002"
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
        print(f"Sending test email with new template...")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Test email sent successfully!")
            print(f"Unique ID: {response_data.get('data', {}).get('unique_id', 'N/A')}")
            print(f"\nCheck your email for:")
            print(f"- Order ID: TEST-789")
            print(f"- Customer name: Test Customer")
            print(f"- 2 items should appear with product details")
        else:
            print(f"Failed to send test email: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("MSG91 Order Template Creator & Tester")
    print("This script will create and test order_placed_v1_3 template")
    
    choice = input("\nWhat would you like to do?\n1. Create/Update template\n2. Test existing template\nChoice (1/2): ")
    
    if choice == "1":
        update_template()
    elif choice == "2":
        test_new_template()
    else:
        print("Invalid choice")
    
    print("\n" + "=" * 80)
    print("TEMPLATE INFORMATION")
    print("=" * 80)
    print(f"Template ID: {TEMPLATE_ID}")
    print(f"This template will be used for order confirmation emails")
    print("\nBackend is now configured to use this template ID!")
