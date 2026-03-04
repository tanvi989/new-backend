#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from payment_service import StripePaymentService
from pymongo import MongoClient

def test_direct_payment_service():
    """Test the payment service directly to isolate the datetime issue"""
    
    print("=== Testing Payment Service Directly ===")
    
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://tanvi9891:tanvi2701@ac-jq2pulx-shard-00-00.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-01.ck8iin3.mongodb.net:27017,ac-jq2pulx-shard-00-02.ck8iin3.mongodb.net:27017/?replicaSet=atlas-29v1f8-shard-0&ssl=true&authSource=admin")
        db = client['gaMultilens']
        
        # Create payment service
        payment_service = StripePaymentService(db)
        
        # Test with minimal metadata
        metadata = {
            "test": "direct_test",
            "user_id": "test_user_123",
            "customer_email": "test@example.com"
        }
        
        print(f"Creating session with metadata: {metadata}")
        
        result = payment_service.create_checkout_session(
            order_id="DIRECT_TEST_123",
            amount=10.00,
            user_email="test@example.com",
            user_id="test_user_123",
            metadata=metadata
        )
        
        print(f"Result: {result}")
        
        if result.get('success'):
            print("✅ Direct service call works!")
        else:
            print(f"❌ Direct service failed: {result.get('error')}")
            
    except Exception as e:
        print(f"Direct test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_payment_service()
