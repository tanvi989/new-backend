# 🚀 Quick Start - Multifolks Backend

## Windows PowerShell (One Command)

```powershell
cd C:\Users\ADMIN\Desktop\backend_multifolks-master; .\venv\Scripts\Activate.ps1; python app.py
```

## Step-by-Step

1. **Navigate to project:**
   ```powershell
   cd C:\Users\ADMIN\Desktop\backend_multifolks-master
   ```

2. **Activate virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Run server:**
   ```bash
   python app.py
   ```

4. **Verify it's running:**
   - Open browser: http://localhost:5000/api/health
   - Or PowerShell: `Invoke-WebRequest -Uri http://localhost:5000/api/health`

## Server URLs

- **API Base:** http://localhost:5000
- **Health Check:** http://localhost:5000/api/health
- **API Docs:** http://localhost:5000/docs
- **ReDoc:** http://localhost:5000/redoc

## Troubleshooting

- **Port in use?** Change `PORT=5001` in `config.py`
- **Module not found?** Run `pip install -r requirements.txt`
- **MongoDB disconnected?** Check `MONGO_URI` in `config.py`

For detailed guide, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

