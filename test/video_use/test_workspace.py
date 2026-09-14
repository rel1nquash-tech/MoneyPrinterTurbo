import json
from pathlib import Path

import pytest

from app.video_pipeline.runner import VideoRenderResult
from app.video_pipeline.variants import all_video_variants
from app.video_use.workspace import prepare_render_workspace, prepare_workspace


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


def test_prepare_render_workspace_keeps_format_and_task_identity(tmp_path: Path):
    sources = {}
    for suffix in ("vertical", "square", "landscape"):
        source = tmp_path / f"{suffix}-generated.mp4"
        source.write_bytes(suffix.encode("utf-8"))
        sources[suffix] = source

    variants = {variant.suffix: variant for variant in all_video_variants()}
    results = [
        VideoRenderResult(variants["vertical"], "task-v", [str(sources["vertical"])]),
        VideoRenderResult(variants["square"], "task-s", [str(sources["square"])]),
        VideoRenderResult(variants["landscape"], "task-l", [str(sources["landscape"])]),
    ]

    workspace = prepare_render_workspace(
        base_dir=tmp_path / "render-session",
        render_results=results,
        subject="Multi-format test",
        script="A format-aware script.",
    )

    assert workspace.path == tmp_path / "render-session" / "video-use"
    assert [source.name for source in workspace.sources] == [
        "vertical-01.mp4",
        "square-01.mp4",
        "landscape-01.mp4",
    ]
    assert workspace.sources[0].read_bytes() == b"vertical"
    assert workspace.sources[1].read_bytes() == b"square"
    assert workspace.sources[2].read_bytes() == b"landscape"

    manifest = json.loads(
        (workspace.path / "RENDER_MANIFEST.json").read_text(encoding="utf-8")
    )
    assert [(entry["variant"], entry["task_id"]) for entry in manifest] == [
        ("9:16", "task-v"),
        ("1:1", "task-s"),
        ("16:9", "task-l"),
    ]
    brief = workspace.brief_path.read_text(encoding="utf-8")
    assert "vertical-01.mp4 (9:16, task task-v)" in brief
    assert "Multi-format test" in brief


def test_prepare_render_workspace_rejects_empty_results(tmp_path: Path):
    with pytest.raises(ValueError, match="At least one successful render result"):
        prepare_render_workspace(tmp_path, [])


def test_prepare_render_workspace_rejects_results_without_videos(tmp_path: Path):
    result = VideoRenderResult(all_video_variants()[0], "task-v", [])
    with pytest.raises(ValueError, match="contain no video files"):
        prepare_render_workspace(tmp_path, [result])


def test_prepare_render_workspace_rejects_duplicate_destination(tmp_path: Path):
    source_a = tmp_path / "a.mp4"
    source_b = tmp_path / "b.mp4"
    source_a.write_bytes(b"a")
    source_b.write_bytes(b"b")
    variant = all_video_variants()[0]
    results = [
        VideoRenderResult(variant, "task-a", [str(source_a)]),
        VideoRenderResult(variant, "task-b", [str(source_b)]),
    ]

    with pytest.raises(FileExistsError, match="already exists"):
        prepare_render_workspace(tmp_path, results)
