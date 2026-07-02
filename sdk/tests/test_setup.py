"""Tests for the setup handlers' merge logic, using a fake home directory."""
from __future__ import annotations

import json

from talos_sdk.setup import aider, vscode, zed


def test_vscode_setup_creates_config(tmp_path, monkeypatch):
    target = tmp_path / ".continue" / "config.json"
    monkeypatch.setattr(vscode, "vscode_continue_config", lambda: target)

    vscode.setup(api_key="talos_test")

    data = json.loads(target.read_text(encoding="utf-8"))
    titles = [m["title"] for m in data["models"]]
    assert "talos-auto" in titles


def test_vscode_setup_is_idempotent(tmp_path, monkeypatch):
    target = tmp_path / ".continue" / "config.json"
    monkeypatch.setattr(vscode, "vscode_continue_config", lambda: target)

    vscode.setup(api_key="talos_test")
    vscode.setup(api_key="talos_test_2")

    data = json.loads(target.read_text(encoding="utf-8"))
    matches = [m for m in data["models"] if m["title"] == "talos-auto"]
    assert len(matches) == 1
    assert matches[0]["apiKey"] == "talos_test_2"
    assert target.with_name("config.json.bak").exists()


def test_vscode_setup_preserves_other_models(tmp_path, monkeypatch):
    target = tmp_path / ".continue" / "config.json"
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps({"models": [{"title": "gpt-4o", "provider": "openai"}]}), encoding="utf-8")
    monkeypatch.setattr(vscode, "vscode_continue_config", lambda: target)

    vscode.setup(api_key="talos_test")

    titles = {m["title"] for m in json.loads(target.read_text(encoding="utf-8"))["models"]}
    assert titles == {"gpt-4o", "talos-auto"}


def test_zed_setup_merges_into_existing_settings(tmp_path, monkeypatch):
    target = tmp_path / "settings.json"
    target.write_text(json.dumps({"theme": "one-dark"}), encoding="utf-8")
    monkeypatch.setattr(zed, "zed_settings", lambda: target)

    zed.setup(api_key="talos_test")

    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["theme"] == "one-dark"
    assert data["language_models"]["openai"]["api_url"]
    names = [m["name"] for m in data["language_models"]["openai"]["available_models"]]
    assert "talos-auto" in names


def test_aider_setup_preserves_unrelated_keys(tmp_path, monkeypatch):
    target = tmp_path / ".aider.conf.yml"
    target.write_text("dark-mode: true\n", encoding="utf-8")
    monkeypatch.setattr(aider, "aider_conf", lambda: target)

    aider.setup(api_key="talos_test")

    content = target.read_text(encoding="utf-8")
    assert "dark-mode: true" in content
    assert "openai-api-key: talos_test" in content
    assert "model: openai/talos-auto" in content


def test_dry_run_does_not_write(tmp_path, monkeypatch):
    target = tmp_path / ".continue" / "config.json"
    monkeypatch.setattr(vscode, "vscode_continue_config", lambda: target)

    result = vscode.setup(api_key="talos_test", dry_run=True)

    assert not target.exists()
    assert "dry run" in result
