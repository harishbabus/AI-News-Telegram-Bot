from providers.provider_factory import ProviderFactory


def summarize_news(news):

    provider = ProviderFactory.get_provider()

    return provider.summarize(news)