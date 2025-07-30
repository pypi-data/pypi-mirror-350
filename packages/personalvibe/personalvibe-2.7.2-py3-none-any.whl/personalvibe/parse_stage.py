# Copyright © 2025 by Nick Jenkins. All rights reserved

import argparse
import re
import runpy
from datetime import datetime
from pathlib import Path
from typing import Union

from personalvibe import vibe_utils


def find_latest_log_file(project_name: Union[str, None] = None) -> Path:
    project_name = _ensure_project_name(project_name)
    base_path = vibe_utils.get_base_path()
    logs_dir = base_path / "data" / project_name / "prompt_outputs"

    if not logs_dir.exists():
        raise FileNotFoundError(f"Logs directory not found: {logs_dir}")

    log_files = list(logs_dir.glob("*.md"))
    if not log_files:
        raise FileNotFoundError("No log files found in the prompt_outputs directory.")

    def extract_timestamp(file_path: Path) -> datetime:
        match = re.match(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})", file_path.stem)
        if match:
            return datetime.strptime(match.group(1), "%Y-%m-%d_%H-%M-%S")
        return datetime.min

    log_files.sort(key=extract_timestamp, reverse=True)
    return log_files[0]


def extract_and_save_code_block(project_name: Union[str, None] = None) -> str:
    base_path = vibe_utils.get_base_path()

    if project_name is None:
        raise ValueError("project_name must be provided")
    input_file = find_latest_log_file(project_name)
    stages_dir = Path(base_path, "prompts", project_name, "stages")

    content = input_file.read_text(encoding="utf-8")
    match = re.search(r"<python>\n(.*?)\n</python>", content, re.DOTALL)
    if not match:
        raise ValueError("No <python> block found in the latest log file.")

    extracted_code = match.group(1).strip()

    # Determine file extension based on mode (bugfix = .md, sprint = .py)
    # Check if this is a bugfix by looking at the version pattern
    if extracted_code:
        file_extension = ".py"
        style = "sprint"
    else:
        file_extension = ".md"
        style = "bugfix"

    new_version = determine_next_version(project_name, style=style)

    output_file = stages_dir / f"{new_version}{file_extension}"

    # Prepare final content with header
    header = f"# python prompts/{project_name}/stages/{new_version}.py\n"
    final_content = f"{header}\n{extracted_code}\n"

    output_file.write_text(final_content, encoding="utf-8")

    print(f"Saved extracted code to: {output_file}")
    return str(output_file)


# === helper added by chunk 2
def _ensure_project_name(name: Union[str, None]) -> str:
    if name:
        return name
    try:
        return vibe_utils.detect_project_name()
    except ValueError as e:  # re-raise with friendly msg
        raise ValueError(str(e)) from e


def determine_next_version(project_name: Union[str, None] = None, style: str = "") -> str:  # noqa: C901
    """Return the *next* semantic version for **patch-files** (x.y.Z).

    Rules
    -----
    • If **no** existing stage files ⇒ ``1.1.0`` (first sprint).
    • If a sprint, increment to `1.2.0`, if a bugfix, increment to `1.1.1.md`
    • Version scan looks at ``prompts/<project>/stages/*.(md|py)``.

    # TODO update the below code and parameters (sprint or bugfix) to improve the naming

    This fixes the long-standing bug where _determine_next_version()
    bumped the *sprint* instead of the *bug-fix* number.
    """
    base_path = vibe_utils.get_base_path()
    if project_name is None:
        raise ValueError("project_name must be provided")
    stages_dir = Path(base_path, "prompts", project_name, "stages")
    stages_dir.mkdir(parents=True, exist_ok=True)

    files = list(stages_dir.glob("*.py")) + list(stages_dir.glob("*.md"))
    version_tuples: list[tuple[int, int, int]] = []
    for f in files:
        m = re.match(r"^(\d+)\.(\d+)\.(\d+)\..*$", f.name)
        if m:
            version_tuples.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))

    if not version_tuples:
        # first ever sprint under major-1
        return "1.1.0"

    sprint_inc = 0
    bug_inc = 0
    if style == "sprint":
        sprint_inc = 1
        bug_inc = 0
    elif style == "bugfix":
        sprint_inc = 0
        bug_inc = 1

    version_tuples.sort()
    latest_major, latest_sprint, latest_bug = version_tuples[-1]
    return f"{latest_major}.{latest_sprint + sprint_inc}.{latest_bug + bug_inc}"


if __name__ == "__main__":
    """Parse and execute the latest sprint code generation.

    python -m personalvibe.parse_stage --project_name personalvive --run
    """
    parser = argparse.ArgumentParser(description="Extract latest prompt output and save as versioned Python file.")

    parser.add_argument("--project_name", help="When omitted, looked up automatically from cwd.")

    parser.add_argument("--run", action="store_true", help="Execute the extracted code after saving.")
    args = parser.parse_args()

    saved_file = extract_and_save_code_block(args.project_name)

    if args.run:
        print(f"Running extracted code from: {saved_file}")
        runpy.run_path(saved_file, run_name="__main__")
