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


from app.models.schema import MaterialInfo
import pytest


@pytest.mark.parametrize("aspect", ["9:16", "1:1", "16:9"])
def test_single_format_resolution(aspect):
    variant, params = build_render_variants(VideoParams(video_subject="test"), [aspect])[0]
    assert params.video_aspect.to_resolution() == (variant.width, variant.height)


def test_default_params_and_nested_materials_are_isolated(tmp_path):
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"audio")
    material = tmp_path / "source.mp4"
    material.write_bytes(b"video")
    params = VideoParams(video_subject="test", custom_audio_file=str(audio), video_materials=[MaterialInfo(url=str(material))])
    assert build_render_variants(params)[0][0].key == "9:16"
    planned = build_render_variants(params, ["9:16", "1:1"])
    planned[0][1].video_materials[0].url = "changed"
    assert planned[1][1].video_materials[0].url == params.video_materials[0].url == str(material)
    assert all(p.custom_audio_file == str(audio) for _, p in planned)
    assert audio.read_bytes() == b"audio"
    assert material.read_bytes() == b"video"
