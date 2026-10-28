"""Opt-in offline smoke test using real tasks and FFmpeg (no LLM/TTS calls).

Run with the project's full runtime: .venv/Scripts/python scripts/validate_multi_format.py
Add --duration 8 --subtitles for longer sources and offline subtitle burn-in.
Subtitle mode uses the existing no-voice timeline, not synthesized speech.
Creates short synthetic fixtures and keeps outputs/report under storage.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.models.schema import MaterialInfo, VideoAspect, VideoParams
from app.config import config
from app.services import task
from app.utils import utils
from app.video_pipeline.runner import render_variants
from app.video_use.workspace import prepare_render_workspace
import imageio_ffmpeg
from moviepy import VideoFileClip


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=int, default=1, choices=range(1, 31),
                        help="Synthetic source/audio duration in seconds (1-30)")
    parser.add_argument("--subtitles", action="store_true",
                        help="Exercise offline no-voice subtitle generation and burn-in")
    args = parser.parse_args()
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
    for ffmpeg_args in (
        ["-f", "lavfi", "-i", "testsrc2=size=640x640:rate=10", "-t", str(args.duration), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(source)],
        ["-f", "lavfi", "-i", "sine=frequency=440:sample_rate=44100", "-t", str(args.duration), str(audio)],
    ):
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-n", *ffmpeg_args], check=True)
    original = {str(p): digest(p) for p in (source, audio)}
    params = VideoParams(
        video_subject="Offline multi-format validation",
        video_script="A short local rendering test.",
        video_source="local", video_materials=[MaterialInfo(provider="local", url=str(source))],
        custom_audio_file=str(audio), subtitle_enabled=False, bgm_type="", video_count=1,
        video_clip_duration=2, n_threads=2, video_aspect=VideoAspect.portrait,
    )
    if args.subtitles:
        # Use the real offline narration timeline, without downloading Whisper.
        config.app["subtitle_provider"] = "edge"
        params.custom_audio_file = None
        params.voice_name = "no-voice"
        params.subtitle_enabled = True
        params.font_name = "MicrosoftYaHeiBold.ttc"
        params.video_script = "Local video rendering keeps each format independent. Clear subtitles remain readable in vertical, square, and landscape videos. Original source files remain unchanged."
    report = {"session": session, "source_duration": args.duration,
              "subtitles": args.subtitles, "source_hashes": original, "runs": []}
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
            subtitle_file = Path(utils.task_dir(task_id)) / "subtitle.srt"
            if args.subtitles:
                assert subtitle_file.is_file() and "-->" in subtitle_file.read_text(encoding="utf-8")
            with VideoFileClip(filename) as clip:
                assert tuple(clip.size) == VideoAspect(aspect).to_resolution()
                assert clip.duration > 0 and clip.audio is not None
                if not args.subtitles:
                    assert clip.duration >= args.duration - 0.1
                clip.get_frame(0)
                if args.subtitles:
                    clip.save_frame(str(root / f"{len(formats)}-{aspect.replace(':', '-')}.png"), t=1)
                run["outputs"].append({"format": aspect, "task_id": task_id, "path": filename, "size": list(clip.size), "duration": clip.duration, "audio": True,
                                       "subtitle_path": str(subtitle_file) if args.subtitles else None})
        assert original == {p: digest(p) for p in original}, "Source files changed"
        report["runs"].append(run)
        (root / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"PASS: {formats}", flush=True)
    print(f"REPORT: {root / 'report.json'}", flush=True)


if __name__ == "__main__":
    main()
