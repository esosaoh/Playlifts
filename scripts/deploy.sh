#!/bin/bash

set -e 

APP_DIR="/home/ec2-user/backend"

echo ">>> Deploying latest backend code..."
cd $APP_DIR

echo ">>> Pulling latest code from GitHub..."
git reset --hard
git pull origin main

echo ">>> Activating virtual environment..."
source venv/bin/activate

echo ">>> Installing dependencies..."
pip install -r requirements.txt

echo ">>> Restarting backend service..."
sudo systemctl restart api

echo ">>> Deployment complete!"
