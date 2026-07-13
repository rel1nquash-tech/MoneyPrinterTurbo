from app.trends.registry import TrendTopic


_TOPICS = [
    TrendTopic(
        title="Agent Workflow Tools",
        description="Teams explore AI assistants that can plan, execute, and verify routine work.",
        score=93,
        category="ai",
    ),
    TrendTopic(
        title="On-device Model Experiments",
        description="Developers prototype smaller local models for faster private user experiences.",
        score=86,
        category="ai",
    ),
    TrendTopic(
        title="Synthetic Media Guardrails",
        description="Product teams discuss labeling and provenance patterns for generated content.",
        score=80,
        category="ai",
    ),
]


def get_daily_topics(limit: int) -> list[TrendTopic]:
    return _TOPICS[: max(limit, 0)]
