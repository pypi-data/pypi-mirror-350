# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Generic retry–with–rollback helper (Chunk A)."""

from __future__ import annotations

import logging
import subprocess
import sys
import time
from types import TracebackType
from typing import Callable, List, Type, Union

log = logging.getLogger(__name__)


class RetryError(RuntimeError):
    """Raised when *all* retry attempts fail."""


def _rollback_branch(branch_name: str) -> None:
    """Hard-reset the git branch to its first commit & delete it.

    We purposefully keep it *brutally* simple – CI will always be on a
    throw-away branch named ``vibed/<semver>`` so nuking it is safe.
    """
    log.error("Rolling-back branch %s …", branch_name)
    cmds = [
        ["git", "reset", "--hard", "HEAD~1"],
        ["git", "checkout", "-"],  # return to previous branch
        ["git", "branch", "-D", branch_name],  # delete the broken branch
    ]
    for cmd in cmds:
        try:
            subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:  # pragma: no cover
            log.warning("Git rollback step failed: %s", exc.stdout)


def run_with_retries(
    action: Callable[[], bool],
    *,
    max_retries: int = 5,
    sleep_seconds: float = 0.0,
    branch_name: Union[str, None] = None,
) -> bool:
    """Run *action* until it returns ``True`` or retries exhausted.

    Parameters
    ----------
    action
        Callable that **returns bool** – *True* ⇒ success.
        It may raise; all exceptions count as failure / trigger retry.
    max_retries
        Maximum number of *attempts* (so ``max_retries=1`` means **no**
        retry, just a single execution).
    sleep_seconds
        Optional backoff between attempts (very small by default).
    branch_name
        When supplied and the action still fails after all retries,
        ``_rollback_branch`` is invoked.

    Returns
    -------
    bool
        ``True`` on success (i.e. action returned True at least once).

    Raises
    ------
    RetryError
        If all attempts fail.
    """
    attempt = 0
    errors: List[Union[BaseException, None]] = []

    while attempt < max_retries:
        attempt += 1
        try:
            log.debug("RetryEngine – attempt %d/%d", attempt, max_retries)
            if action():
                if attempt > 1:
                    log.info("✅  Succeeded after %d attempts", attempt)
                return True
            else:
                log.warning("Action returned False (attempt %d)", attempt)
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)
            etype: Type[BaseException] = type(exc)
            log.warning("Action raised %s: %s  (attempt %d)", etype.__name__, exc, attempt)

        if attempt < max_retries and sleep_seconds:
            time.sleep(sleep_seconds)

    # ---- failure after all attempts ------------------------------------
    log.error("❌  All %d attempts failed.", max_retries)
    if branch_name:
        _rollback_branch(branch_name)

    # Preserve last error for callers wanting more context
    raise RetryError(f"All {max_retries} attempts failed; see logs.") from (errors[-1] if errors else None)
