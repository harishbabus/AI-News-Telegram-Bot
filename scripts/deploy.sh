#!/bin/bash
set -e

echo "===== Deployment started: $(date) ====="

cd /home/ubuntu/projects/AI-News-Telegram-Bot

echo "Fetching latest code..."
git fetch origin

echo "Resetting to origin/main..."
git reset --hard origin/main

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "===== Deployment completed ====="