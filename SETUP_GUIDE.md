# Multifolks Backend - Setup & Run Guide

This guide will help you set up and run the Multifolks FastAPI backend server.

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **MongoDB** connection (Atlas or local instance)
- **Git** (if cloning the repository)

## 🚀 Quick Start Guide

### Step 1: Navigate to Project Directory

```bash
cd C:\Users\ADMIN\Desktop\backend_multifolks-master
```

### Step 2: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

> **Note:** If you don't have a virtual environment, create one first:
> ```bash
> python -m venv venv
> ```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables (Optional)

Create a `.env` file in the project root (optional - defaults are set in `config.py`):

```env
# MongoDB Configuration
MONGO_URI=mongodb+srv://gaMultilens:gaMultilens@cluster0.mongodb.net/
DATABASE_NAME=gaMultilens
COLLECTION_NAME=accounts_login

# JWT Configuration
SECRET_KEY=your-secret-key-here

# Server Configuration
HOST=0.0.0.0
PORT=5000
DEBUG=True

# Stripe Configuration (if using payments)
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret

# MSG91 Configuration (if using email/SMS)
MSG91_AUTH_KEY=your_msg91_auth_key
MSG91_DOMAIN=email.multifolks.com
```

### Step 5: Run the Server

**Option 1: Direct Python execution (Recommended)**
```bash
python app.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app:app --host 0.0.0.0 --port 5000
```

### Step 6: Verify Server is Running

Open your browser or use curl/PowerShell to check:

**PowerShell:**
```powershell
Invoke-WebRequest -Uri http://localhost:5000/api/health -UseBasicParsing
```

**Browser:**
```
http://localhost:5000/api/health
```

**Expected Response:**
```json
{
  "success": true,
  "message": "API is running",
  "mongodb": "connected",
  "total_users": 123,
  "timestamp": "2025-12-25T05:55:25.511689+00:00"
}
```

## 📝 One-Line Quick Start (Windows PowerShell)

```powershell
cd C:\Users\ADMIN\Desktop\backend_multifolks-master; .\venv\Scripts\Activate.ps1; python app.py
```

## 🔧 Troubleshooting

### Issue: MongoDB Connection Failed

**Symptoms:** `"mongodb": "disconnected"` in health check

**Solutions:**
1. Check your MongoDB URI in `config.py` or `.env` file
2. Verify MongoDB server is running (if local)
3. Check network connectivity to MongoDB Atlas (if cloud)
4. Verify credentials are correct

### Issue: Port Already in Use

**Error:** `Address already in use` or `Port 5000 is already in use`

**Solutions:**
1. Change the port in `config.py` or `.env`:
   ```env
   PORT=5001
   ```
2. Or kill the process using port 5000:
   ```powershell
   # Find process
   netstat -ano | findstr :5000
   # Kill process (replace PID with actual process ID)
   taskkill /PID <PID> /F
   ```

### Issue: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Virtual Environment Not Found

**Solution:**
```bash
# Create new virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## 📚 Key Endpoints

Once the server is running, you can access:

- **Health Check:** `GET http://localhost:5000/api/health`
- **API Documentation:** `http://localhost:5000/docs` (Swagger UI)
- **Alternative Docs:** `http://localhost:5000/redoc` (ReDoc)

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

## 📦 Project Structure

```
backend_multifolks-master/
├── app.py                 # Main FastAPI application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create if needed)
├── venv/                 # Virtual environment
├── cart_service.py       # Cart management service
├── order_service.py      # Order management service
├── payment_service.py    # Payment processing service
├── product_service.py    # Product management service
└── ...                  # Other service files
```

## 🔐 Security Notes

- **Never commit** `.env` file to version control
- Change `SECRET_KEY` in production
- Use strong MongoDB credentials
- Keep API keys secure

## 🚀 Production Deployment

For production:
1. Set `DEBUG=False` in environment
2. Use a production-grade ASGI server (e.g., Gunicorn with Uvicorn workers)
3. Set up proper logging
4. Configure HTTPS
5. Use environment variables for all sensitive data

## 📞 Support

If you encounter issues:
1. Check the server logs in the terminal
2. Verify all environment variables are set correctly
3. Ensure MongoDB connection is working
4. Check that all dependencies are installed

---

**Last Updated:** December 2025
**Framework:** FastAPI
**Python Version:** 3.8+

