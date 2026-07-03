import json
from pathlib import Path
from typing import Any

from app.models.schema import VideoAspect, VideoConcatMode


CONTENT_PRESET = "worldcup_shorts"

DEFAULT_SAFE_BROLL_TERMS = [
    "football stadium crowd",
    "fans celebrating football",
    "football training field",
    "soccer ball close up",
    "stadium lights at night",
    "football boots grass",
    "national flag fans",
    "city skyline celebration",
    "football field aerial",
    "trophy celebration atmosphere",
]

SCRIPT_SYSTEM_PROMPT = """
You are a short-form football video editor creating World Cup Shorts.
Write energetic, factual English narration for a vertical, faceless short video.
Target a 30-50 second runtime.
Use only the facts supplied by the user. If a fact is missing, keep the line general.
Do not instruct anyone to use official match footage, broadcast clips, highlight reels,
or copyrighted player close-ups from matches.
Return only the spoken narration, with no markdown and no title.
""".strip()

SCRIPT_REQUIREMENTS_PROMPT = """
Create a 30-50 second English World Cup Short.
Use punchy narration with one clear hook, a factual middle, and a clean final line.
Keep it faceless and suitable for safe stock B-roll.
Do not mention or request copyrighted match footage, broadcast clips, or highlight reels.
""".strip()


def load_topics(path: str | Path) -> list[dict[str, Any]]:
    topic_path = Path(path)
    if not topic_path.exists():
        return []

    with topic_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def build_subject(topic: dict[str, Any]) -> str:
    match = str(topic.get("match", "")).strip()
    angle = str(topic.get("angle", "")).strip()
    facts = topic.get("facts", [])
    if not isinstance(facts, list):
        facts = [facts]

    fact_text = "; ".join(str(fact).strip() for fact in facts if str(fact).strip())

    parts = [f"World Cup short about {match}" if match else "World Cup short"]
    if angle:
        parts.append(f"Angle: {angle}")
    if fact_text:
        parts.append(f"Facts: {fact_text}")
    return ". ".join(parts)


def apply_worldcup_defaults(params):
    params.video_language = "en"
    params.video_aspect = VideoAspect.portrait.value
    params.video_count = getattr(params, "video_count", 1) or 1
    params.video_clip_duration = min(getattr(params, "video_clip_duration", 4) or 4, 4)
    params.video_concat_mode = VideoConcatMode.sequential.value
    params.match_materials_to_script = True
    params.subtitle_enabled = True

    if not getattr(params, "video_terms", None):
        params.video_terms = list(DEFAULT_SAFE_BROLL_TERMS)

    if not (getattr(params, "custom_system_prompt", "") or "").strip():
        params.custom_system_prompt = SCRIPT_SYSTEM_PROMPT

    if not (getattr(params, "video_script_prompt", "") or "").strip():
        params.video_script_prompt = SCRIPT_REQUIREMENTS_PROMPT

    return params
