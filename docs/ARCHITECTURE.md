This is my favorite document.

We'll explain:

Overall architecture
Why we chose Provider Pattern
Why prompts are separate
Why services exist
Why news is a package
Folder responsibilities

We'll also include diagrams.

Example:

RSS Feeds
     │
     ▼
News Fetcher
     │
     ▼
Formatter
     │
     ▼
Summarizer Service
     │
     ▼
Provider Factory
     │
 ┌──────┴─────────┐
 │                │
Gemini        OpenAI
 │                │
 └──────┬─────────┘
        ▼
Telegram Bot
        ▼
Telegram Channel