# Engineering Journal

This document records the major milestones, technical decisions, challenges, and lessons learned while building the **AI News Telegram Bot**.

The goal is to document not only **what** was built, but also **why** certain design decisions were made and **what was learned** throughout the development journey.

---

# Project Goal

The primary objective of this project is to gain hands-on experience in building and deploying a real-world AI application using Python.

The project combines several software engineering concepts including:

- Python programming
- REST APIs
- RSS feed processing
- Prompt Engineering
- Large Language Models (LLMs)
- Telegram Bot development
- Cloud deployment
- CI/CD automation
- Linux administration
- Git and GitHub
- Software architecture

---

# Learning Timeline

---

## Milestone 1 – Project Setup

### Objective

Create the initial project structure and establish version control.

### Completed

- Created GitHub repository
- Configured Python virtual environment
- Created initial project files
- Added requirements.txt
- Configured .gitignore

### Key Learnings

- Python virtual environments
- Dependency management
- Git basics
- GitHub repository management

---

## Milestone 2 – RSS Feed Integration

### Objective

Automatically fetch AI news from trusted RSS feeds.

### Completed

- Added RSS feed parser
- Integrated multiple AI news sources
- Parsed feed entries
- Normalized article format

### Challenges

- Different RSS formats
- Duplicate articles
- Missing metadata

### Key Learnings

- RSS parsing
- XML processing
- Data normalization

---

## Milestone 3 – Telegram Bot Integration

### Objective

Automatically send news to a Telegram group.

### Completed

- Created Telegram bot
- Integrated Telegram API
- Message formatting
- Message splitting for long posts

### Key Learnings

- Telegram Bot API
- HTTP requests
- Error handling

---

## Milestone 4 – AI Summarization

### Objective

Generate concise AI-powered news summaries.

### Completed

- Integrated Google Gemini
- Designed reusable prompts
- Generated daily summaries

### Challenges

- Prompt tuning
- Output formatting
- Token limits

### Key Learnings

- Prompt Engineering
- LLM APIs
- AI response optimization

---

## Milestone 5 – Multi-Provider Architecture

### Objective

Support multiple AI providers without changing application logic.

### Completed

- Implemented BaseProvider
- Created GeminiProvider
- Created OpenAIProvider
- Implemented ProviderFactory

### Design Decision

Applied the **Factory Design Pattern** to decouple provider selection from business logic.

### Key Learnings

- Object-oriented programming
- Design patterns
- Abstraction
- Polymorphism

---

## Milestone 6 – Project Refactoring

### Objective

Improve maintainability by reorganizing the project.

### Completed

Reorganized the project into packages:

- app
- common
- news
- providers
- prompts
- services
- telegram
- scripts
- docs
- tests

### Key Learnings

- Python packages
- Absolute imports
- Modular architecture
- Separation of concerns

---

## Milestone 7 – Oracle Cloud Deployment

### Objective

Deploy the application to a free cloud server.

### Completed

- Created Oracle Cloud account
- Provisioned Always Free VM
- Connected using SSH
- Configured Ubuntu environment
- Deployed application

### Challenges

- VM availability
- Public IP assignment
- SSH authentication

### Key Learnings

- Cloud infrastructure
- Linux server administration
- SSH
- Virtual machines

---

## Milestone 8 – Linux Cron Scheduler

### Objective

Run the application automatically every day.

### Completed

- Created run.sh
- Configured Cron
- Verified scheduled execution

### Challenges

- Cron path issues
- Python module execution
- File permissions

### Key Learnings

- Linux Cron
- Shell scripting
- Environment management

---

## Milestone 9 – Automated Deployment

### Objective

Deploy automatically after every Git push.

### Completed

- Configured GitHub Actions
- Added SSH deployment
- Created deploy.sh
- Automated dependency installation

### Challenges

- SSH authentication
- File permissions
- Git conflicts on server

### Key Learnings

- CI/CD
- GitHub Actions
- Automated deployment
- Deployment strategies

---

## Milestone 10 – Documentation

### Objective

Document the entire project.

### Completed

Created:

- README.md
- ARCHITECTURE.md
- DEVELOPMENT.md
- DEPLOYMENT.md
- CI_CD.md
- LEARNING_JOURNAL.md

### Key Learnings

- Technical writing
- Documentation standards
- Software architecture communication

---

# Major Technical Decisions

## Why Oracle Cloud?

Oracle Cloud Always Free provides a persistent virtual machine suitable for hosting the application without recurring infrastructure costs.

---

## Why Cron Instead of GitHub Scheduler?

Cron offers:

- Better reliability
- Runs independently of GitHub
- Simpler scheduling
- Full control over execution

GitHub Actions is used exclusively for deployment.

---

## Why Use the Provider Pattern?

Adding a new AI provider should require minimal code changes.

Current providers:

- Gemini
- OpenAI

Future providers can be added by implementing the same interface.

---

## Why Separate Prompt Templates?

Separating prompts from provider implementations improves:

- Maintainability
- Reusability
- Experimentation
- Version control

---

## Why Modular Packages?

Breaking the application into packages improves:

- Readability
- Maintainability
- Testing
- Scalability

---

# Challenges Faced

Some of the notable issues encountered during development include:

- Python import errors after refactoring
- Cron execution failures
- Oracle Cloud VM capacity limitations
- SSH deployment issues
- Git merge conflicts during deployment
- Executable permission problems
- API rate limiting
- Telegram message size limitations

Each challenge provided valuable practical experience in debugging and production troubleshooting.

---

# Skills Gained

Throughout this project, practical experience was gained in:

### Python

- Modules
- Packages
- Virtual environments
- Logging
- Exception handling

### AI

- Prompt Engineering
- LLM APIs
- AI provider abstraction

### Cloud

- Oracle Cloud Infrastructure
- Linux administration
- SSH
- Cron

### DevOps

- GitHub Actions
- Automated deployment
- CI/CD
- Git workflows

### Software Engineering

- Modular architecture
- Factory Pattern
- Configuration management
- Documentation
- Clean code principles

---

# Future Learning Goals

Planned areas for continued learning include:

- Docker
- Kubernetes
- FastAPI
- Redis
- PostgreSQL
- Unit testing with Pytest
- Integration testing
- Monitoring and observability
- Infrastructure as Code (Terraform)
- AWS and Azure cloud platforms

---

# Reflection

This project evolved from a simple Python script into a production-style application featuring:

- Modular architecture
- AI provider abstraction
- Cloud deployment
- Automated CI/CD
- Scheduled execution
- Comprehensive documentation

More importantly, it provided hands-on experience across the full software development lifecycle—from coding and debugging to deployment and maintenance.

The lessons learned during this project form a strong foundation for building more advanced AI-powered applications in the future.

---

# Next Project

The next milestone in this learning journey is to build increasingly sophisticated AI applications, focusing on:

- Retrieval-Augmented Generation (RAG)
- AI Agents
- Multi-agent systems
- Vector databases
- MCP (Model Context Protocol)
- Production-grade APIs
- Scalable cloud-native architectures

The knowledge and practices established in this project will serve as the foundation for those future projects.