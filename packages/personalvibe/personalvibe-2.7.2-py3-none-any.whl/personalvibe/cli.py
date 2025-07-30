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
import os
import platform
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import List, Sequence, Union

from personalvibe import run_pipeline, vibe_utils
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
            _unused_mode = yaml.safe_load(f).get("mode", "").strip()
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
        if ns.max_tokens != 16000:
            forwarded += ["--max_tokens", str(ns.max_tokens)]

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
    if ns.max_tokens != 16000:
        forwarded += ["--max_tokens", str(ns.max_tokens)]

    # Inject the correct mode directly into YAML?  – not needed, YAML already
    # holds it; we *trust* user passed the right sub-command.

    _call_run_pipeline(forwarded)


def _cmd_parse_stage(ns: argparse.Namespace) -> None:
    proj = ns.project_name
    if not proj:
        from personalvibe.vibe_utils import detect_project_name

        try:
            proj = detect_project_name()
        except ValueError as e:
            print(str(e))
            raise SystemExit(1) from e
    saved = extract_and_save_code_block(proj)
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
        sp.add_argument("--max_tokens", type=int, default=16000, help="Maximum completion tokens")

    # run ----------
    run_sp = sub.add_parser("run", help="Determine mode from YAML then execute.")
    _common(run_sp)
    run_sp.add_argument("--raw-argv", help=argparse.SUPPRESS, default="")
    run_sp.set_defaults(func=_cmd_run)

    # explicit modes -
    for _mode in ("milestone", "sprint", "validate", "prd", "bugfix"):
        m_sp = sub.add_parser(_mode, help=f"{_mode} workflow")
        _common(m_sp)
        m_sp.set_defaults(func=lambda ns, m=_mode: _cmd_mode(ns, m))

    # new-milestone -------------------------------------------------
    nm = sub.add_parser("new-milestone", help="Scaffold next milestone YAML")
    nm.add_argument("--project_name", help="Override auto detection.")
    nm.add_argument("--no-open", action="store_true", help="Skip opening editor/viewer.")
    nm.set_defaults(func=_cmd_new_milestone)

    # prepare-sprint -----------------------------------------------
    pspr = sub.add_parser("prepare-sprint", help="Scaffold next sprint YAML")
    pspr.add_argument("--project_name", help="Override auto detection.")
    pspr.add_argument("--no-open", action="store_true")
    pspr.set_defaults(func=_cmd_prepare_sprint)
    # prepare-bugfix -----------------------------------------------
    pbug = sub.add_parser("prepare-bugfix", help="Scaffold next bugfix YAML")
    pbug.add_argument("--project_name", help="Override auto detection.")
    pbug.add_argument("--no-open", action="store_true")
    pbug.set_defaults(func=_cmd_prepare_bugfix)

    # parse-stage ---
    ps = sub.add_parser("parse-stage", help="Extract latest assistant code block.")
    ps.add_argument("--project_name", required=True)
    ps.add_argument("--run", action="store_true", help="Execute the extracted script after save.")
    ps.set_defaults(func=_cmd_parse_stage)

    return p


def cli_main(argv: Union[Sequence[str], None] = None) -> None:
    parser = _build_parser()
    ns = parser.parse_args(argv)
    # dispatch
    ns.func(ns)  # type: ignore[arg-type]


# ----------------------------------------------------------------- helpers
def _open_in_editor(path: Path) -> None:
    """Best-effort open *path* either in $EDITOR or OS default viewer."""
    editor = os.getenv("EDITOR")
    try:
        if editor:
            subprocess.call([editor, str(path)])
        elif platform.system() == "Darwin":
            subprocess.call(["open", str(path)])
        else:
            subprocess.call(["xdg-open", str(path)])
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] Unable to open {path}: {exc}", file=sys.stderr)


def _scan_versions(stages_dir: Path) -> list[tuple[int, int, int]]:
    vers: list[tuple[int, int, int]] = []
    for f in stages_dir.glob("*.*"):
        m = re.match(r"^(\d+)\.(\d+)\.(\d+)\..*$", f.name)
        if m:
            vers.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return sorted(vers)


# ----------------------------------------------------------------- NM
def _cmd_new_milestone(ns: argparse.Namespace) -> None:
    proj = ns.project_name or vibe_utils.detect_project_name()
    stages = vibe_utils.get_base_path() / "prompts" / proj / "stages"
    stages.mkdir(parents=True, exist_ok=True)
    versions = _scan_versions(stages)
    next_major = (versions[-1][0] + 1) if versions else 1
    ver_str = f"{next_major}.0.0"
    dest = Path.cwd() / f"{ver_str}.yaml"

    # copy template
    tmpl = vibe_utils._load_template("milestone_template.yaml")
    dest.write_text(tmpl.replace("{{ project_name }}", proj), encoding="utf-8")
    print(f"Created new milestone YAML: {dest}")
    if not ns.no_open:
        _open_in_editor(dest)


# ----------------------------------------------------------------- PS
def _cmd_prepare_sprint(ns: argparse.Namespace) -> None:
    proj = ns.project_name or vibe_utils.detect_project_name()
    stages = vibe_utils.get_base_path() / "prompts" / proj / "stages"
    stages.mkdir(parents=True, exist_ok=True)
    versions = _scan_versions(stages)

    if not versions:
        # no sprints yet – assume major 1
        next_ver = "1.1.0"
    else:
        latest = versions[-1]
        next_ver = f"{latest[0]}.{latest[1] + 1}.0"  # bump sprint

    dest = Path.cwd() / f"{next_ver}.yaml"
    tmpl = vibe_utils._load_template("sprint_template.yaml")
    dest.write_text(tmpl.replace("{{ project_name }}", proj), encoding="utf-8")
    print(f"Created sprint YAML: {dest}")
    if not ns.no_open:
        _open_in_editor(dest)


# ----------------------------------------------------------------- PB
def _cmd_prepare_bugfix(ns: argparse.Namespace) -> None:
    proj = ns.project_name or vibe_utils.detect_project_name()
    stages = vibe_utils.get_base_path() / "prompts" / proj / "stages"
    stages.mkdir(parents=True, exist_ok=True)
    versions = _scan_versions(stages)

    if not versions:
        # no files yet
        next_ver = "1.0.1"
    else:
        latest = versions[-1]
        # For bugfix, increment patch version
        next_ver = f"{latest[0]}.{latest[1]}.{latest[2] + 1}"

    dest = Path.cwd() / f"{next_ver}.yaml"
    tmpl = vibe_utils._load_template("bugfix_template.yaml")
    dest.write_text(tmpl.replace("{{ project_name }}", proj), encoding="utf-8")
    print(f"Created bugfix YAML: {dest}")
    if not ns.no_open:
        _open_in_editor(dest)


# === CHUNK3_cli_helpers_cmds END ===


# Entry-point for poetry console-script
def app() -> None:  # noqa: D401
    """Poetry console-script shim."""
    cli_main()


if __name__ == "__main__":  # pragma: no cover
    cli_main()
