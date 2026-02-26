#!/usr/bin/env python3
"""
Update MSG91 welcome email template
"""
import requests
import json
import os

# MSG91 Configuration
AUTH_KEY = "482085AD1VnJzkrUX6937ff86P1"  # Your MSG91 auth key
DOMAIN = "email.multifolks.com"
TEMPLATE_ID = "welcome_emailer_new"

# New HTML template content
NEW_TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="x-apple-disable-message-reformatting">
    <title>Welcome to Multifolks</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #f6f3f5;
            font-size: 14px;
            font-family: Arial, Helvetica, sans-serif;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 16px;
            overflow: hidden;
        }
        
        .hero-image {
            width: 100%;
            max-width: 600px;
            height: auto;
            border: 0;
        }
        
        .content {
            padding: 28px;
            font-family: Arial, Helvetica, sans-serif;
            color: #111;
        }
        
        .welcome-title {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        
        .welcome-text {
            font-size: 15px;
            line-height: 24px;
            color: #333;
        }
        
        .cta-button {
            background: #563049;
            color: #ffffff;
            text-decoration: none;
            padding: 12px 28px;
            border-radius: 30px;
            font-weight: 700;
            font-size: 14px;
            display: inline-block;
        }
        
        .footer {
            padding: 20px 28px 26px 28px;
            font-family: Arial, Helvetica, sans-serif;
        }
        
        .team-signature {
            font-size: 14px;
            color: #111;
        }
        
        .address {
            font-size: 12px;
            color: #777;
            margin-top: 10px;
        }
        
        @media (max-width: 600px) {
            .container { width: 100% !important; }
            .px { padding-left: 18px !important; padding-right: 18px !important; }
            .center { text-align: center !important; }
        }
    </style>
</head>
<body style="margin: 0; padding: 0; background: #f6f3f5;">
    <!-- Preheader -->
    <div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;">
        Welcome to the life-enhancing power of multifocals.
    </div>
    
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background: #f6f3f5; width: 100%;">
        <tr>
            <td align="center" style="padding: 24px 12px;">
                <table class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width: 600px; max-width: 600px; background: #ffffff; border-radius: 16px; overflow: hidden;">
                    <!-- Hero -->
                    <tr>
                        <td style="background: #563049;">
                            <img src="https://storage.googleapis.com/myapp-image-bucket-001/emailer/Email%20Banner.jpg" width="600" alt="Multifolks — Made for real life. Made for you." style="width: 100%; max-width: 600px; height: auto; border: 0;" class="hero-image">
                        </td>
                    </tr>
                    
                    <!-- Welcome Content -->
                    <tr>
                        <td class="px content" style="padding: 28px; font-family: Arial, Helvetica, sans-serif; color: #111;">
                            <div class="welcome-title">Welcome to Multifolks, {{name}}.</div>
                            <div class="welcome-text">
                                You've joined a community that believes good living starts with good vision.<br><br>
                                At Multifolks, we are obsessed about making multifocals work for you — accurately measured, beautifully designed, and fairly priced.<br><br>
                                No guesswork. No compromises. Just glasses made for the way you live now.<br><br>
                                Whether you're exploring progressives for the first time or refining your next pair, we're here to guide you with clarity and care.
                            </div>
                            
                            <!-- CTA Button -->
                            <div style="text-align: center; margin-top: 28px;">
                                <a href="https://multifolks.com" class="cta-button">&nbsp;Explore Multifocals&nbsp;</a>
                            </div>
                            
                            <div style="margin-top: 28px; font-size: 14px; line-height: 22px; color: #444;">
                                If you ever need help choosing lenses, understanding prescriptions, or getting your perfect fit — just reply to this email.<br><br>
                                We're real people. And we're here for you.
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td class="footer" style="padding: 20px 28px 26px 28px; font-family: Arial, Helvetica, sans-serif;">
                            <div class="team-signature">— Team Multifolks</div>
                            <div class="address">Multifolks • 2 Leman Street, London E1W 9US</div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""

def update_template():
    """
    Update the welcome email template in MSG91
    """
    print("=" * 80)
    print("UPDATING MSG91 WELCOME EMAIL TEMPLATE")
    print("=" * 80)
    
    # MSG91 API endpoint for updating templates
    url = f"https://control.msg91.com/api/v5/email/template/{TEMPLATE_ID}"
    
    headers = {
        "authkey": AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "template_name": "Welcome Email Template",
        "template_html": NEW_TEMPLATE_HTML,
        "template_text": "Welcome to Multifolks! You've joined a community that believes good living starts with good vision.",
        "category": "transactional",
        "variables": [
            {
                "name": "name",
                "type": "string",
                "required": True,
                "display_name": "Customer Name"
            }
        ]
    }
    
    try:
        print(f"Updating template: {TEMPLATE_ID}")
        print(f"Using Auth Key: {AUTH_KEY[:20]}...")
        
        response = requests.put(url, json=payload, headers=headers)
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Template updated successfully!")
            print(f"Response: {json.dumps(response_data, indent=2)}")
        else:
            print(f"Failed to update template")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

def test_template():
    """
    Test the updated template
    """
    print("\n" + "=" * 80)
    print("TESTING UPDATED TEMPLATE")
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
                "name": "Test User",
                "NAME": "Test User"
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
    print("MSG91 Template Updater")
    print("This script will update the welcome email template in MSG91")
    
    choice = input("\nWhat would you like to do?\n1. Update template\n2. Test existing template\n3. Both\nChoice (1/2/3): ")
    
    if choice in ["1", "3"]:
        update_template()
    
    if choice in ["2", "3"]:
        test_template()
    
    print("\n" + "=" * 80)
    print("Alternative: Manual Update")
    print("=" * 80)
    print("If the API doesn't work, you can manually update the template:")
    print("1. Go to: https://control.msg91.com/")
    print("2. Navigate: Email -> Templates")
    print(f"3. Find template: {TEMPLATE_ID}")
    print("4. Click 'Edit' and paste the new HTML content")
    print("5. Save the template")
