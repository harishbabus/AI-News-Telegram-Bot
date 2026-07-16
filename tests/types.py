# tests/types.py

from collections.abc import Callable

from common.models import NewsArticle

type ArticleFactory = Callable[..., NewsArticle]
