# 🚀 VPS Deployment Guide - Multifolks Backend

Complete guide to deploy the Multifolks FastAPI backend on a Linux VPS server.

## 📋 Prerequisites

- **VPS Server** (Ubuntu 20.04/22.04 or similar Linux distribution)
- **SSH access** to your VPS
- **Domain name** (optional, for HTTPS)
- **MongoDB Atlas** account or MongoDB installed on VPS

## 🔧 Step 1: Connect to Your VPS

```bash
ssh username@your-vps-ip
# Example: ssh root@192.168.1.100
```

## 📦 Step 2: Install System Dependencies

### Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### Install Python and Required Tools
```bash
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor
```

### Install MongoDB (if using local MongoDB)
```bash
# For MongoDB Atlas, skip this step
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

## 📁 Step 3: Set Up Project Directory

```bash
# Create project directory
sudo mkdir -p /var/www/multifolks-backend
sudo chown $USER:$USER /var/www/multifolks-backend

# Navigate to directory
cd /var/www/multifolks-backend
```

## 📥 Step 4: Upload Project Files

### Option A: Using Git (Recommended)
```bash
# Clone your repository
git clone https://github.com/yourusername/backend_multifolks.git .

# Or if you have a private repo
git clone https://your-repo-url.git .
```

### Option B: Using SCP (from your local machine)
```bash
# From your local machine, run:
scp -r /path/to/backend_multifolks-master/* username@your-vps-ip:/var/www/multifolks-backend/
```

### Option C: Using rsync (from your local machine)
```bash
rsync -avz --exclude 'venv' --exclude '__pycache__' /path/to/backend_multifolks-master/ username@your-vps-ip:/var/www/multifolks-backend/
```

## 🐍 Step 5: Set Up Python Virtual Environment

```bash
cd /var/www/multifolks-backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Step 6: Configure Environment Variables

```bash
# Create .env file
nano .env
```

Add the following content (adjust values as needed):

```env
# MongoDB Configuration
MONGO_URI=mongodb+srv://username:password@cluster0.mongodb.net/
DATABASE_NAME=gaMultilens
COLLECTION_NAME=accounts_login

# JWT Configuration (CHANGE THIS IN PRODUCTION!)
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars

# Server Configuration
HOST=0.0.0.0
PORT=5000
DEBUG=False

# Stripe Configuration
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Payment URLs
CURRENCY=gbp
PAYMENT_SUCCESS_URL=https://yourdomain.com/thank-you
PAYMENT_CANCEL_URL=https://yourdomain.com/payment/cancel

# BlueDart Delivery Configuration
BLUEDART_BASE_URL=https://netconnect.bluedart.com/Ver1.10/
BLUEDART_CUSTOMER_CODE=your_customer_code
BLUEDART_LOGIN_ID=your_login_id
BLUEDART_LICENSE_KEY=your_license_key

# Warehouse Configuration
WAREHOUSE_PINCODE=122001
WAREHOUSE_ADDRESS_LINE1=Plot A-8, Infocity 1
WAREHOUSE_ADDRESS_LINE2=Sector 34
WAREHOUSE_ADDRESS_LINE3=Gurgaon, Haryana 122002
WAREHOUSE_PHONE=0124-6101010

# MSG91 Configuration
MSG91_AUTH_KEY=your_msg91_auth_key
MSG91_DOMAIN=email.multifolks.com
MSG91_TEMPLATE_ID=request_for_otp
MSG91_RESET_TEMPLATE_ID=forgot_password_46592
MSG91_WELCOME_TEMPLATE_ID=welcome_emailer_new
MSG91_ORDER_TEMPLATE_ID=order_placed_23
MSG91_SENDER_EMAIL=support@multifolks.com
MSG91_SENDER_NAME=Multifolks
```

**Save and exit:** `Ctrl+X`, then `Y`, then `Enter`

## 🔒 Step 7: Secure the .env File

```bash
# Set proper permissions (only owner can read/write)
chmod 600 .env

# Verify
ls -la .env
```

## 🚀 Step 8: Test the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Test run (in foreground to check for errors)
python app.py
```

If it runs successfully, press `Ctrl+C` to stop it.

## 🔄 Step 9: Set Up Systemd Service (Auto-start on boot)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/multifolks-backend.service
```

Add the following content:

```ini
[Unit]
Description=Multifolks FastAPI Backend
After=network.target mongod.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/multifolks-backend
Environment="PATH=/var/www/multifolks-backend/venv/bin"
ExecStart=/var/www/multifolks-backend/venv/bin/python /var/www/multifolks-backend/app.py
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=multifolks-backend

[Install]
WantedBy=multi-user.target
```

**Note:** If you're not using `www-data` user, replace it with your username.

Enable and start the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable multifolks-backend

# Start the service
sudo systemctl start multifolks-backend

# Check status
sudo systemctl status multifolks-backend

# View logs
sudo journalctl -u multifolks-backend -f
```

## 🌐 Step 10: Configure Nginx Reverse Proxy

Create Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/multifolks-backend
```

Add the following content:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # If you don't have a domain, use your VPS IP
    # server_name _;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

Enable the site:

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/multifolks-backend /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Enable Nginx to start on boot
sudo systemctl enable nginx
```

## 🔐 Step 11: Set Up SSL with Let's Encrypt (Optional but Recommended)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Certbot will automatically configure Nginx and set up auto-renewal
```

## 🔥 Step 12: Configure Firewall

```bash
# Allow SSH (if not already allowed)
sudo ufw allow 22/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

## 📊 Step 13: Set Up Logging

Create log directory:

```bash
sudo mkdir -p /var/log/multifolks-backend
sudo chown www-data:www-data /var/log/multifolks-backend
```

## 🔍 Step 14: Verify Deployment

1. **Check service status:**
   ```bash
   sudo systemctl status multifolks-backend
   ```

2. **Check Nginx status:**
   ```bash
   sudo systemctl status nginx
   ```

3. **Test API endpoint:**
   ```bash
   curl http://localhost:5000/api/health
   # Or from your browser: http://your-vps-ip/api/health
   ```

4. **View logs:**
   ```bash
   # Application logs
   sudo journalctl -u multifolks-backend -n 50 --no-pager
   
   # Nginx logs
   sudo tail -f /var/log/nginx/access.log
   sudo tail -f /var/log/nginx/error.log
   ```

## 🛠️ Useful Commands

### Service Management
```bash
# Start service
sudo systemctl start multifolks-backend

# Stop service
sudo systemctl stop multifolks-backend

# Restart service
sudo systemctl restart multifolks-backend

# View logs
sudo journalctl -u multifolks-backend -f

# View last 100 lines
sudo journalctl -u multifolks-backend -n 100
```

### Update Application
```bash
cd /var/www/multifolks-backend

# Pull latest changes (if using Git)
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install new dependencies (if any)
pip install -r requirements.txt

# Restart service
sudo systemctl restart multifolks-backend
```

### Nginx Management
```bash
# Test configuration
sudo nginx -t

# Reload Nginx (without downtime)
sudo systemctl reload nginx

# Restart Nginx
sudo systemctl restart nginx
```

## 🔒 Security Best Practices

1. **Change default SSH port** (optional but recommended)
2. **Use SSH keys** instead of passwords
3. **Keep system updated:** `sudo apt update && sudo apt upgrade`
4. **Use strong SECRET_KEY** in `.env` file
5. **Restrict MongoDB access** to specific IPs
6. **Regular backups** of database and code
7. **Monitor logs** regularly
8. **Use fail2ban** to prevent brute force attacks:
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   sudo systemctl start fail2ban
   ```

## 🐛 Troubleshooting

### Service won't start
```bash
# Check service status
sudo systemctl status multifolks-backend

# Check logs for errors
sudo journalctl -u multifolks-backend -n 50

# Test manually
cd /var/www/multifolks-backend
source venv/bin/activate
python app.py
```

### Port already in use
```bash
# Find what's using port 5000
sudo lsof -i :5000
# or
sudo netstat -tulpn | grep 5000

# Kill the process if needed
sudo kill -9 <PID>
```

### Permission issues
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/multifolks-backend

# Fix permissions
sudo chmod -R 755 /var/www/multifolks-backend
sudo chmod 600 /var/www/multifolks-backend/.env
```

### MongoDB connection issues
- Verify MongoDB URI in `.env`
- Check MongoDB Atlas IP whitelist (add your VPS IP)
- Test connection: `mongosh "your-mongo-uri"`

### Nginx 502 Bad Gateway
- Check if backend service is running: `sudo systemctl status multifolks-backend`
- Check backend logs: `sudo journalctl -u multifolks-backend -n 50`
- Verify proxy_pass URL in Nginx config

## 📈 Monitoring (Optional)

### Install PM2 (Alternative to systemd)
```bash
# Install PM2
npm install -g pm2

# Create ecosystem file
nano ecosystem.config.js
```

```javascript
module.exports = {
  apps: [{
    name: 'multifolks-backend',
    script: 'app.py',
    interpreter: 'venv/bin/python',
    cwd: '/var/www/multifolks-backend',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    }
  }]
};
```

```bash
# Start with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 📝 Quick Reference

| Task | Command |
|------|---------|
| Start service | `sudo systemctl start multifolks-backend` |
| Stop service | `sudo systemctl stop multifolks-backend` |
| Restart service | `sudo systemctl restart multifolks-backend` |
| View logs | `sudo journalctl -u multifolks-backend -f` |
| Check status | `sudo systemctl status multifolks-backend` |
| Test API | `curl http://localhost:5000/api/health` |
| Reload Nginx | `sudo systemctl reload nginx` |

## 🎉 Deployment Complete!

Your backend should now be accessible at:
- **HTTP:** `http://your-vps-ip` or `http://yourdomain.com`
- **HTTPS:** `https://yourdomain.com` (if SSL configured)
- **API Health:** `http://your-vps-ip/api/health`
- **API Docs:** `http://your-vps-ip/docs`

---

**Need Help?** Check the logs first, then verify all configuration files are correct.

