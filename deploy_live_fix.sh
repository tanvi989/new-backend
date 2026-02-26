#!/bin/bash
echo "=== DEPLOYING CONFIRMATION EMAIL FIX TO LIVE SERVER ==="

# 1. Go to backend directory
cd ~/new-backend

# 2. Check current git status
echo "Current git status:"
git status

# 3. Pull latest changes
echo "Pulling latest changes..."
git pull origin main

# 4. Check if endpoint exists in app.py
echo "Checking if confirmation email endpoint exists..."
grep -n "send-confirmation-email" app.py

# 5. Restart backend service
echo "Restarting backend service..."
sudo systemctl restart testbackend

# 6. Check service status
echo "Checking service status..."
sudo systemctl status testbackend

# 7. Check logs for any errors
echo "Checking recent logs..."
sudo journalctl -u testbackend --no-pager -n 20

echo "=== DEPLOYMENT COMPLETE ==="
echo "Test the confirmation email endpoint:"
echo "curl -X POST https://testbackend.multifolks.com/api/v1/orders/TEST-ORDER/send-confirmation-email -H 'Content-Type: application/json' -H 'Authorization: Bearer test-token'"
