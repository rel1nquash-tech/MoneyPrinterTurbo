"""Multi-format video rendering orchestration.

This module owns orchestration only: it creates one task per requested output
format and aggregates successful video results. The existing task implementation
remains untouched.
"""

from dataclasses import dataclass
from typing import Callable, Optional
from uuid import uuid4

from app.models.schema import VideoParams

from .planner import build_render_variants
from .variants import VideoVariant


@dataclass(frozen=True)
class VideoRenderResult:
    """Result from one output-format task."""

    variant: VideoVariant
    task_id: str
    videos: list[str]


def render_variants(
    params: VideoParams,
    start_task: Callable[[str, VideoParams], Optional[dict]],
    values=None,
) -> list[VideoRenderResult]:
    """Run one existing video task per selected format and aggregate videos.

    ``start_task`` is injected so this orchestration layer can be unit-tested
    without invoking the real video generation service.
    """
    results: list[VideoRenderResult] = []
    for variant, variant_params in build_render_variants(params, values):
        task_id = str(uuid4())
        result = start_task(task_id, variant_params)
        if not result or "videos" not in result:
            continue
        results.append(
            VideoRenderResult(
                variant=variant,
                task_id=task_id,
                videos=list(result.get("videos") or []),
            )
        )
    return results
