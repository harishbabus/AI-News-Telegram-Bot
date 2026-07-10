#!/bin/bash
set -e

echo "===== Deployment started: $(date) ====="

cd /home/ubuntu/projects/AI-News-Telegram-Bot

git fetch origin
git reset --hard origin/main

source .venv/bin/activate

pip install -r requirements.txt

echo "===== Deployment completed ====="