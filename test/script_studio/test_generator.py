import json

from app.script_studio.generator import (
    PLATFORMS,
    _parse_json_object,
    build_platform_prompt,
    build_script_studio_prompt,
)


def test_parse_json_object_accepts_code_fence():
    value = _parse_json_object('```json\n{"title": "Test", "hashtags": ["#test"]}\n```')
    assert value["title"] == "Test"
    assert value["hashtags"] == ["#test"]


def test_parse_json_object_recovers_embedded_object():
    value = _parse_json_object('Here is the result: {"title": "Test"}')
    assert value == {"title": "Test"}


def test_script_studio_prompt_contains_core_inputs():
    prompt = build_script_studio_prompt("AI", language="tr-TR", duration=45)
    assert "AI" in prompt
    assert "tr-TR" in prompt
    assert "45 seconds" in prompt
    assert "ONLY valid JSON" in prompt


def test_platform_prompt_contains_platform_and_schema():
    prompt = build_platform_prompt("AI", "Test script", "youtube_shorts")
    assert "YouTube Shorts" in prompt
    assert "hashtags" in prompt


def test_platform_registry_is_stable():
    assert "tiktok" in PLATFORMS
    assert "linkedin" in PLATFORMS
    assert len(set(PLATFORMS)) == len(PLATFORMS)

    # Ensure the expected JSON representation remains serializable for future API use.
    json.dumps(list(PLATFORMS))
