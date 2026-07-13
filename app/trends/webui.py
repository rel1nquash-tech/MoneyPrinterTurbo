import json
from dataclasses import asdict

from app.trends.registry import TrendTopic, get_provider, list_providers


PROVIDER_LABELS = {
    "football": "Football",
    "finance": "Finance",
    "ai": "AI",
}


def get_provider_options() -> list[tuple[str, str]]:
    return [
        (name, PROVIDER_LABELS.get(name, name.title()))
        for name in list_providers()
    ]


def get_topics_for_providers(
    provider_names: list[str], limit_per_provider: int = 3
) -> list[TrendTopic]:
    topics = []
    for provider_name in provider_names:
        provider = get_provider(provider_name)
        topics.extend(provider.get_daily_topics(limit=limit_per_provider))
    return topics


def topic_to_dict(topic: TrendTopic) -> dict:
    return asdict(topic)


def topics_to_json(topics: list[TrendTopic]) -> str:
    return json.dumps(
        [topic_to_dict(topic) for topic in topics],
        ensure_ascii=False,
        indent=2,
    )
