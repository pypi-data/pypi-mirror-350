# Copyright © 2025 by Nick Jenkins. All rights reserved
"""
Personalvibe CLI  –  3.0.0-chunk-1

Console-script “pv” now exposes **explicit** sub-commands:

    pv run         --config cfg.yaml               # auto-detect mode
    pv milestone   --config cfg.yaml [...]
    pv sprint      --config cfg.yaml [...]
    pv validate    --config cfg.yaml [...]
    pv parse-stage --project_name X [--run]

Common flags:
    --verbosity  {verbose,none,errors}
    --prompt_only
    --max_retries N
Hidden flag:
    --raw-argv "..."       → passes literal args to run_pipeline

Design notes
------------
• Thin wrapper around personalvibe.run_pipeline.main().
• `pv run` inspects YAML to discover `mode`, then *delegates* to the
  specialised handler (so behaviour equals pv <mode>).
• A dedicated `parse-stage` bridges to personalvibe.parse_stage.
• Keeps **backward-compat alias**  pv prd  (no longer documented).
"""

from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path
from typing import List, Sequence

from personalvibe import run_pipeline
from personalvibe.parse_stage import extract_and_save_code_block


# --------------------------------------------------------------------- utils
def _delegated_argv(extra: Sequence[str]) -> List[str]:
    "Build argv list for re-invoking run_pipeline.main()."
    return ["personalvibe.run_pipeline", *extra]


def _call_run_pipeline(extra: Sequence[str]) -> None:
    "Monkey-patch sys.argv then call run_pipeline.main()."
    sys.argv = _delegated_argv(extra)
    run_pipeline.main()  # never returns on sys.exit()


# ----------------------------------------------------------------- commands
def _cmd_run(ns: argparse.Namespace) -> None:
    # Auto-detect mode just by *loading* the YAML (no validation error
    # because run_pipeline will do it later anyway).
    try:
        import yaml  # local import to avoid mandatory dep here

        with open(ns.config, "r", encoding="utf-8") as f:
            mode = yaml.safe_load(f).get("mode", "").strip()
    except Exception:  # noqa: BLE001
        mode = ""

    # --raw-argv bypass (power users)
    if ns.raw_argv:
        forwarded = shlex.split(ns.raw_argv)
    else:
        forwarded = [
            "--config",
            ns.config,
            "--verbosity",
            ns.verbosity,
        ]
        if ns.prompt_only:
            forwarded.append("--prompt_only")
        if ns.max_retries != 5:
            forwarded += ["--max_retries", str(ns.max_retries)]

    # Delegate straight away
    _call_run_pipeline(forwarded)


def _cmd_mode(ns: argparse.Namespace, mode: str) -> None:
    forwarded = [
        "--config",
        ns.config,
        "--verbosity",
        ns.verbosity,
    ]
    if ns.prompt_only:
        forwarded.append("--prompt_only")
    if ns.max_retries != 5:
        forwarded += ["--max_retries", str(ns.max_retries)]

    # Inject the correct mode directly into YAML?  – not needed, YAML already
    # holds it; we *trust* user passed the right sub-command.

    _call_run_pipeline(forwarded)


def _cmd_parse_stage(ns: argparse.Namespace) -> None:
    saved = extract_and_save_code_block(ns.project_name)
    if ns.run:
        import runpy

        print(f"Running extracted code from: {saved}")
        runpy.run_path(saved, run_name="__main__")


# ------------------------------------------------------------------- parser
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pv",
        description="Personalvibe CLI – Command-Line Interface",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd", required=True, metavar="<command>")

    # Helper to DRY common args
    def _common(sp):
        sp.add_argument("--config", required=True, help="Path to YAML config file.")
        sp.add_argument("--verbosity", choices=["verbose", "none", "errors"], default="none")
        sp.add_argument("--prompt_only", action="store_true")
        sp.add_argument("--max_retries", type=int, default=5)

    # run ----------
    run_sp = sub.add_parser("run", help="Determine mode from YAML then execute.")
    _common(run_sp)
    run_sp.add_argument("--raw-argv", help=argparse.SUPPRESS, default="")
    run_sp.set_defaults(func=_cmd_run)

    # explicit modes -
    for _mode in ("milestone", "sprint", "validate", "prd"):
        m_sp = sub.add_parser(_mode, help=f"{_mode} workflow")
        _common(m_sp)
        m_sp.set_defaults(func=lambda ns, m=_mode: _cmd_mode(ns, m))

    # parse-stage ---
    ps = sub.add_parser("parse-stage", help="Extract latest assistant code block.")
    ps.add_argument("--project_name", required=True)
    ps.add_argument("--run", action="store_true", help="Execute the extracted script after save.")
    ps.set_defaults(func=_cmd_parse_stage)

    return p


def cli_main(argv: Sequence[str] | None = None) -> None:
    parser = _build_parser()
    ns = parser.parse_args(argv)
    # dispatch
    ns.func(ns)  # type: ignore[arg-type]


# Entry-point for poetry console-script
def app() -> None:  # noqa: D401
    """Poetry console-script shim."""
    cli_main()


if __name__ == "__main__":  # pragma: no cover
    cli_main()
