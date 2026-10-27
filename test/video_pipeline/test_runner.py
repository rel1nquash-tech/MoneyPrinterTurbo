from app.models.schema import VideoAspect, VideoParams
from app.video_pipeline.runner import render_variants


def test_render_variants_creates_one_task_per_selected_format():
    params = VideoParams(video_subject="test")
    calls = []

    def fake_start(task_id, variant_params):
        calls.append((task_id, variant_params.video_aspect))
        return {"videos": [f"/tmp/{variant_params.video_aspect.value}.mp4"]}

    results = render_variants(params, fake_start, ["9:16", "1:1", "16:9"])

    assert len(results) == 3
    assert len({task_id for task_id, _ in calls}) == 3
    assert [aspect for _, aspect in calls] == [
        VideoAspect.portrait,
        VideoAspect.square,
        VideoAspect.landscape,
    ]
    assert [result.variant.key for result in results] == ["9:16", "1:1", "16:9"]


def test_render_variants_skips_failed_tasks_and_keeps_successes():
    params = VideoParams(video_subject="test")
    calls = []

    def fake_start(task_id, variant_params):
        calls.append(variant_params.video_aspect)
        if variant_params.video_aspect == VideoAspect.square:
            return None
        return {"videos": ["ok.mp4"]}

    results = render_variants(params, fake_start, ["9:16", "1:1", "16:9"])

    assert len(calls) == 3
    assert [result.variant.key for result in results] == ["9:16", "16:9"]
    assert [video for result in results for video in result.videos] == ["ok.mp4", "ok.mp4"]


def test_render_variants_continues_after_task_raises():
    params = VideoParams(video_subject="test")
    calls = []

    def fake_start(task_id, variant_params):
        calls.append(variant_params.video_aspect)
        if variant_params.video_aspect == VideoAspect.square:
            raise RuntimeError("render failed")
        return {"videos": [f"{variant_params.video_aspect.value}.mp4"]}

    results = render_variants(params, fake_start, ["9:16", "1:1", "16:9"])

    assert len(calls) == 3
    assert [result.variant.key for result in results] == ["9:16", "16:9"]


def test_render_variants_skips_empty_video_lists():
    params = VideoParams(video_subject="test")

    def fake_start(task_id, variant_params):
        if variant_params.video_aspect == VideoAspect.square:
            return {"videos": []}
        return {"videos": [f"{variant_params.video_aspect.value}.mp4"]}

    results = render_variants(params, fake_start, ["9:16", "1:1", "16:9"])

    assert [result.variant.key for result in results] == ["9:16", "16:9"]


import pytest


@pytest.mark.parametrize("bad", [None, {}, [], "bad", {"videos": []}, {"videos": "a.mp4"}, {"videos": [None]}, {"videos": [""]}, {"videos": 1}])
def test_invalid_outputs_report_failure_and_continue(bad):
    failures = []
    calls = []
    def start(task_id, params):
        calls.append(task_id)
        return bad if len(calls) == 1 else {"videos": ["ok.mp4"]}
    results = render_variants(VideoParams(video_subject="test"), start, ["9:16", "1:1"], failures=failures)
    assert len(results) == len(failures) == 1
    assert failures[0].task_id == calls[0]
    assert failures[0].variant.key == "9:16"
    assert failures[0].error
    assert results[0].task_id == calls[1]


def test_all_exceptions_report_each_format():
    failures = []
    def start(task_id, params):
        raise RuntimeError("encoder unavailable")
    assert render_variants(VideoParams(video_subject="test"), start, ["9:16", "1:1", "16:9"], failures=failures) == []
    assert [f.variant.key for f in failures] == ["9:16", "1:1", "16:9"]
    assert all(f.error == "encoder unavailable" for f in failures)
    assert len({f.task_id for f in failures}) == 3


def test_explicit_empty_selection_starts_no_tasks():
    def start(*args):
        pytest.fail("No task should start")
    assert render_variants(VideoParams(video_subject="test"), start, []) == []
