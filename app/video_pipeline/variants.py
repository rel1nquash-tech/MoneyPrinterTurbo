"""Pure definitions for multi-format video output variants.

This module deliberately does not render videos. It provides a stable contract
for orchestration layers to request the supported social-video formats without
coupling the format choice to the existing video generation task.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VideoVariant:
    """A canonical output format for a generated video."""

    key: str
    label: str
    width: int
    height: int
    aspect_ratio: str
    suffix: str


VIDEO_VARIANTS: tuple[VideoVariant, ...] = (
    VideoVariant("9:16", "Vertical", 1080, 1920, "9:16", "vertical"),
    VideoVariant("1:1", "Square", 1080, 1080, "1:1", "square"),
    VideoVariant("16:9", "Landscape", 1920, 1080, "16:9", "landscape"),
)

_VARIANTS_BY_KEY = {variant.key: variant for variant in VIDEO_VARIANTS}
_VARIANTS_BY_SUFFIX = {variant.suffix: variant for variant in VIDEO_VARIANTS}


def get_video_variant(value: str) -> VideoVariant:
    """Resolve a variant by aspect-ratio key or filename-safe suffix."""
    normalized = str(value).strip().lower()
    if normalized in _VARIANTS_BY_KEY:
        return _VARIANTS_BY_KEY[normalized]
    if normalized in _VARIANTS_BY_SUFFIX:
        return _VARIANTS_BY_SUFFIX[normalized]
    raise ValueError(f"Unsupported video variant: {value}")


def normalize_video_variants(values) -> list[VideoVariant]:
    """Normalize user selections while preserving order and removing duplicates."""
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]

    result: list[VideoVariant] = []
    seen: set[str] = set()
    for value in values:
        variant = get_video_variant(value)
        if variant.key not in seen:
            result.append(variant)
            seen.add(variant.key)
    return result


def all_video_variants() -> tuple[VideoVariant, ...]:
    """Return all supported variants in the canonical UI order."""
    return VIDEO_VARIANTS
