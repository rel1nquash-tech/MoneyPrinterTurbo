from dataclasses import dataclass
from importlib import import_module
from typing import Protocol


@dataclass(frozen=True)
class TrendTopic:
    title: str
    description: str
    score: int
    category: str


class TrendProvider(Protocol):
    def get_daily_topics(self, limit: int) -> list[TrendTopic]:
        ...


_PROVIDERS: dict[str, str] = {
    "ai": "app.trends.ai",
    "finance": "app.trends.finance",
    "football": "app.trends.football",
}


def list_providers() -> list[str]:
    return sorted(_PROVIDERS)


def get_provider(name: str) -> TrendProvider:
    module_path = _PROVIDERS.get(name)
    if module_path is None:
        raise ValueError(f"Unknown trend provider: {name}")

    return import_module(module_path)
