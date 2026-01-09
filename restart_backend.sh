#!/bin/bash
# Script to restart the backend server

echo "🔄 Restarting backend server..."

# Kill existing python app.py process
pkill -f "python.*app.py"
sleep 1

# Start the server
echo "🚀 Starting backend..."
cd /home/selfeey-india/Documents/AI_Projects/login_api
source ../aienv/bin/activate
python app.py
