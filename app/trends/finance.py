from app.trends.registry import TrendTopic


_TOPICS = [
    TrendTopic(
        title="Rate Outlook Debate",
        description="Markets weigh inflation signals against expectations for future central bank moves.",
        score=89,
        category="finance",
    ),
    TrendTopic(
        title="Retail Earnings Focus",
        description="Investors look for consumer spending clues in upcoming quarterly reports.",
        score=82,
        category="finance",
    ),
    TrendTopic(
        title="Clean Energy Capital Flows",
        description="Mock market chatter highlights renewed interest in grid and storage infrastructure.",
        score=76,
        category="finance",
    ),
]


def get_daily_topics(limit: int) -> list[TrendTopic]:
    return _TOPICS[: max(limit, 0)]
