"""Prepare MoneyPrinterTurbo output for an optional video-use editing pass."""

from dataclasses import dataclass
import json
from pathlib import Path
import shutil

from app.video_pipeline.runner import VideoRenderResult


@dataclass(frozen=True)
class VideoUseWorkspace:
    """A self-contained directory that can be opened by a video-use agent."""

    path: Path
    sources: tuple[Path, ...]
    brief_path: Path

    @property
    def command(self) -> str:
        return (
            f'cd "{self.path}"\n'
            "claude\n"
            "Use the video-use skill to edit the source video(s). "
            "Read VIDEO_USE_BRIEF.md first and write the result to edit/final.mp4."
        )


def _source_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"Generated video was not found: {path}")
    return path


def prepare_workspace(
    task_dir: str | Path,
    video_files: list[str],
    subject: str = "",
    script: str = "",
) -> VideoUseWorkspace:
    """Copy generated videos and an editing brief into a video-use-ready folder."""
    if not video_files:
        raise ValueError("At least one generated video is required")

    workspace = Path(task_dir) / "video-use"
    workspace.mkdir(parents=True, exist_ok=True)

    copied_sources = []
    for index, video_file in enumerate(video_files, start=1):
        source = _source_path(video_file)
        destination = workspace / f"source-{index:02d}{source.suffix.lower() or '.mp4'}"
        shutil.copy2(source, destination)
        copied_sources.append(destination)

    brief = workspace / "VIDEO_USE_BRIEF.md"
    source_list = "\n".join(f"- {source.name}" for source in copied_sources)
    brief.write_text(
        "\n".join(
            [
                "# MoneyPrinterTurbo post-production brief",
                "",
                "## Source videos",
                source_list,
                "",
                "## Video subject",
                subject.strip() or "Not provided",
                "",
                "## Script",
                script.strip() or "Not provided",
                "",
                "## Editing request",
                (
                    "Use the video-use skill to improve pacing, remove awkward pauses, "
                    "apply consistent audio fades and color treatment, then render "
                    "edit/final.mp4. Review the source files before making cuts."
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )

    return VideoUseWorkspace(
        path=workspace,
        sources=tuple(copied_sources),
        brief_path=brief,
    )


def prepare_render_workspace(
    base_dir: str | Path,
    render_results: list[VideoRenderResult],
    subject: str = "",
    script: str = "",
) -> VideoUseWorkspace:
    """Aggregate multi-format render results into one safe video-use workspace.

    Each source keeps its output-format suffix and the workspace records the
    originating task ID in ``RENDER_MANIFEST.json``. This prevents a combined
    9:16/1:1/16:9 render from being treated as though all files belonged to one
    task directory.
    """
    if not render_results:
        raise ValueError("At least one successful render result is required")

    workspace = Path(base_dir) / "video-use"
    workspace.mkdir(parents=True, exist_ok=True)

    copied_sources: list[Path] = []
    manifest: list[dict[str, object]] = []

    for result in render_results:
        for index, video_file in enumerate(result.videos, start=1):
            source = _source_path(video_file)
            extension = source.suffix.lower() or ".mp4"
            destination = workspace / f"{result.variant.suffix}-{index:02d}{extension}"
            if destination.exists():
                raise FileExistsError(f"Render workspace source already exists: {destination}")
            shutil.copy2(source, destination)
            copied_sources.append(destination)
            manifest.append(
                {
                    "source": destination.name,
                    "variant": result.variant.key,
                    "task_id": result.task_id,
                    "original_path": str(source),
                }
            )

    if not copied_sources:
        raise ValueError("Render results contain no video files")

    brief = workspace / "VIDEO_USE_BRIEF.md"
    source_list = "\n".join(
        f"- {entry['source']} ({entry['variant']}, task {entry['task_id']})"
        for entry in manifest
    )
    brief.write_text(
        "\n".join(
            [
                "# MoneyPrinterTurbo multi-format post-production brief",
                "",
                "## Source videos",
                source_list,
                "",
                "## Video subject",
                subject.strip() or "Not provided",
                "",
                "## Script",
                script.strip() or "Not provided",
                "",
                "## Editing request",
                (
                    "Review the available format variants and choose the best source(s) "
                    "for the requested edit. Keep the source aspect ratio unless a crop "
                    "is explicitly needed, then render edit/final.mp4."
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )
    (workspace / "RENDER_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return VideoUseWorkspace(
        path=workspace,
        sources=tuple(copied_sources),
        brief_path=brief,
    )
