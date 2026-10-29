"""TLS option contract without importing the video runtime."""
import ast
import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest


def tls_option(settings, root):
    tree = ast.parse(Path("app/services/material.py").read_text(encoding="utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_get_tls_verify")
    env = dict(os=os, config=SimpleNamespace(app=settings),
               utils=SimpleNamespace(root_dir=lambda: str(root)), logger=Mock())
    exec(compile(ast.Module(body=[node], type_ignores=[]), "tls-option", "exec"), env)
    return env["_get_tls_verify"]()


def test_default_tls_verification_remains_enabled(tmp_path):
    assert tls_option({}, tmp_path) is True


@pytest.mark.parametrize("relative", [True, False])
def test_ca_bundle_resolves_from_project_root(tmp_path, relative):
    bundle = tmp_path / "trusted.pem"
    bundle.write_text("test fixture")
    value = bundle.name if relative else str(bundle)
    assert tls_option({"tls_ca_bundle": value}, tmp_path) == str(bundle)


def test_missing_bundle_fails_without_disabling_verification(tmp_path):
    with pytest.raises(ValueError, match="existing PEM"):
        tls_option({"tls_ca_bundle": "missing.pem"}, tmp_path)


def test_explicit_legacy_disable_remains_supported(tmp_path):
    assert tls_option({"tls_verify": "false", "tls_ca_bundle": "missing.pem"}, tmp_path) is False
