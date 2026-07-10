#!/bin/bash

cd ~/projects/AI-News-Telegram-Bot

source .venv/bin/activate

python3 main.py >> logs/bot.log 2>&1