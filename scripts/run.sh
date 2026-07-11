#!/bin/bash
set -e

PROJECT_DIR="/home/ubuntu/projects/AI-News-Telegram-Bot"
LOG_FILE="$PROJECT_DIR/logs/cron.log"

mkdir -p "$PROJECT_DIR/logs"

exec >> "$LOG_FILE" 2>&1

echo "===== Started $(date) ====="

cd "$PROJECT_DIR"

source .venv/bin/activate

python3 app.main.py

echo "===== Finished $(date) ====="