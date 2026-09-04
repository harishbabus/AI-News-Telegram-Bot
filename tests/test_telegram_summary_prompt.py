from prompts.telegram_summary_prompt import build_telegram_summary_prompt
from tests.types import ArticleFactory


def test_telegram_prompt_has_editorial_sections(
    article_factory: ArticleFactory,
) -> None:
    prompt = build_telegram_summary_prompt([article_factory()])
    assert "🔥 TOP STORIES" in prompt
    assert "🛠️ NEW AI TOOLS" in prompt
    assert "🔬 RESEARCH HIGHLIGHTS" in prompt
    assert "🎯 WHY TODAY'S NEWS MATTERS" in prompt
    assert "Do not produce a raw article list." in prompt
    assert "No raw URLs" in prompt
