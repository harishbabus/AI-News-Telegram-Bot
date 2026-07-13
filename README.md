# 🤖 AI News Telegram Bot

An AI-powered Telegram bot that automatically collects the latest Artificial Intelligence news from trusted RSS feeds, generates concise summaries using Large Language Models (LLMs), and delivers a daily digest directly to a Telegram chat.

The project is designed with a modular architecture, supports multiple AI providers, and includes automated deployment to an Oracle Cloud VM using GitHub Actions.

---

## ✨ Features

- 📰 Aggregates AI news from multiple RSS feeds
- 🤖 AI-powered news summarization
- 🔄 Multiple AI provider support
  - Google Gemini
  - OpenAI
- 📱 Telegram Bot integration
- 🕒 Automated daily scheduling using Linux Cron
- 🚀 Automatic deployment using GitHub Actions
- ☁️ Hosted on Oracle Cloud Always Free VM
- 🏗️ Modular and extensible project structure
- 📝 Centralized logging
- ⚙️ Environment-based configuration

---

## 📖 Why this Project?

Keeping up with the rapidly evolving AI ecosystem requires monitoring numerous news websites and blogs. This project automates that process by:

1. Collecting the latest AI news from trusted RSS feeds.
2. Removing duplicate articles.
3. Using an LLM to generate concise summaries.
4. Formatting the content into a readable daily digest.
5. Sending the digest directly to a Telegram group or channel.

Instead of browsing multiple websites every day, users receive a single curated summary in Telegram.

---

## 🏛️ High-Level Architecture

```text
                     +-----------------------+
                     |      RSS Feeds        |
                     +----------+------------+
                                |
                                v
                     +-----------------------+
                     |    News Fetcher       |
                     +----------+------------+
                                |
                                v
                     +-----------------------+
                     | Duplicate Removal     |
                     +----------+------------+
                                |
                                v
                     +-----------------------+
                     | News Formatter        |
                     +----------+------------+
                                |
                                v
                     +-----------------------+
                     | Summarizer Service    |
                     +----------+------------+
                                |
                                v
                     +-----------------------+
                     | Provider Factory      |
                     +----+-------------+----+
                          |             |
                          |             |
                    +-----v----+   +----v-----+
                    | Gemini   |   | OpenAI   |
                    +-----+----+   +----+-----+
                          |             |
                          +------+------+
                                 |
                                 v
                     +-----------------------+
                     | Telegram Bot          |
                     +----------+------------+
                                |
                                v
                     +-----------------------+
                     | Telegram Chat/Group   |
                     +-----------------------+
```

Detailed architecture is available in **docs/ARCHITECTURE.md**.

---

# 📂 Project Structure

```text
AI-News-Telegram-Bot
│
├── app/                # Application entry point and configuration
├── common/             # Shared utilities and logger
├── news/               # RSS fetching and formatting
├── providers/          # AI provider implementations
├── prompts/            # Prompt templates
├── services/           # Business services
├── telegram/           # Telegram integration
├── scripts/            # Deployment and scheduler scripts
├── docs/               # Documentation
├── tests/              # Unit tests
├── logs/               # Runtime logs
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🛠️ Technology Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.12 |
| AI Providers | Google Gemini, OpenAI |
| News Sources | RSS Feeds |
| Messaging | Telegram Bot API |
| Deployment | Oracle Cloud VM |
| Automation | GitHub Actions |
| Scheduler | Linux Cron |
| Version Control | Git & GitHub |

---

# 🚀 Getting Started

## Clone the repository

```bash
git clone https://github.com/harishbabus/AI-News-Telegram-Bot.git

cd AI-News-Telegram-Bot
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Configuration

Create a `.env` file in the project root.

Example:

```env
BOT_TOKEN=xxxxxxxxxxxxxxxx
CHAT_ID=-100xxxxxxxx
AI_PROVIDER=gemini
GEMINI_API_KEY=xxxxxxxxxxxxxxxx
OPENAI_API_KEY=xxxxxxxxxxxxxxxx
```

---

# ▶️ Running Locally

```bash
python -m app.main
```

---

# ☁️ Deployment

The production deployment consists of:

- Oracle Cloud Always Free VM
- Ubuntu Server
- GitHub Actions
- SSH Deployment
- Linux Cron Scheduler

Deployment documentation:

```
docs/DEPLOYMENT.md
```

---

# 🔄 CI/CD Pipeline

Every push to the **main** branch automatically:

1. Triggers GitHub Actions
2. Connects to Oracle VM over SSH
3. Pulls the latest code
4. Installs dependencies
5. Updates the production environment

The daily execution is performed by Linux Cron on the VM.

---

# 📅 Scheduler

The bot is executed every day using Cron.

Example:

```cron
30 0 * * * /home/ubuntu/projects/AI-News-Telegram-Bot/scripts/run.sh
```

(06:00 IST)

---

# 🧩 Supported AI Providers

Current providers:

- Google Gemini
- OpenAI

The architecture allows additional providers to be added with minimal changes.

Future providers may include:

- Anthropic Claude
- Azure OpenAI
- Ollama
- Hugging Face
- Groq
- GitHub trending AI repositories
- arXiv AI papers
- Reddit AI discussions

---

# 📚 Related Documentation

- README.md — Project overview and quick start
- ARCHITECTURE.md — System design and module interactions
- DEVELOPMENT.md — Local development and contribution guide
- DEPLOYMENT.md — Oracle Cloud deployment instructions
- CI_CD.md — Deployment automation pipeline

---

# 🛣️ Roadmap

### Completed

- RSS aggregation
- AI summarization
- Telegram integration
- Provider Factory
- Gemini support
- OpenAI support
- Oracle Cloud deployment
- GitHub Actions deployment
- Cron scheduler
- Modular project structure

### Planned

- Duplicate article detection improvements
- News categorization
- Multiple Telegram channels
- Weekly digest
- Docker support
- Unit testing
- Historical archive
- Web dashboard
- Email notifications
- Slack integration
- Logging and Metrics
- Configuration management
- LLM-powered summarization
- Future roadmap and screenshots


---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Please:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Harish Babu Subramanian**

Built as part of a hands-on journey to learn Python, software engineering practices, cloud deployment, CI/CD, and AI application development.

---

⭐ If you found this project useful, consider giving it a star on GitHub.