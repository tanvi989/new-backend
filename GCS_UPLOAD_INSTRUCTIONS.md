# Google Cloud Storage Image Upload Instructions

## Prerequisites

### 1. Install Google Cloud SDK
```bash
# Download and install
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Initialize
gcloud init
```

### 2. Install Python Library
```bash
pip install google-cloud-storage
```

### 3. Authenticate
```bash
# Authenticate with your Google account
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

### 4. Verify Bucket Access
```bash
# List buckets to verify access
gsutil ls gs://myapp-image-bucket-001/

# Or create the bucket if it doesn't exist
gsutil mb gs://myapp-image-bucket-001/

# Make bucket publicly readable (for product images)
gsutil iam ch allUsers:objectViewer gs://myapp-image-bucket-001
```

---

## Upload Images

### Run the Upload Script
```bash
cd /home/selfeey-india/Documents/AI_Projects/login_api
python3 upload_images_to_gcs.py
```

The script will:
1. ✅ Upload all images from `Spexmojo_images/` to GCS
2. ✅ Upload all images from `Faceaface/` to GCS
3. ✅ Update MongoDB with new GCS URLs
4. ✅ Maintain folder structure in GCS

---

## Verify Upload

### Check GCS Bucket
```bash
# List uploaded files
gsutil ls -r gs://myapp-image-bucket-001/ | head -20

# Check specific product images
gsutil ls gs://myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E19B8501/
```

### Test Image URL
Open in browser:
```
https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E19B8501/E19B8501_1.jpg
```

### Verify Database
```bash
python3 -c "from pymongo import MongoClient; import config; client = MongoClient(config.MONGO_URI); db = client[config.DATABASE_NAME]; product = db['products'].find_one(); print('Image:', product.get('image'))"
```

Should show:
```
Image: https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E19B8501/E19B8501_1.jpg
```

---

## Cleanup Local Files

After verifying GCS upload works:

```bash
cd /home/selfeey-india/Documents/AI_Projects/Multifolks_Frontend

# Remove symlinks
rm public/Spexmojo_images
rm public/Faceaface

# Optionally, archive local images (don't delete yet!)
# tar -czf ~/product_images_backup.tar.gz Spexmojo_images/ "Faceaface and ad cross correct (1)/"
```

---

## Troubleshooting

### Permission Denied
```bash
# Re-authenticate
gcloud auth application-default login
```

### Bucket Not Found
```bash
# Create bucket
gsutil mb -l us-central1 gs://myapp-image-bucket-001

# Make public
gsutil iam ch allUsers:objectViewer gs://myapp-image-bucket-001
```

### Images Not Loading in Browser
```bash
# Check CORS configuration
gsutil cors get gs://myapp-image-bucket-001

# Set CORS if needed
echo '[{"origin": ["*"], "method": ["GET"], "responseHeader": ["Content-Type"], "maxAgeSeconds": 3600}]' > cors.json
gsutil cors set cors.json gs://myapp-image-bucket-001
```

---

## Cost Estimate

- **Storage**: ~$0.02/GB/month (Standard storage)
- **Network**: ~$0.12/GB (egress to internet)
- **Operations**: Minimal cost for GET requests

For 811 products × 6 images × ~16KB average = ~78MB
- Storage cost: ~$0.002/month
- Bandwidth (1000 views/day): ~$0.30/month

**Total estimated cost: <$1/month**
