# v8.2 hardening patch

Apply over the current v8.1 working tree.

Changes:
- category relevance uses article content only, never feed/source labels;
- major claims from discovery-only publishers require corroboration from a stronger source;
- Google News landing pages get a best-effort publisher-link resolution pass before being marked unresolved;
- email briefing removes accidental Markdown `**` markers from Gemini output;
- focused v8.2 regression tests added.

Run after overlay:

    black .
    ruff check .
    mypy .
    pytest

Then run:

    python -m app.main
