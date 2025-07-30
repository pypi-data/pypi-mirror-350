# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Unified LiteLLM entry-point (Chunk-1).

Public helper
-------------
chat_completion(model: str | None, messages: list, **kw) -> Any
    • `model` None / "" defaults to "openai/gpt-4o-mini"
    • Thin sync wrapper around `litellm.completion`
"""

from __future__ import annotations

import logging
import os
from typing import Any, List, Union

import litellm
import requests

# runtime dependency injected by chunk-1

_log = logging.getLogger(__name__)

_DEFAULT_MODEL = "openai/o3"


# ------------------------------------------------------------------


class MyCustomLLM:
    """Custom Sharp_Boe LLM provider wrapper."""

    API_URL = "http://10.37.44.155:5000"

    def __init__(self) -> None:  # noqa: ANN101
        secret = os.getenv("SHARP_USER_SECRET")
        name = os.getenv("SHARP_USER_NAME")
        if not secret:
            raise ValueError("SHARP_USER_SECRET env var not set")
        if not name:
            raise ValueError("SHARP_USER_NAME env var not set")
        self.secret = secret
        self.name = name

    def completion(self, model: str, messages: list, **kwargs: Any) -> Any:  # noqa: ANN101, ANN401
        """Call the Sharp_Boe HTTP API for chat completions."""
        # Expect model format "sharp_boe/<model_name>"
        try:
            _, model_name = model.split("/", 1)
        except ValueError:
            raise ValueError(f"Invalid custom model string: {model!r}")
        url = f"{self.API_URL}/sharp/api/v4/generate"

        # Currently only supports myself as username, need to have more options
        payload = {
            "messages": messages,
            "model": model_name,
            "user_name": self.name,
            "user_secret": self.secret,
            **kwargs,
        }
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()


def chat_completion(
    *,
    model: Union[str, None] = None,
    messages: List[dict],
    **kwargs: Any,  # noqa: ANN401
) -> Any:  # noqa: ANN401
    """Route a chat completion through **LiteLLM**.

    Parameters
    ----------
    model
        Provider/model string (e.g. "openai/gpt-4o-mini").
        Falls back to `_DEFAULT_MODEL` when None / "".
    messages
        List of OpenAI-style chat messages.
    **kwargs
        Passed verbatim to `litellm.completion`.

    Returns
    -------
    The object returned by `litellm.completion` (sync).

    Raises
    ------
    ValueError
        If `messages` is empty / not a list or model is invalid.
    """
    if not isinstance(messages, list) or not messages:
        raise ValueError("messages must be a non-empty list")

    _model = model or _DEFAULT_MODEL
    # route custom Sharp_Boe provider
    if _model.startswith("sharp_boe/"):
        return MyCustomLLM().completion(_model, messages, **kwargs)

    if not isinstance(_model, str) or "/" not in _model:
        # Very lenient – just catch blatant mistakes; real validation is
        # delegated to LiteLLM which knows the registry.
        raise ValueError(f"Invalid model string {_model!r}")

    _log.debug("llm_router → %s  (%d msgs)", _model, len(messages))

    try:
        return litellm.completion(model=_model, messages=messages, **kwargs)
    except Exception as exc:  # noqa: BLE001
        # LiteLLM raises many specialised errors; we re-raise untouched
        _log.error("LiteLLM call failed: %s", exc)
        raise
