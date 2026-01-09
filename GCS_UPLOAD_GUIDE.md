# GCS Upload - Step-by-Step Guide

## Overview
Upload ~5,000 product images to Google Cloud Storage and update MongoDB paths.

---

## Step 1: Install Google Cloud Storage Library

```bash
cd /home/selfeey-india/Documents/AI_Projects/login_api
pip install google-cloud-storage
```

---

## Step 2: Authenticate with Google Cloud

**Option A: Using Service Account (Recommended for Production)**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to IAM & Admin → Service Accounts
3. Create a service account with Storage Admin role
4. Download JSON key file
5. Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

**Option B: Using gcloud CLI (Easier for Development)**
```bash
# Install gcloud SDK if not installed
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Authenticate
gcloud auth application-default login

# Set project
gcloud config set project YOUR_PROJECT_ID
```

---

## Step 3: Verify Bucket Exists and is Public

```bash
# Check if bucket exists
gsutil ls gs://myapp-image-bucket-001/

# If bucket doesn't exist, create it
gsutil mb -l us-central1 gs://myapp-image-bucket-001

# Make bucket publicly readable
gsutil iam ch allUsers:objectViewer gs://myapp-image-bucket-001

# Set CORS for web access
echo '[{"origin": ["*"], "method": ["GET"], "responseHeader": ["Content-Type"], "maxAgeSeconds": 3600}]' > /tmp/cors.json
gsutil cors set /tmp/cors.json gs://myapp-image-bucket-001
```

---

## Step 4: Run Upload Script

```bash
cd /home/selfeey-india/Documents/AI_Projects/login_api
python3 upload_images_to_gcs.py
```

**What it does:**
- Uploads all images from `Spexmojo_images/` (4,236 images)
- Uploads all images from `Faceaface/` (630 images)
- Updates MongoDB with GCS URLs
- Shows progress for each file
- Skips already uploaded files

**Expected output:**
```
================================================================================
🚀 Google Cloud Storage Image Upload & MongoDB Update Script
================================================================================
✅ Connected to GCS bucket: myapp-image-bucket-001
✅ Connected to MongoDB: gaMultilens

📁 Scanning directory: /path/to/Spexmojo_images
📊 Found 4236 image files to upload
✅ Uploaded (1/4236): Spexmojo_images/Spexmojo_images/E19B8501/E19B8501_1.jpg
...
```

---

## Step 5: Verify Upload

### Check GCS
```bash
# List some uploaded files
gsutil ls gs://myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/ | head -10

# Check specific product
gsutil ls gs://myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E19B8501/
```

### Test Image URL in Browser
```
https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E19B8501/E19B8501_1.jpg
```

### Check MongoDB
```bash
python3 -c "from pymongo import MongoClient; import config; client = MongoClient(config.MONGO_URI); db = client[config.DATABASE_NAME]; p = db['products'].find_one(); print('Image:', p.get('image'))"
```

Should output:
```
Image: https://storage.googleapis.com/myapp-image-bucket-001/Spexmojo_images/Spexmojo_images/E19B8501/E19B8501_1.jpg
```

---

## Step 6: Test Frontend

1. Refresh browser (Ctrl+Shift+R)
2. Navigate to Men Collection or Women Collection
3. Images should load from GCS URLs
4. Check browser DevTools Network tab - should see requests to `storage.googleapis.com`

---

## Step 7: Cleanup (After Verification)

```bash
cd /home/selfeey-india/Documents/AI_Projects/Multifolks_Frontend

# Remove symlinks (no longer needed)
rm public/Spexmojo_images
rm public/Faceaface

# Optional: Archive local images (DON'T DELETE YET!)
tar -czf ~/product_images_backup_$(date +%Y%m%d).tar.gz \
  Spexmojo_images/ \
  "Faceaface and ad cross correct (1)/"
```

---

## Troubleshooting

### Error: "Could not automatically determine credentials"
```bash
gcloud auth application-default login
```

### Error: "403 Forbidden"
```bash
# Make bucket public
gsutil iam ch allUsers:objectViewer gs://myapp-image-bucket-001
```

### Error: "Bucket not found"
```bash
# Create bucket
gsutil mb gs://myapp-image-bucket-001
```

### Images not loading in browser
- Check CORS: `gsutil cors get gs://myapp-image-bucket-001`
- Verify public access: `gsutil iam get gs://myapp-image-bucket-001`
- Test URL directly in browser

---

## Cost Estimate

- **Storage**: $0.02/GB/month
- **Bandwidth**: $0.12/GB egress
- **Total images**: ~78MB
- **Monthly cost**: <$1

---

## Next Steps

1. ✅ Install google-cloud-storage
2. ✅ Authenticate with Google Cloud
3. ✅ Verify bucket access
4. ✅ Run upload script
5. ✅ Verify images in GCS
6. ✅ Test frontend
7. ✅ Remove local symlinks
