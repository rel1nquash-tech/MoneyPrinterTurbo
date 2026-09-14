import pytest

from app.video_pipeline.variants import (
    all_video_variants,
    get_video_variant,
    normalize_video_variants,
)


def test_all_video_variants_have_canonical_dimensions():
    variants = all_video_variants()
    assert [(v.key, v.width, v.height) for v in variants] == [
        ("9:16", 1080, 1920),
        ("1:1", 1080, 1080),
        ("16:9", 1920, 1080),
    ]


def test_get_video_variant_accepts_aspect_ratio_and_suffix():
    assert get_video_variant("9:16").suffix == "vertical"
    assert get_video_variant("VERTICAL").key == "9:16"
    assert get_video_variant("landscape").key == "16:9"


def test_normalize_video_variants_preserves_order_and_deduplicates():
    variants = normalize_video_variants(["9:16", "square", "9:16", "16:9"])
    assert [variant.key for variant in variants] == ["9:16", "1:1", "16:9"]


def test_normalize_video_variants_accepts_single_string():
    assert [v.key for v in normalize_video_variants("1:1")] == ["1:1"]


def test_unsupported_variant_raises_clear_error():
    with pytest.raises(ValueError, match="Unsupported video variant"):
        get_video_variant("4:3")
