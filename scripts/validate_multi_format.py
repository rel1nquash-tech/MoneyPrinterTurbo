"""Opt-in offline smoke test using real tasks and FFmpeg (no LLM/TTS calls).

Run with the project's full runtime: .venv/Scripts/python scripts/validate_multi_format.py
Creates short synthetic fixtures and keeps outputs/report under storage.
"""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.models.schema import MaterialInfo, VideoAspect, VideoParams
from app.services import task
from app.utils import utils
from app.video_pipeline.runner import render_variants
from app.video_use.workspace import prepare_render_workspace
import imageio_ffmpeg
from moviepy import VideoFileClip


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    # The smoke test must never publish synthetic outputs, even if configured.
    task.upload_post.upload_post_service.auto_upload = False
    session = str(uuid4())
    root = Path(utils.storage_dir("validation", create=True)) / session
    root.mkdir()
    source = Path(utils.storage_dir("local_videos", create=True)) / f"smoke-{session}.mp4"
    audio = root / "tone.wav"
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    for args in (
        ["-f", "lavfi", "-i", "testsrc2=size=640x640:rate=10", "-t", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(source)],
        ["-f", "lavfi", "-i", "sine=frequency=440:sample_rate=44100", "-t", "1", str(audio)],
    ):
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-n", *args], check=True)
    original = {str(p): digest(p) for p in (source, audio)}
    params = VideoParams(
        video_subject="Offline multi-format validation",
        video_script="A short local rendering test.",
        video_source="local", video_materials=[MaterialInfo(provider="local", url=str(source))],
        custom_audio_file=str(audio), subtitle_enabled=False, bgm_type="", video_count=1,
        video_clip_duration=2, n_threads=2, video_aspect=VideoAspect.portrait,
    )
    report = {"session": session, "source_hashes": original, "runs": []}
    for formats in (["9:16"], ["9:16", "1:1"], ["9:16", "1:1", "16:9"]):
        failures = []
        if len(formats) == 1:
            task_id = str(uuid4())
            result = task.start(task_id=task_id, params=params.model_copy(deep=True))
            assert result and result.get("videos"), "Single-format generation failed"
            outputs = [(formats[0], task_id, p) for p in result["videos"]]
        else:
            results = render_variants(params, lambda task_id, p: task.start(task_id=task_id, params=p), formats, failures=failures)
            assert not failures, failures
            assert len(results) == len(formats)
            outputs = [(r.variant.key, r.task_id, p) for r in results for p in r.videos]
            workspace = prepare_render_workspace(root / f"formats-{len(formats)}", results)
            assert all(digest(copy) == digest(original_path) for copy, (_, _, original_path) in zip(workspace.sources, outputs))
        run = {"formats": formats, "outputs": []}
        for aspect, task_id, filename in outputs:
            with VideoFileClip(filename) as clip:
                assert tuple(clip.size) == VideoAspect(aspect).to_resolution()
                assert clip.duration > 0 and clip.audio is not None
                clip.get_frame(0)
                run["outputs"].append({"format": aspect, "task_id": task_id, "path": filename, "size": list(clip.size), "duration": clip.duration, "audio": True})
        assert original == {p: digest(p) for p in original}, "Source files changed"
        report["runs"].append(run)
        (root / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"PASS: {formats}", flush=True)
    print(f"REPORT: {root / 'report.json'}", flush=True)


if __name__ == "__main__":
    main()
