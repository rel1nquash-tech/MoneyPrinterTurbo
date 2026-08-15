import json

import pytest

import app.script_studio.generator as generator

from app.script_studio.generator import (
    PLATFORMS,
    _parse_json_object,
    _default_cta,
    build_platform_prompt,
    build_script_studio_prompt,
    generate_package,
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



def test_parse_json_object_recovers_first_of_multiple_embedded_objects():
    value = _parse_json_object(
        'Preamble {"title": "First"} trailing {"title": "Second"}'
    )
    assert value == {"title": "First"}


def test_default_cta_matches_requested_language():
    assert _default_cta("tr-TR") == "Daha fazlası için takip et."
    assert _default_cta("en-US") == "Follow for more."


def test_generate_package_falls_back_without_creating_unrequested_platforms(monkeypatch):
    monkeypatch.setattr(
        generator,
        "_generate_structured",
        lambda _prompt: {"title": "AI update", "hook": "", "script": "", "cta": ""},
    )
    monkeypatch.setattr(
        generator.llm,
        "generate_script",
        lambda **_kwargs: "Fallback narration. It is ready to record.",
    )

    package = generate_package(
        subject="AI",
        language="en-US",
        duration=45,
        platforms=[],
    )

    assert package.title == "AI update"
    assert package.hook == "Fallback narration"
    assert package.script == "Fallback narration. It is ready to record."
    assert package.cta == "Follow for more."
    assert package.platforms == {}


def test_generate_package_uses_core_copy_when_platform_metadata_is_invalid(monkeypatch):
    responses = iter(
        [
            {
                "title": "AI update",
                "hook": "Stop scrolling.",
                "script": "A concise factual script.",
                "cta": "Follow for more.",
            },
            {},
        ]
    )
    monkeypatch.setattr(generator, "_generate_structured", lambda _prompt: next(responses))

    package = generate_package(
        subject="AI",
        language="en-US",
        platforms=["tiktok"],
    )

    assert package.platforms["tiktok"].title == "AI update"
    assert package.platforms["tiktok"].caption == "A concise factual script."
    assert package.platforms["tiktok"].hashtags == []



def test_generate_package_raises_when_script_fallback_returns_an_error(monkeypatch):
    monkeypatch.setattr(generator, "_generate_structured", lambda _prompt: {})
    monkeypatch.setattr(
        generator.llm,
        "generate_script",
        lambda **_kwargs: "Error: openai: api_key is not set",
    )

    with pytest.raises(RuntimeError, match="api_key is not set"):
        generate_package(subject="AI", platforms=[])
