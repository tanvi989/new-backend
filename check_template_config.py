#!/usr/bin/env python3
"""
Check which template ID is actually being used at runtime
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import config
    
    print("=" * 60)
    print("CURRENT TEMPLATE CONFIGURATION")
    print("=" * 60)
    print(f"MSG91_AUTH_KEY: {config.MSG91_AUTH_KEY[:20]}...")
    print(f"MSG91_DOMAIN: {config.MSG91_DOMAIN}")
    print(f"MSG91_TEMPLATE_ID: {config.MSG91_TEMPLATE_ID}")
    print(f"MSG91_RESET_TEMPLATE_ID: {config.MSG91_RESET_TEMPLATE_ID}")
    print(f"MSG91_WELCOME_TEMPLATE_ID: {config.MSG91_WELCOME_TEMPLATE_ID}")
    print(f"MSG91_ORDER_TEMPLATE_ID: {config.MSG91_ORDER_TEMPLATE_ID}")
    print(f"MSG91_SENDER_EMAIL: {config.MSG91_SENDER_EMAIL}")
    print(f"MSG91_SENDER_NAME: {config.MSG91_SENDER_NAME}")
    
    print("\n" + "=" * 60)
    print("ENVIRONMENT VARIABLES")
    print("=" * 60)
    
    # Check environment variables
    env_vars = [
        'MSG91_AUTH_KEY',
        'MSG91_DOMAIN', 
        'MSG91_TEMPLATE_ID',
        'MSG91_RESET_TEMPLATE_ID',
        'MSG91_WELCOME_TEMPLATE_ID',
        'MSG91_ORDER_TEMPLATE_ID',
        'MSG91_SENDER_EMAIL',
        'MSG91_SENDER_NAME'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"{var}: {value}")
        else:
            print(f"{var}: (not set)")
    
    print("\n" + "=" * 60)
    print("TEMPLATE USED FOR RESET PIN")
    print("=" * 60)
    
    # Simulate what template ID would be used for reset pin
    reset_template_id = config.MSG91_RESET_TEMPLATE_ID or config.MSG91_TEMPLATE_ID
    print(f"Reset PIN will use template: {reset_template_id}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
