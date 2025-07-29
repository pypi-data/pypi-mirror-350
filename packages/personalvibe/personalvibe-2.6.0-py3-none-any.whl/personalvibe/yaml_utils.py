# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Utility helpers for **robust YAML loading** (Chunk-4).

Public API
----------
sanitize_yaml_text(text: str, *, origin: Union[str, None] = None) -> str
    • strips ASCII control chars 0x00-0x1F (except \n, \r, \t)
    • raises *ValueError* on any remaining surrogate code-points
"""

from __future__ import annotations

import re
from typing import Union

# Control characters excluding \n, \r, \t
_CTRL = "".join(chr(i) for i in range(32) if chr(i) not in "\n\r\t")
_CTRL_RE = re.compile(f"[{re.escape(_CTRL)}]")

# UTF-16 surrogate range (invalid in well-formed Unicode text)
_SURROGATE_RE = re.compile(r"[\uD800-\uDFFF]")


def sanitize_yaml_text(text: str, *, origin: Union[str, None] = None) -> str:
    """Strip *dangerous* runes before YAML parsing.

    Parameters
    ----------
    text
        Raw YAML string.
    origin
        Helpful file-path inserted into raised error messages.

    Returns
    -------
    str
        Cleaned text suitable for ``yaml.safe_load``.
    """
    cleaned = _CTRL_RE.sub(" ", text)

    # Surrogates should never appear in valid UTF-8 files
    m = _SURROGATE_RE.search(cleaned)
    if m:
        bad = repr(m.group(0))
        raise ValueError(f'Invalid Unicode rune {bad} found while reading YAML {origin or ""}'.strip())

    return cleaned
