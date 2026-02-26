#!/usr/bin/env python3
"""
Corrected order template HTML using orderItems instead of cart
"""

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

											<!-- DYNAMIC LOOP START - USING orderItems -->
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
													Shipping Cost: {{shipping_cost}}
												</td>
											</tr>

											<!-- Total -->
											<tr>
												<td colspan="2" style="padding:12px 0;border-top:2px solid #111;font-weight:700;font-size:16px;text-align:right;">
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

if __name__ == "__main__":
    print("CORRECTED ORDER TEMPLATE HTML")
    print("=" * 50)
    print("Key Changes:")
    print("1. Changed {{#each cart}} to {{#each orderItems}}")
    print("2. All other variables remain the same")
    print("3. This will now display product details correctly")
    print("\nCopy this HTML and update your MSG91 template:")
    print("Template ID: order_placed_v1_3")
    print("\nThe template will now show:")
    print("- Product names and IDs")
    print("- Lens details (category, type, index, coating)")
    print("- Tint information (if available)")
    print("- Quantities")
    print("- Shipping cost and total")
    print("=" * 50)
    print(CORRECTED_TEMPLATE_HTML)
