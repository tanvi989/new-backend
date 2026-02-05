import requests
import json
import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MSG91Service:
    def __init__(self):
        self.auth_key = config.MSG91_AUTH_KEY
        self.domain = config.MSG91_DOMAIN
        self.sender_email = config.MSG91_SENDER_EMAIL
        self.sender_name = config.MSG91_SENDER_NAME
        self.base_url = "https://control.msg91.com/api/v5/email/send"
        
        logger.info(f"MSG91 Service initialized - Domain: {self.domain}, Sender: {self.sender_email}")

    def send_email(self, to_email: str, template_id: str, variables: dict):
        """
        Send email using MSG91 API with detailed logging.
        
        Args:
            to_email: Recipient email address
            template_id: MSG91 template ID
            variables: Dictionary of template variables
            
        Returns:
            dict: Response with success status and data/error message
        """
        logger.info(f"[MSG91] Preparing to send email")
        logger.info(f"   Template: {template_id}")
        logger.info(f"   To: {to_email}")
        logger.info(f"   Variables: {list(variables.keys())}")
        
        if not self.auth_key or not self.domain:
            logger.error("[ERR] MSG91 credentials not configured")
            return {"success": False, "msg": "MSG91 not configured"}

        payload = {
            "recipients": [
                {
                    "to": [
                        {
                            "name": variables.get("name", variables.get("NAME", "User")),
                            "email": to_email
                        }
                    ],
                    "variables": variables
                }
            ],
            "from": {
                "email": self.sender_email,
                "name": self.sender_name
            },
            "domain": self.domain,
            "template_id": template_id
        }

        headers = {
            "authkey": self.auth_key,
            "Content-Type": "application/json"
        }
        
        logger.info(f"[MSG91] Sending request to {self.base_url}")

        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            logger.info(f"[MSG91] Response status {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                unique_id = response_data.get('data', {}).get('unique_id', 'N/A')
                logger.info(f"[OK] MSG91: Email queued successfully")
                logger.info(f"   Unique ID: {unique_id}")
                logger.info(f"   Message: {response_data.get('message', 'N/A')}")
                return {"success": True, "data": response_data}
            else:
                logger.error(f"[ERR] MSG91: Failed with status {response.status_code}")
                logger.error(f"   Response: {response.text}")
                return {"success": False, "msg": f"Failed to send email: {response.text}"}
        except Exception as e:
            logger.error(f"[ERR] MSG91: Exception occurred: {str(e)}")
            return {"success": False, "msg": str(e)}

    def send_login_pin(self, email: str, pin: str, name: str = None):
        """
        Send login PIN via email.
        """
        logger.info(f"[MSG91] Sending login PIN to {email}")
        template_id = config.MSG91_TEMPLATE_ID
        if not template_id:
            logger.error("[ERR] MSG91_TEMPLATE_ID not configured")
            return {"success": False, "msg": "Template ID missing"}
            
        variables = {
            "oneTimePin": pin,
            "firstName": name or "User",
            # Keep old ones for backward compatibility if needed, or remove them. 
            # Given the image is specific, best to include exactly what's needed plus common variations if unsure, 
            # but user said "its like this", so I will prioritize the new ones.
            "OTP": pin,
            "name": name or "User"
        }
        
        return self.send_email(email, template_id, variables)

    def send_password_reset_pin(self, email: str, pin: str, name: str = None):
        """
        Send password reset PIN via email.
        """
        logger.info(f"[MSG91] Sending password reset PIN to {email}")
        template_id = config.MSG91_RESET_TEMPLATE_ID or config.MSG91_TEMPLATE_ID
        if not template_id:
            logger.error("[ERR] MSG91_RESET_TEMPLATE_ID not configured")
            return {"success": False, "msg": "Template ID missing"}
            
        variables = {
            "oneTimePin": pin,
            "firstName": name or "User",
            "OTP": pin,
            "name": name or "User"
        }
        
        return self.send_email(email, template_id, variables)

    def send_welcome_email(self, email: str, name: str = None, password: str = None):
        """
        Send welcome email to new users.
        """
        logger.info(f"[MSG91] Sending welcome email to {email}")
        template_id = config.MSG91_WELCOME_TEMPLATE_ID
        if not template_id:
            logger.error("[ERR] MSG91_WELCOME_TEMPLATE_ID not configured")
            return {"success": False, "msg": "Welcome template ID missing"}
            
        variables = {
            "NAME": name or "User",
            "name": name or "User",
            "email": email
        }
        
        if password:
            variables["PASSWORD"] = password
            variables["password"] = password
        
        return self.send_email(email, template_id, variables)

    def send_order_confirmation(self, email: str, order_id: str, order_total: str = None, name: str = None):
        """
        Send order confirmation email.
        """
        logger.info(f"[MSG91] Sending order confirmation to {email}")
        logger.info(f"   Order ID: {order_id}, Total: {order_total}")
        template_id = config.MSG91_ORDER_TEMPLATE_ID
        if not template_id:
            logger.error("[ERR] MSG91_ORDER_TEMPLATE_ID not configured")
            return {"success": False, "msg": "Order template ID missing"}
            
        variables = {
            "NAME": name or "User",
            "name": name or "User",
            "order_id": order_id,
            "ORDER_ID": order_id,
            "email": email
        }
        
        if order_total:
            variables["order_total"] = order_total
            variables["ORDER_TOTAL"] = order_total
        
        return self.send_email(email, template_id, variables)
