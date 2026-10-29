"""Exercise stream consumption without importing optional TTS providers."""
import ast
import asyncio
from pathlib import Path
from typing import Union

import pytest


def consume():
    tree = ast.parse(Path("app/services/voice.py").read_text(encoding="utf-8"))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "stream_edge_tts_chunks")
    env = {"asyncio": asyncio, "Union": Union}
    exec(compile(ast.Module(body=[function], type_ignores=[]), "stream-consumption", "exec"), env)
    return env["stream_edge_tts_chunks"]


def test_async_provider_error_is_not_masked_by_sync_wrapper():
    class Provider:
        async def stream(self):
            raise PermissionError("provider rejected request")
            yield

        def stream_sync(self):
            pytest.fail("Broken sync wrapper must not be selected")

    with pytest.raises(PermissionError, match="provider rejected"):
        consume()(Provider(), lambda chunk: None, timeout_seconds=1)


def test_async_chunks_are_forwarded_in_order():
    class Provider:
        async def stream(self):
            yield {"type": "audio", "data": b"audio"}
            yield {"type": "SentenceBoundary", "text": "test"}

    chunks = []
    consume()(Provider(), chunks.append, timeout_seconds=1)
    assert [chunk["type"] for chunk in chunks] == ["audio", "SentenceBoundary"]


def test_async_timeout_still_applies():
    class Provider:
        async def stream(self):
            await asyncio.sleep(60)
            yield

    with pytest.raises(TimeoutError):
        consume()(Provider(), lambda chunk: None, timeout_seconds=0.01)


def test_sync_only_provider_remains_supported():
    class Provider:
        def stream_sync(self):
            yield "legacy-chunk"

    chunks = []
    consume()(Provider(), chunks.append)
    assert chunks == ["legacy-chunk"]
