#!/usr/bin/env python3
"""
Update MSG91 forgot password email template
"""
import requests
import json
import os

# MSG91 Configuration
AUTH_KEY = "482085AD1VnJzkrUX6937ff86P1"  # Your MSG91 auth key
DOMAIN = "email.multifolks.com"
TEMPLATE_ID = "forgot_password_46592"

# New HTML template content
NEW_TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>Reset your PIN — Multifolks</title>

<style>
body {
  margin:0;
  padding:0;
  background:#f6f3f5;
  font-size:14px;
}

@media (max-width:600px) {
  .container { width:100% !important; }
  .px { padding-left:18px !important; padding-right:18px !important; }
  .center { text-align:center !important; }
}
</style>
</head>

<body style="margin:0;padding:0;background:#f6f3f5;">

<!-- Preheader -->
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;">
Use this code to reset your Multifolks PIN.
</div>

<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f6f3f5;">
<tr>
<td align="center" style="padding:24px 12px;">

<table class="container" width="600" cellpadding="0" cellspacing="0" border="0"
style="width:600px;max-width:600px;background:#ffffff;border-radius:16px;overflow:hidden;">

<!-- Hero -->
<tr>
<td style="background:#563049;">
<img src="https://storage.googleapis.com/myapp-image-bucket-001/emailer/Email%20Banner.jpg"
width="600"
alt="Multifolks — Made for real life. Made for you."
style="width:100%;max-width:600px;height:auto;border:0;">
</td>
</tr>

<!-- Content -->
<tr>
<td class="px" style="padding:28px;font-family:Arial,Helvetica,sans-serif;color:#111;">

<div style="font-size:18px;font-weight:700;margin-bottom:12px;">
Your Multifolks OTP
</div>

<div style="font-size:15px;line-height:24px;color:#333;">
We received a request to generate OTP for your Multifolks account.
<br><br>
Use the code below to continue:
</div>

<!-- PIN Code Box -->
<div style="margin-top:18px;text-align:center;">
  <div style="display:inline-block;background:#f6f3f5;border:1px solid #eee;border-radius:14px;padding:16px 22px;">
    <div style="font-size:12px;letter-spacing:0.6px;color:#666;margin-bottom:6px;">OTP</div>
    <div style="font-size:26px;letter-spacing:6px;font-weight:800;color:#111;">{{OTP}}</div>
  </div>
</div>

<div style="margin-top:18px;font-size:14px;line-height:22px;color:#444;">
This code will expire in <strong>15</strong> minutes.
<br>
If you didn't request this, you can safely ignore this email — your account remains secure.
</div>

<div style="margin-top:22px;font-size:12px;line-height:18px;color:#666;">
For your security, please don't share this code with anyone (including Multifolks team members).
</div>

</td>
</tr>

<!-- Footer -->
<tr>
<td style="padding:20px 28px 26px 28px;font-family:Arial,Helvetica,sans-serif;">
<div style="font-size:14px;color:#111;">— Team Multifolks</div>
<div style="font-size:12px;color:#777;margin-top:10px;">
Multifolks • 2 Leman Street, London E1W 9US
</div>
</td>
</tr>

</table>

</td>
</tr>
</table>

</body>
</html>"""

def test_template():
    """
    Test the current template
    """
    print("=" * 80)
    print("TESTING FORGOT PASSWORD TEMPLATE")
    print("=" * 80)
    
    test_email = "paradkartanvii@gmail.com"  # Replace with your test email
    url = "https://control.msg91.com/api/v5/email/send"
    
    headers = {
        "authkey": AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "recipients": [{
            "to": [{
                "name": "Test User",
                "email": test_email
            }],
            "variables": {
                "OTP": "123456",
                "PIN": "123456"
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
        print(f"Sending test email to: {test_email}")
        print(f"Using template ID: {TEMPLATE_ID}")
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Test email sent successfully!")
            print(f"Response: {json.dumps(response_data, indent=2)}")
        else:
            print(f"Failed to send test email")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("MSG91 Forgot Password Template Tester")
    print("This script will test the forgot_password_46592 template")
    
    print("\n" + "=" * 80)
    print("TEMPLATE INFORMATION")
    print("=" * 80)
    print(f"Template ID: {TEMPLATE_ID}")
    print(f"This is the template used for password reset PIN emails")
    
    test_template()
    
    print("\n" + "=" * 80)
    print("MANUAL UPDATE INSTRUCTIONS")
    print("=" * 80)
    print("To update the template content:")
    print("1. Go to: https://control.msg91.com/")
    print("2. Navigate: Email -> Templates")
    print(f"3. Find template: {TEMPLATE_ID}")
    print("4. Click 'Edit' and paste the new HTML content")
    print("5. Save the template")
    print("\nThe new HTML content is provided in this script as NEW_TEMPLATE_HTML")
