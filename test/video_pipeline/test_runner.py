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
