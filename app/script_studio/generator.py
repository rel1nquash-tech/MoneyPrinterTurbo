"""High-level content package generation for AI Script Studio.

The module deliberately reuses MoneyPrinterTurbo's existing LLM service so the
studio works with every provider already supported by the application.
"""

from dataclasses import dataclass, field
import json
import re

from app.services import llm


PLATFORMS = (
    "tiktok",
    "instagram_reels",
    "youtube_shorts",
    "x",
    "threads",
    "linkedin",
)

PLATFORM_LABELS = {
    "tiktok": "TikTok",
    "instagram_reels": "Instagram Reels",
    "youtube_shorts": "YouTube Shorts",
    "x": "X",
    "threads": "Threads",
    "linkedin": "LinkedIn",
}


@dataclass
class PlatformCopy:
    title: str = ""
    caption: str = ""
    hashtags: list[str] = field(default_factory=list)


@dataclass
class ScriptPackage:
    title: str
    hook: str
    script: str
    cta: str
    platforms: dict[str, PlatformCopy] = field(default_factory=dict)


def _clean(value: object) -> str:
    return str(value or "").strip()


def _parse_json_object(text: str) -> dict:
    """Parse a JSON object from a provider response, tolerating code fences."""
    value = _clean(text)
    value = re.sub(r"^```(?:json)?\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s*```$", "", value)
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", value, flags=re.DOTALL)
        if not match:
            return {}
        try:
            parsed = json.loads(match.group(0))
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}


def _generate_structured(prompt: str) -> dict:
    """Use the existing LLM service and recover a JSON object from its text."""
    response = llm._generate_response(prompt)
    return _parse_json_object(response)


def build_script_studio_prompt(
    subject: str,
    language: str = "tr-TR",
    duration: int = 45,
    extra_requirements: str = "",
) -> str:
    return f"""You are an expert short-form social video editor.
Create a production-ready content package for this topic: {subject}
Language: {language}
Target duration: {duration} seconds

Return ONLY valid JSON with exactly these string fields:
- title: a strong, curiosity-driven title
- hook: the first 1-2 spoken sentences, designed to stop scrolling
- script: the complete spoken narration, natural and factual
- cta: a short call to action

Rules:
- Start directly with the hook; no greetings or meta commentary.
- Use the same language as the requested language.
- Keep claims grounded in the supplied topic; do not invent precise facts.
- The narration should fit the target duration.
- Do not use markdown in the values.
- {extra_requirements or 'Keep the tone clear, energetic and credible.'}
"""


def build_platform_prompt(
    subject: str,
    script: str,
    platform: str,
    language: str = "tr-TR",
) -> str:
    label = PLATFORM_LABELS.get(platform, platform)
    return f"""Create publishing copy for {label}.
Topic: {subject}
Script: {script}
Language: {language}

Return ONLY valid JSON with:
- title: platform-appropriate title
- caption: concise publishing caption
- hashtags: an array of relevant hashtags without duplicates

Tailor the style to {label}. Do not invent facts. No markdown in title or caption.
"""


def generate_package(
    subject: str,
    language: str = "tr-TR",
    duration: int = 45,
    platforms: list[str] | None = None,
    extra_requirements: str = "",
) -> ScriptPackage:
    """Generate the core script and platform-specific publishing metadata."""
    subject = _clean(subject)
    if not subject:
        raise ValueError("subject is required")

    selected = [p for p in (platforms or PLATFORMS) if p in PLATFORMS]
    if not selected:
        selected = list(PLATFORMS)

    core = _generate_structured(
        build_script_studio_prompt(
            subject=subject,
            language=language,
            duration=duration,
            extra_requirements=extra_requirements,
        )
    )

    title = _clean(core.get("title"))
    hook = _clean(core.get("hook"))
    script = _clean(core.get("script"))
    cta = _clean(core.get("cta"))

    if not script:
        # Keep a deterministic fallback through the existing script generator.
        script = llm.generate_script(
            video_subject=subject,
            language=language,
            paragraph_number=max(1, min(10, round(duration / 45))),
            video_script_prompt=extra_requirements,
        ).strip()
    if not title:
        title = subject
    if not hook:
        hook = script.split(".", 1)[0].strip() if script else subject
    if not cta:
        cta = "Daha fazlası için takip et."

    package = ScriptPackage(title=title, hook=hook, script=script, cta=cta)

    for platform in selected:
        metadata = _generate_structured(
            build_platform_prompt(
                subject=subject,
                script=f"{hook}\n\n{script}\n\n{cta}",
                platform=platform,
                language=language,
            )
        )
        hashtags = metadata.get("hashtags", [])
        if isinstance(hashtags, str):
            hashtags = hashtags.split()
        hashtags = [_clean(tag) for tag in hashtags if _clean(tag)]
        package.platforms[platform] = PlatformCopy(
            title=_clean(metadata.get("title")) or title,
            caption=_clean(metadata.get("caption")) or script,
            hashtags=hashtags,
        )

    return package
