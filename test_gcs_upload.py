#!/usr/bin/env python3
"""
Test script to verify GCS prescription upload functionality
"""
import os
import sys
from google.cloud import storage
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_gcs_connection():
    """Test GCS connection and bucket access"""
    print("=" * 60)
    print("Testing GCS Connection and Permissions")
    print("=" * 60)
    
    gcs_credentials_path = os.path.join(os.path.dirname(__file__), "gcs-service-account.json")
    
    # Check if credentials file exists
    print(f"\n1. Checking credentials file...")
    if not os.path.exists(gcs_credentials_path):
        print(f"   ❌ FAIL: Credentials file not found at: {gcs_credentials_path}")
        return False
    print(f"   ✓ PASS: Credentials file found")
    
    # Initialize GCS client
    print(f"\n2. Initializing GCS client...")
    try:
        storage_client = storage.Client.from_service_account_json(gcs_credentials_path)
        print(f"   ✓ PASS: GCS client initialized")
    except Exception as e:
        print(f"   ❌ FAIL: Failed to initialize GCS client: {str(e)}")
        return False
    
    # Check bucket access
    print(f"\n3. Checking bucket access...")
    bucket_name = "myapp-image-bucket-001"
    try:
        bucket = storage_client.bucket(bucket_name)
        exists = bucket.exists()
        if exists:
            print(f"   ✓ PASS: Bucket '{bucket_name}' exists and is accessible")
        else:
            print(f"   ❌ FAIL: Bucket '{bucket_name}' does not exist")
            return False
    except Exception as e:
        print(f"   ❌ FAIL: Error accessing bucket: {str(e)}")
        return False
    
    # Test upload permission
    print(f"\n4. Testing upload permission...")
    try:
        test_blob_name = f"prescriptions/test/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        blob = bucket.blob(test_blob_name)
        test_content = b"Test prescription upload"
        blob.upload_from_string(test_content, content_type="text/plain")
        print(f"   ✓ PASS: Successfully uploaded test file")
        
        # Generate URL
        public_url = f"https://storage.googleapis.com/{bucket_name}/{test_blob_name}"
        print(f"   📎 Test file URL: {public_url}")
        
        # Clean up test file
        print(f"\n5. Cleaning up test file...")
        blob.delete()
        print(f"   ✓ PASS: Test file deleted")
        
    except Exception as e:
        print(f"   ❌ FAIL: Upload test failed: {str(e)}")
        return False
    
    print(f"\n{'=' * 60}")
    print("✅ All tests passed! GCS is configured correctly.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_gcs_connection()
    sys.exit(0 if success else 1)
