#!/bin/bash

echo "Starting deployment..."

cd ~/projects/AI-News-Telegram-Bot

git pull origin main

source .venv/bin/activate

pip install -r requirements.txt

echo "Deployment complete."