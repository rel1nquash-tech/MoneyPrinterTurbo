"""Check audio dispatch without loading network TTS provider dependencies."""
import ast
from pathlib import Path
from typing import Union
from unittest.mock import Mock

import pytest


def duration_function():
    source = Path("app/services/voice.py").read_text(encoding="utf-8")
    function = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == "get_audio_duration")
    env = dict(Union=Union, SubMaker=type("SubMaker", (), {}), logger=Mock(),
               _get_audio_duration_from_mp3=Mock(return_value=1.5),
               _get_audio_duration_from_submaker=Mock(return_value=2.5))
    exec(compile(ast.Module(body=[function], type_ignores=[]), "audio-duration", "exec"), env)
    return env


@pytest.mark.parametrize("extension", ["mp3", "MP3", "wav", "m4a", "aac", "flac", "ogg"])
def test_supported_uploads_are_probed(extension):
    env = duration_function()
    filename = f"custom-audio.{extension}"
    assert env["get_audio_duration"](filename) == 1.5
    env["_get_audio_duration_from_mp3"].assert_called_once_with(filename)


def test_submaker_and_invalid_input_keep_existing_behavior():
    env = duration_function()
    assert env["get_audio_duration"](env["SubMaker"]()) == 2.5
    assert env["get_audio_duration"](None) == 0.0
    env["_get_audio_duration_from_mp3"].assert_not_called()
