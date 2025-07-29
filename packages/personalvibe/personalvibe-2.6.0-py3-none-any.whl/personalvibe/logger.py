# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Opinionated Structured Logging (per-run log file aware)."""

from __future__ import annotations

import logging
import logging.config
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal, Union

_configured = False


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[95m",
    }
    RESET = "\033[0m"

    def format(self, record):  # type: ignore[override]
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def configure_logging(
    verbosity: Union[Literal["verbose", "none", "errors"], str] = "none",
    *,
    color: bool = True,
    run_id: Union[str, None] = None,
    log_dir: Union[str, Path] = "logs",
) -> None:
    """Idempotent logging bootstrap.

    Parameters
    ----------
    verbosity
        "verbose" = DEBUG, "none" = INFO (default), "errors" = ERROR
    run_id
        When supplied, a *file* handler is attached at
        ``<log_dir>/<run_id>.log``. First call for a given run_id will
        create the file and write::

            RUN_ID=<run_id>               # line-1
            BEGIN-STAMP <iso-timestamp>   # line-2  (always for *_base)

        Subsequent processes with the *same* run_id will **append** a fresh
        BEGIN-STAMP line (useful for tee piping).
    """
    global _configured
    if _configured:  # pragma: no cover
        return

    # ------------------------ base console handler -------------------------
    levels = {"verbose": logging.DEBUG, "none": logging.INFO, "errors": logging.ERROR}
    level = levels.get(verbosity, logging.INFO)

    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    date = "%Y-%m-%d %H:%M:%S"
    formatter_cls = ColorFormatter if color else logging.Formatter
    formatter = formatter_cls(fmt=fmt, datefmt=date)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logging.root.setLevel(level)
    logging.root.handlers.clear()
    logging.root.addHandler(console_handler)

    # ----------------------------- file handler ----------------------------
    if run_id:
        log_path = Path(log_dir) / f"{run_id}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create file with RUN_ID header on first ever write
        if not log_path.exists():
            log_path.write_text(f"RUN_ID={run_id}\n", encoding="utf-8")

        # For *_base logs record a session stamp **every** invocation
        if run_id.endswith("_base"):
            ts = datetime.utcnow().isoformat(timespec="seconds")
            with log_path.open("a", encoding="utf-8") as fh:
                fh.write(f"BEGIN-STAMP {ts}\n")

        file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(fmt, date))
        logging.root.addHandler(file_handler)

    _configured = True


def reset_logging() -> None:
    """Utility for unit tests – wipes all handlers so we can re-init."""
    global _configured
    logging.root.handlers.clear()
    _configured = False
