from app.models.schema import VideoAspect, VideoParams
from app.video_pipeline.planner import build_render_variants


def test_build_render_variants_uses_current_aspect_by_default():
    params = VideoParams(video_subject="test", video_aspect=VideoAspect.landscape)

    planned = build_render_variants(params)

    assert len(planned) == 1
    variant, planned_params = planned[0]
    assert variant.key == "16:9"
    assert planned_params.video_aspect == VideoAspect.landscape


def test_build_render_variants_preserves_order_and_deduplicates():
    params = VideoParams(video_subject="test")

    planned = build_render_variants(params, ["9:16", "square", "9:16", "landscape"])

    assert [variant.key for variant, _ in planned] == ["9:16", "1:1", "16:9"]
    assert [planned_params.video_aspect for _, planned_params in planned] == [
        VideoAspect.portrait,
        VideoAspect.square,
        VideoAspect.landscape,
    ]


def test_build_render_variants_does_not_mutate_original_params():
    params = VideoParams(video_subject="test", video_aspect=VideoAspect.portrait)

    planned = build_render_variants(params, ["16:9"])

    assert params.video_aspect == VideoAspect.portrait
    assert planned[0][1] is not params
    assert planned[0][1].video_aspect == VideoAspect.landscape
