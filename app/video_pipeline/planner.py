"""Pure planning helpers for multi-format video rendering.

The planner only prepares VideoParams variants. It does not start tasks or
change the existing video generation implementation.
"""

from app.models.schema import VideoAspect, VideoParams

from .variants import VideoVariant, normalize_video_variants


def build_render_variants(
    params: VideoParams, values=None
) -> list[tuple[VideoVariant, VideoParams]]:
    """Return independent VideoParams copies for the requested formats.

    When no formats are supplied, the current ``params.video_aspect`` is used,
    preserving the existing single-format behavior.
    """
    selected = values
    if selected is None:
        selected = [params.video_aspect.value if params.video_aspect else "9:16"]

    variants = normalize_video_variants(selected)
    return [
        (
            variant,
            params.copy(update={"video_aspect": VideoAspect(variant.key)}),
        )
        for variant in variants
    ]
