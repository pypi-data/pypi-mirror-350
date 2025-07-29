# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Unique deterministic ID for one PersonalVibe invocation.

The identifier is easy to read **and** collision-safe:

    20250605_142233_e4a1d2c3

    <ISODATE>_<time>_<8-char random>

Down-stream code treats the instance as a string thanks to __str__().
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class RunContext:
    timestamp: datetime = field(default_factory=datetime.utcnow, repr=False)
    uuid_hex8: str = field(default_factory=lambda: uuid.uuid4().hex[:8], repr=False)

    @property
    def id(self: "RunContext") -> str:
        return f"{self.timestamp.strftime('%Y%m%d_%H%M%S')}_{self.uuid_hex8}"

    # stringification helper -------------------------------------------------
    def __str__(self: "RunContext") -> str:  # pragma: no cover
        return self.id
