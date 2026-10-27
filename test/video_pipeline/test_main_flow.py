"""Execute the actual generation block with UI/service fakes, without Streamlit imports."""
import ast
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import Mock

import pytest
from app.models.schema import VideoAspect, VideoParams
from app.video_pipeline.runner import render_variants


class Stop(Exception):
    pass


class UI(Mock):
    def stop(self):
        raise Stop()


def run_generation(formats, enabled=True, fail=False):
    source = Path("webui/Main.py").read_text(encoding="utf-8")
    block = next(n for n in ast.parse(source).body if isinstance(n, ast.If) and isinstance(n.test, ast.Name) and n.test.id == "start_button")
    state = {"completed_video_files": ["old.mp4"], "completed_video_task_id": "old", "completed_video_render_results": ["old"], "completed_video_task_ids": ["old"], "local_video_materials": [], "trend_prefill": "keep"}
    ui = UI()
    ui.session_state = state
    ui.spinner = lambda *a: nullcontext()
    calls = []
    def start(task_id, params):
        calls.append((task_id, params.video_aspect))
        if fail or (enabled and len(formats) > 1 and params.video_aspect == VideoAspect.square):
            return None
        return {"videos": [f"{task_id}.mp4"]}
    env = dict(start_button=True, st=ui, config=SimpleNamespace(save_config=lambda: None, app={"pexels_api_keys": "fake"}, ui={"hide_log": True}), uuid4=uuid4, params=VideoParams(video_subject="test", video_aspect=VideoAspect.portrait), enable_multi_format=enabled, selected_output_formats=formats, uploaded_audio_file=None, uploaded_files=[], logger=Mock(), utils=SimpleNamespace(to_json=lambda p: ""), tr=lambda x:x, scroll_to_bottom=lambda:None, open_task_folder=lambda x:None, tm=SimpleNamespace(start=start), render_variants=render_variants, VideoAspect=VideoAspect)
    try:
        exec(compile(ast.Module(body=[block], type_ignores=[]), "Main-generation", "exec"), env)
    except Stop:
        pass
    return state, calls, ui


@pytest.mark.parametrize("formats,enabled,expected", [(["9:16"], True, ["9:16"]), (["1:1"], True, ["1:1"]), (["16:9"], True, ["16:9"]), (["1:1", "16:9"], False, ["9:16"]), (["9:16", "1:1", "16:9"], True, ["9:16", "1:1", "16:9"]), (["9:16", "1:1"], True, ["9:16", "1:1"])])
def test_actual_generation_routes_and_preserves_identity(formats, enabled, expected):
    state, calls, ui = run_generation(formats, enabled)
    assert [aspect.value for _, aspect in calls] == expected
    assert state["trend_prefill"] == "keep"
    assert "old.mp4" not in state.get("completed_video_files", [])
    if len(expected) > 1:
        successful_ids = [task_id for task_id, aspect in calls if aspect != VideoAspect.square]
        assert state["completed_video_task_ids"] == successful_ids
        assert state["completed_video_files"] == [f"{task_id}.mp4" for task_id in successful_ids]
        assert state["completed_video_failures"][0].variant.key == "1:1"
        ui.warning.assert_called_once()
    else:
        assert "completed_video_render_results" not in state
        assert state["completed_video_task_id"] == calls[0][0]
        assert state["completed_video_files"] == [f"{calls[0][0]}.mp4"]


@pytest.mark.parametrize("formats,fail", [([], False), (["9:16"], True), (["9:16", "1:1"], True)])
def test_rejected_or_failed_attempt_clears_previous_outputs(formats, fail):
    state, calls, ui = run_generation(formats, fail=fail)
    assert "completed_video_files" not in state
    assert "completed_video_task_id" not in state
    assert "completed_video_render_results" not in state
    assert "completed_video_task_ids" not in state
    assert state["trend_prefill"] == "keep"
    ui.error.assert_called()
    if not formats:
        assert calls == []
