#!/bin/bash

echo "=========================================="
echo "TESTING FRONTEND REGISTRATION"
echo "=========================================="
echo ""
echo "1. Frontend should now connect to localhost:5000"
echo "2. Open browser: http://localhost:3000"
echo "3. Try to register a new user"
echo "4. Watch this terminal for backend logs"
echo ""
echo "=========================================="
echo "WATCHING BACKEND LOGS..."
echo "=========================================="
echo ""

cd /home/selfeey-india/Documents/AI_Projects/login_api
tail -f backend.log | grep --line-buffered -E "REGISTRATION|WELCOME EMAIL|MSG91"
