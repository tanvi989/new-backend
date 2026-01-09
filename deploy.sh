#!/bin/bash

# Multifolks Backend VPS Deployment Script
# Run this script on your VPS server

set -e  # Exit on error

echo "=========================================="
echo "  Multifolks Backend VPS Deployment"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}Please do not run as root. Use a regular user with sudo privileges.${NC}"
   exit 1
fi

# Variables
PROJECT_DIR="/var/www/multifolks-backend"
SERVICE_NAME="multifolks-backend"
NGINX_SITE="multifolks-backend"

echo -e "${GREEN}Step 1: Installing system dependencies...${NC}"
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor

echo -e "${GREEN}Step 2: Creating project directory...${NC}"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

echo -e "${GREEN}Step 3: Setting up Python virtual environment...${NC}"
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

echo -e "${YELLOW}Note: Please upload your project files to $PROJECT_DIR${NC}"
echo -e "${YELLOW}You can use: scp, rsync, or git clone${NC}"
read -p "Press Enter after you've uploaded the project files..."

if [ ! -f "$PROJECT_DIR/app.py" ]; then
    echo -e "${RED}Error: app.py not found in $PROJECT_DIR${NC}"
    echo -e "${RED}Please upload your project files first.${NC}"
    exit 1
fi

echo -e "${GREEN}Step 4: Installing Python dependencies...${NC}"
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo -e "${YELLOW}Warning: requirements.txt not found. Installing basic dependencies...${NC}"
    pip install fastapi uvicorn pymongo python-dotenv passlib PyJWT
fi

echo -e "${GREEN}Step 5: Creating systemd service...${NC}"
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=Multifolks FastAPI Backend
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/app.py
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=$SERVICE_NAME

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}Step 6: Creating Nginx configuration...${NC}"
read -p "Enter your domain name (or press Enter to use IP): " DOMAIN
if [ -z "$DOMAIN" ]; then
    DOMAIN="_"
fi

sudo tee /etc/nginx/sites-available/$NGINX_SITE > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/$NGINX_SITE /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true

echo -e "${GREEN}Step 7: Testing Nginx configuration...${NC}"
sudo nginx -t

echo -e "${GREEN}Step 8: Enabling and starting services...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME
sudo systemctl restart nginx

echo -e "${GREEN}Step 9: Configuring firewall...${NC}"
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
echo "y" | sudo ufw enable

echo ""
echo -e "${GREEN}=========================================="
echo "  Deployment Complete!"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}Important Next Steps:${NC}"
echo "1. Create .env file in $PROJECT_DIR with your configuration"
echo "2. Set proper permissions: chmod 600 $PROJECT_DIR/.env"
echo "3. Check service status: sudo systemctl status $SERVICE_NAME"
echo "4. View logs: sudo journalctl -u $SERVICE_NAME -f"
echo "5. Test API: curl http://localhost:5000/api/health"
echo ""
echo -e "${YELLOW}Optional: Set up SSL with Let's Encrypt${NC}"
echo "sudo apt install certbot python3-certbot-nginx"
echo "sudo certbot --nginx -d yourdomain.com"
echo ""
echo -e "${GREEN}Your backend should be running at: http://$(hostname -I | awk '{print $1}')${NC}"
