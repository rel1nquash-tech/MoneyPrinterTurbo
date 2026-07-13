from dataclasses import dataclass

from app.trends.registry import TrendTopic


@dataclass(frozen=True)
class TopicSeed:
    label: str
    theme: str
    detail: str
    tags: list[str]


@dataclass(frozen=True)
class TopicAngle:
    title: str
    hook: str
    description: str
    tags: list[str]


def build_topic_library(
    category: str,
    seeds: list[TopicSeed],
    angles: list[TopicAngle],
    voices: list[str],
) -> list[TrendTopic]:
    topics = []
    for seed_index, seed in enumerate(seeds, start=1):
        for angle_index, angle in enumerate(angles, start=1):
            topic_number = (seed_index - 1) * len(angles) + angle_index
            topics.append(
                TrendTopic(
                    id=f"{category}-{topic_number:03d}",
                    title=angle.title.format(
                        label=seed.label,
                        theme=seed.theme,
                    ),
                    hook=angle.hook.format(
                        label=seed.label,
                        theme=seed.theme,
                    ),
                    description=angle.description.format(
                        label=seed.label,
                        theme=seed.theme,
                        detail=seed.detail,
                    ),
                    score=100 - ((topic_number - 1) % 31),
                    estimated_duration=35 + ((topic_number - 1) % 6) * 5,
                    voice=voices[(topic_number - 1) % len(voices)],
                    category=category,
                    tags=sorted(set([category, seed.theme] + seed.tags + angle.tags)),
                )
            )
    return topics
