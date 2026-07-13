from app.trends.registry import TrendTopic


_TOPICS = [
    TrendTopic(
        title="Championship Race Tightens",
        description="Late-season fixtures create fresh storylines around title pressure and squad depth.",
        score=91,
        category="football",
    ),
    TrendTopic(
        title="Rising Academy Forward",
        description="A young striker earns attention after a run of decisive substitute appearances.",
        score=84,
        category="football",
    ),
    TrendTopic(
        title="Transfer Window Watch",
        description="Clubs are linked with midfield reinforcements as planning starts for the next window.",
        score=78,
        category="football",
    ),
]


def get_daily_topics(limit: int) -> list[TrendTopic]:
    return _TOPICS[: max(limit, 0)]
