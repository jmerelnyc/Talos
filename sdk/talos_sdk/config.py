"""Shared defaults and environment resolution for the SDK and CLI."""
from __future__ import annotations

import os

DEFAULT_BASE_URL = "https://api.usetalos.xyz/v1"
DEFAULT_ANTHROPIC_BASE_URL = "https://api.usetalos.xyz"
DEFAULT_MODEL = "talos-auto"

API_KEY_ENV = "TALOS_API_KEY"
BASE_URL_ENV = "TALOS_BASE_URL"
MODEL_ENV = "TALOS_MODEL"


def resolve_api_key(explicit: str | None = None) -> str:
    key = explicit or os.environ.get(API_KEY_ENV)
    if not key:
        raise RuntimeError(
            f"No Talos API key found. Pass --api-key, or set {API_KEY_ENV}. "
            "Create one on your dashboard: https://usetalos.xyz/dashboard"
        )
    return key


def resolve_base_url(explicit: str | None = None, default: str = DEFAULT_BASE_URL) -> str:
    return explicit or os.environ.get(BASE_URL_ENV, default)


def resolve_model(explicit: str | None = None) -> str:
    return explicit or os.environ.get(MODEL_ENV, DEFAULT_MODEL)
