"""Thin wrapper around the official OpenAI SDK with Talos defaults baked in,
so you do not have to repeat the base URL and model everywhere.
"""
from __future__ import annotations

from typing import Any, Iterator

from .config import resolve_api_key, resolve_base_url, resolve_model


class Client:
    """A talos-auto client that behaves like the OpenAI SDK, pointed at Talos.

    All arguments are optional: with none given, the API key comes from
    `TALOS_API_KEY`, the base URL defaults to the hosted gateway, and the
    model defaults to `talos-auto`.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "talos_sdk.Client needs the `openai` package: pip install openai"
            ) from exc

        self.model = resolve_model(model)
        self._openai = OpenAI(
            api_key=resolve_api_key(api_key),
            base_url=resolve_base_url(base_url),
        )

    @property
    def chat(self) -> Any:
        """Escape hatch: the underlying OpenAI `chat` namespace, for full control."""
        return self._openai.chat

    def ask(self, prompt: str, **kwargs: Any) -> str:
        """Send a single prompt, return the full text reply (no streaming)."""
        response = self._openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return response.choices[0].message.content or ""

    def stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        """Send a single prompt, yield text chunks as they arrive."""
        chunks = self._openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            **kwargs,
        )
        for chunk in chunks:
            delta = chunk.choices[0].delta.content or ""
            if delta:
                yield delta
