from pathlib import Path

import pytest

from app.video_use.workspace import prepare_workspace


def test_prepare_workspace_copies_sources_and_writes_brief(tmp_path: Path):
    source = tmp_path / "generated.mp4"
    source.write_bytes(b"video-data")

    workspace = prepare_workspace(
        task_dir=tmp_path / "task-1",
        video_files=[str(source)],
        subject="AI update",
        script="A short narration.",
    )

    assert workspace.path == tmp_path / "task-1" / "video-use"
    assert [source.name for source in workspace.sources] == ["source-01.mp4"]
    assert workspace.sources[0].read_bytes() == b"video-data"
    assert "AI update" in workspace.brief_path.read_text(encoding="utf-8")
    assert "video-use skill" in workspace.command


def test_prepare_workspace_rejects_missing_source(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match="Generated video was not found"):
        prepare_workspace(task_dir=tmp_path, video_files=[str(tmp_path / "missing.mp4")])
