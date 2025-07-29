# Copyright © 2025 by Nick Jenkins. All rights reserved

"""OpenAI compatibility shims and migration tools (Chunk-5).

This module provides backwards compatibility for code transitioning
from direct OpenAI usage to LiteLLM. It's intended for temporary use
during migration; new code should use llm_router directly.
"""

import warnings
from typing import Any, Dict, List, Optional

from personalvibe import llm_router


# Create an alias to maintain backwards compatibility
def deprecation_warning(fn_name: str) -> None:
    warnings.warn(
        f"{fn_name} is deprecated and will be removed in a future version. " "Use llm_router.chat_completion instead.",
        DeprecationWarning,
        stacklevel=2,
    )


def openai_chat_completion(
    *,
    model: Optional[str] = None,
    messages: List[Dict[str, Any]],
    **kwargs: Any,  # noqa: ANN401
) -> Dict[str, Any]:
    """Deprecated OpenAI completion adapter.

    This function is a backward compatibility shim that translates
    OpenAI-style calls to llm_router.chat_completion. New code should
    use llm_router directly.
    """
    deprecation_warning("openai_chat_completion")

    # If model is specified without provider, add openai/ prefix
    if model and "/" not in model:
        model = f"openai/{model}"

    return llm_router.chat_completion(model=model, messages=messages, **kwargs)


# This is a placeholder for any other legacy functions that might need
# temporary compatibility wrappers during the transition period.
