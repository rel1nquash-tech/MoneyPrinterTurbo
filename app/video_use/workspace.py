"""Prepare MoneyPrinterTurbo output for an optional video-use editing pass."""

from dataclasses import dataclass
from pathlib import Path
import shutil


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
