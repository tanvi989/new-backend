#!/bin/bash
echo "Pushing updated backend to GitHub..."

# Add all changes
git add .

# Commit the changes
git commit -m "Fix order confirmation email - send only after payment

- Add /send-confirmation-email endpoint
- Disable premature email sending in order creation and webhook
- Extract full lens data and product_id for email template
- Send confirmation email only after payment success
- Fix frontend authentication token retrieval
- Add detailed console logging for debugging"

# Push to GitHub
git push origin main

echo "✅ Backend code pushed to GitHub!"
echo "Now run these commands on live server:"
echo "cd ~/new-backend"
echo "git pull origin main"
echo "sudo systemctl restart testbackend"
