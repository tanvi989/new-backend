"""
Prescription CDN Service for Google Cloud Storage
Uses existing GCP setup with bucket: myapp-image-bucket-001
"""

import os
from datetime import datetime
from google.cloud import storage
from werkzeug.utils import secure_filename
import logging

# Configure logging
logger = logging.getLogger(__name__)

# GCS Configuration
BUCKET_NAME = "myapp-image-bucket-001"
GCS_BASE_URL = f"https://storage.googleapis.com/{BUCKET_NAME}"
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(__file__), 'gcs-service-account.json')

# Set credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_PATH

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(file, filename=None):
    """Validate file before upload"""
    if not file:
        raise ValueError("No file provided")
    
    # Get filename - handle both Flask and FastAPI file objects
    file_name = filename or getattr(file, 'filename', None)
    if not file_name:
        raise ValueError("Could not determine filename")
    
    if not allowed_file(file_name):
        raise ValueError(f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Check file size (if available)
    try:
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024)}MB")
    except (AttributeError, OSError):
        # If seek doesn't work, skip size validation
        pass
    
    return True

def generate_prescription_filename(customer_id, cart_id):
    """Generate unique filename for prescription"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"prescription_cust_{customer_id}_cart_{cart_id}_{timestamp}"

def get_gcs_client():
    """Get GCS storage client"""
    try:
        return storage.Client()
    except Exception as e:
        logger.error(f"Failed to initialize GCS client: {str(e)}")
        raise

def upload_prescription_to_gcs(file, customer_id, cart_id, filename=None):
    """
    Upload prescription file to Google Cloud Storage
    
    Args:
        file: File object from Flask/FastAPI request
        customer_id: Customer ID
        cart_id: Cart ID
        filename: Optional filename (for FastAPI UploadFile)
        
    Returns:
        dict: {
            'success': bool,
            'gcs_url': str,
            'blob_name': str,
            'format': str,
            'size': int
        }
    """
    try:
        # Get filename - handle both Flask and FastAPI file objects
        file_name = filename or getattr(file, 'filename', 'prescription.jpg')
        
        # Validate file
        validate_file(file, file_name)
        
        # Get file extension
        file_ext = file_name.rsplit('.', 1)[1].lower() if '.' in file_name else 'jpg'
        
        # Generate unique filename
        base_filename = generate_prescription_filename(customer_id, cart_id)
        new_filename = f"{base_filename}.{file_ext}"
        
        # GCS blob path (organize in prescriptions folder)
        blob_name = f"prescriptions/{new_filename}"
        
        # Initialize GCS client
        storage_client = get_gcs_client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        
        # Set content type based on file extension
        content_type_map = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'pdf': 'application/pdf'
        }
        content_type = content_type_map.get(file_ext, 'application/octet-stream')
        
        # Upload file
        file.seek(0)  # Reset file pointer
        blob.upload_from_file(
            file,
            content_type=content_type,
            rewind=True
        )
        
        # Make blob publicly readable (optional - remove if you want private access)
        # blob.make_public()
        
        # Get file size
        try:
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
        except:
            file_size = 0
        
        # Generate GCS URL
        gcs_url = f"{GCS_BASE_URL}/{blob_name}"
        
        logger.info(f"Successfully uploaded prescription to GCS: {blob_name}")
        
        return {
            'success': True,
            'gcs_url': gcs_url,
            'blob_name': blob_name,
            'format': file_ext,
            'size': file_size,
            'uploaded_at': datetime.now().isoformat()
        }
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        logger.error(f"GCS upload error: {str(e)}")
        return {
            'success': False,
            'error': 'Failed to upload prescription to GCS'
        }

def delete_prescription_from_gcs(blob_name):
    """
    Delete prescription from Google Cloud Storage
    
    Args:
        blob_name: GCS blob name (e.g., 'prescriptions/prescription_cust_123_cart_456.jpg')
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        storage_client = get_gcs_client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        
        if blob.exists():
            blob.delete()
            logger.info(f"Successfully deleted prescription from GCS: {blob_name}")
            return {
                'success': True,
                'message': 'Prescription deleted from GCS'
            }
        else:
            logger.warning(f"Prescription not found in GCS: {blob_name}")
            return {
                'success': False,
                'message': 'Prescription not found in GCS'
            }
            
    except Exception as e:
        logger.error(f"GCS delete error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def generate_signed_url(blob_name, expiration_minutes=60):
    """
    Generate a signed URL for secure, time-limited access to prescription
    
    Args:
        blob_name: GCS blob name
        expiration_minutes: URL expiration time in minutes (default 60)
        
    Returns:
        str: Signed URL or None on error
    """
    try:
        storage_client = get_gcs_client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        
        # Generate signed URL
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=expiration_minutes),
            method="GET"
        )
        
        return url
        
    except Exception as e:
        logger.error(f"Error generating signed URL: {str(e)}")
        return None

def get_prescription_info(blob_name):
    """
    Get information about a prescription file from GCS
    
    Args:
        blob_name: GCS blob name
        
    Returns:
        dict: File information
    """
    try:
        storage_client = get_gcs_client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        
        if blob.exists():
            blob.reload()  # Fetch metadata
            return {
                'success': True,
                'url': f"{GCS_BASE_URL}/{blob_name}",
                'size': blob.size,
                'content_type': blob.content_type,
                'created_at': blob.time_created.isoformat() if blob.time_created else None,
                'updated_at': blob.updated.isoformat() if blob.updated else None
            }
        else:
            return {
                'success': False,
                'error': 'File not found'
            }
    except Exception as e:
        logger.error(f"Error getting prescription info: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def check_gcs_connection():
    """
    Check if GCS connection is working
    
    Returns:
        bool: True if connection successful
    """
    try:
        storage_client = get_gcs_client()
        bucket = storage_client.bucket(BUCKET_NAME)
        bucket.exists()
        logger.info(f"GCS connection successful. Bucket: {BUCKET_NAME}")
        return True
    except Exception as e:
        logger.error(f"GCS connection failed: {str(e)}")
        return False
