# Development Guide

This document provides instructions for setting up a local development environment, understanding the project structure, following coding conventions, and contributing new features.

---

# Table of Contents

- Prerequisites
- Clone the Repository
- Create a Virtual Environment
- Install Dependencies
- Configure Environment Variables
- Running the Application
- Project Structure
- Coding Guidelines
- Adding a New AI Provider
- Adding a New RSS Feed
- Logging
- Testing
- Deployment
- Troubleshooting

---

# Prerequisites

Before getting started, ensure the following software is installed.

| Software | Version |
|-----------|----------|
| Python | 3.12+ |
| Git | Latest |
| VS Code (Recommended) | Latest |

Optional:

- Oracle Cloud VM (for deployment)
- Telegram Bot
- Gemini API Key
- OpenAI API Key

---

# Clone the Repository

```bash
git clone https://github.com/harishbabus/AI-News-Telegram-Bot.git

cd AI-News-Telegram-Bot
```

---

# Create a Virtual Environment

## Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

## Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

To install any newly added packages:

```bash
pip install <package-name>

pip freeze > requirements.txt
```

---

# Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
BOT_TOKEN=xxxxxxxx

CHAT_ID=-100xxxxxxxx

AI_PROVIDER=gemini

GEMINI_API_KEY=xxxxxxxx

OPENAI_API_KEY=xxxxxxxx
```

Do **not** commit the `.env` file.

---

# Running the Application

Run the application from the project root.

```bash
python -m app.main
```

---

# Project Structure

```
AI-News-Telegram-Bot
│
├── app/
│   ├── main.py
│   └── config.py
│
├── common/
│   ├── logger.py
│   └── utils.py
│
├── news/
│   ├── fetcher.py
│   ├── formatter.py
│   └── sources.py
│
├── providers/
│
├── prompts/
│
├── services/
│
├── telegram/
│
├── scripts/
│
├── docs/
│
├── tests/
│
└── logs/
```

---

# Package Responsibilities

## app

Contains:

- Application entry point
- Configuration

---

## common

Shared utilities.

Examples:

- Logger
- Utility functions

---

## news

Responsible for:

- Reading RSS feeds
- Fetching articles
- Formatting articles

---

## providers

Contains implementations of supported AI providers.

Current providers:

- Gemini
- OpenAI

Future providers:

- Claude
- Azure OpenAI
- Ollama
- Hugging Face

---

## prompts

Contains reusable prompt templates used by AI providers.

Prompts should not be hardcoded inside providers.

---

## services

Contains business logic.

Example:

- News summarization

---

## telegram

Contains Telegram integration.

Responsibilities:

- Message formatting
- Sending messages
- Handling Telegram API communication

---

## scripts

Contains deployment and scheduling scripts.

Examples:

- deploy.sh
- run.sh

---

# Coding Guidelines

## Imports

Use absolute imports.

Good:

```python
from news.fetcher import get_latest_news
```

Avoid relative imports unless necessary.

---

## Functions

Keep functions focused on a single responsibility.

Example:

Good:

```python
fetch_news()

remove_duplicates()

format_news()

send_message()
```

Avoid writing one large function that performs multiple tasks.

---

## Logging

Use the shared logger.

```python
from common.logger import logger
```

Avoid using:

```python
print()
```

for production code.

---

## Error Handling

Catch expected exceptions.

Log meaningful messages.

Example:

```python
try:
    response = provider.generate_summary(news)
except Exception as e:
    logger.error(e)
```

---

# Adding a New AI Provider

The project follows the Provider Pattern.

Steps:

## 1

Create a new provider.

Example:

```
providers/claude_provider.py
```

---

## 2

Inherit from BaseProvider.

```python
class ClaudeProvider(BaseProvider):
```

---

## 3

Implement required methods.

Example:

```python
summarize()
```

---

## 4

Register the provider inside

```
provider_factory.py
```

Example:

```python
elif provider == "claude":
    return ClaudeProvider()
```

No other part of the application should require modification.

---

# Adding a New RSS Feed

Open

```
news/sources.py
```

Add the new RSS URL.

Example:

```python
RSS_FEEDS = [
    ...
]
```

The fetcher will automatically include it.

---

# Testing

Future unit tests will be located under

```
tests/
```

Run all tests.

```bash
pytest
```

---

# Deployment

Deployment is automated.

A push to the `main` branch triggers GitHub Actions, which:

- Connects to the Oracle Cloud VM
- Updates the repository
- Installs dependencies
- Leaves execution to the Linux Cron scheduler

Deployment details are documented in:

```
docs/DEPLOYMENT.md
```

---

# Troubleshooting

## ModuleNotFoundError

Run the project as:

```bash
python -m app.main
```

Do not execute:

```bash
python app/main.py
```

unless all imports are configured for direct execution.

---

## Missing Environment Variables

Verify the `.env` file exists.

Check:

- BOT_TOKEN
- CHAT_ID
- AI_PROVIDER
- GEMINI_API_KEY
- OPENAI_API_KEY

---

## Telegram Message Not Received

Verify:

- Bot token
- Chat ID
- Bot is added to the group
- Bot has permission to send messages

---

## Cron Job Not Running

Check:

```bash
crontab -l
```

Verify the cron service.

```bash
sudo systemctl status cron
```

Review cron logs.

```bash
grep CRON /var/log/syslog
```

---

# Development Workflow

Recommended workflow for new features.

1. Create a feature branch

```bash
git checkout -b feature/new-feature
```

2. Implement the feature

3. Test locally

```bash
python -m app.main
```

4. Commit changes

```bash
git add .

git commit -m "Add new feature"
```

5. Push

```bash
git push origin feature/new-feature
```

6. Merge into `main`

GitHub Actions will automatically deploy the latest version to the Oracle Cloud VM.

---

# Future Improvements

Planned enhancements include:

- Unit tests
- Docker support
- Slack notifications
- Email digest
- News categorization
- Duplicate detection improvements
- Historical archive
- Web dashboard

## Related Documentation

- README.md — Project overview and quick start
- ARCHITECTURE.md — System design and module interactions
- DEVELOPMENT.md — Local development and contribution guide
- DEPLOYMENT.md — Oracle Cloud deployment instructions
- CI_CD.md — Deployment automation pipeline

---

Happy Coding!
