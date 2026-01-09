# 🚀 VPS Quick Start Guide

## Prerequisites Checklist
- [ ] VPS server with Ubuntu 20.04/22.04
- [ ] SSH access to VPS
- [ ] MongoDB Atlas account (or local MongoDB)
- [ ] Domain name (optional)

## Quick Deployment (3 Methods)

### Method 1: Automated Script (Easiest)

1. **Upload deploy.sh to your VPS:**
   ```bash
   scp deploy.sh username@your-vps-ip:~/
   ```

2. **SSH into your VPS:**
   ```bash
   ssh username@your-vps-ip
   ```

3. **Make script executable and run:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. **Follow the prompts and upload your project files**

### Method 2: Manual Step-by-Step

1. **Connect to VPS:**
   ```bash
   ssh username@your-vps-ip
   ```

2. **Install dependencies:**
   ```bash
   sudo apt update && sudo apt install -y python3 python3-pip python3-venv git nginx
   ```

3. **Upload project files:**
   ```bash
   # From your local machine:
   rsync -avz --exclude 'venv' --exclude '__pycache__' \
     /path/to/backend_multifolks-master/ \
     username@your-vps-ip:/var/www/multifolks-backend/
   ```

4. **Set up on VPS:**
   ```bash
   cd /var/www/multifolks-backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Create .env file:**
   ```bash
   nano .env
   # Add your configuration (see VPS_DEPLOYMENT_GUIDE.md)
   chmod 600 .env
   ```

6. **Set up systemd service:**
   ```bash
   sudo cp multifolks-backend.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable multifolks-backend
   sudo systemctl start multifolks-backend
   ```

7. **Set up Nginx:**
   ```bash
   sudo cp nginx-config.conf /etc/nginx/sites-available/multifolks-backend
   sudo nano /etc/nginx/sites-available/multifolks-backend
   # Edit server_name to match your domain/IP
   sudo ln -s /etc/nginx/sites-available/multifolks-backend /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Method 3: Using PM2 (Alternative)

```bash
# Install Node.js and PM2
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g pm2

# Set up project
cd /var/www/multifolks-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create PM2 config
cat > ecosystem.config.js <<EOF
module.exports = {
  apps: [{
    name: 'multifolks-backend',
    script: 'app.py',
    interpreter: 'venv/bin/python',
    cwd: '/var/www/multifolks-backend',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
};
EOF

# Start with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Essential Commands

```bash
# Service management
sudo systemctl status multifolks-backend
sudo systemctl restart multifolks-backend
sudo journalctl -u multifolks-backend -f

# Nginx
sudo nginx -t
sudo systemctl restart nginx

# Test API
curl http://localhost:5000/api/health
```

## SSL Setup (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Firewall Setup

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Verification

1. **Check service:** `sudo systemctl status multifolks-backend`
2. **Check logs:** `sudo journalctl -u multifolks-backend -n 50`
3. **Test API:** `curl http://your-vps-ip/api/health`
4. **Check Nginx:** `sudo systemctl status nginx`

## Troubleshooting

**Service won't start?**
```bash
sudo journalctl -u multifolks-backend -n 50
cd /var/www/multifolks-backend
source venv/bin/activate
python app.py  # Test manually
```

**502 Bad Gateway?**
- Check if backend is running: `sudo systemctl status multifolks-backend`
- Check backend logs
- Verify Nginx proxy_pass URL

**Permission issues?**
```bash
sudo chown -R www-data:www-data /var/www/multifolks-backend
```

For detailed guide, see [VPS_DEPLOYMENT_GUIDE.md](VPS_DEPLOYMENT_GUIDE.md)

