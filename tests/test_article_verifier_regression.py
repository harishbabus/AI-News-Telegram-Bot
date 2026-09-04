from services.article_verifier import _ArticleHTMLParser


def test_meta_tag_without_name_property_or_itemprop_does_not_crash() -> None:
    parser = _ArticleHTMLParser()
    parser.feed(
        '<html><head><meta charset="utf-8"><title>Example</title></head><body><p>This is a sufficiently long paragraph of article content for parsing.</p></body></html>'
    )
    assert parser.title == "Example"
