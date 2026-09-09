# v8 Phase 1 patch

Apply these files on top of the locally cleaned v7.2 repository. Do not replace the whole repository with the earlier v8 ZIP.

Files changed for v8 Phase 1:
- app/main.py
- common/models.py
- news/fetcher.py
- news/sources.py
- prompts/news_summary_prompt.py
- services/article_verifier.py
- services/editorial_scoring.py (new)
- services/fallback_renderer.py
- tests/test_editorial_scoring.py (new)
- tests/test_main.py

After copying, run:

    black .
    ruff check .
    mypy .
    pytest

Then, only if all four pass:

    python -m app.main

The most useful runtime logs are the candidate counts, editorial shortlist scores, article verification summary, and the final email content.
