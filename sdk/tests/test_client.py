"""Tests for the Client wrapper's defaults, without hitting the network."""
from __future__ import annotations

import pytest

from talos_sdk import Client
from talos_sdk.config import API_KEY_ENV


def test_client_uses_defaults(monkeypatch):
    monkeypatch.setenv(API_KEY_ENV, "talos_test")
    client = Client()
    assert client.model == "talos-auto"


def test_client_accepts_overrides():
    client = Client(api_key="talos_test", model="talos-llama-3.1-8b")
    assert client.model == "talos-llama-3.1-8b"


def test_client_requires_a_key(monkeypatch):
    monkeypatch.delenv(API_KEY_ENV, raising=False)
    with pytest.raises(RuntimeError):
        Client()
