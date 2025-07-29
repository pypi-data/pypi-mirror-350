# Copyright © 2025 by Nick Jenkins. All rights reserved

import argparse
import re
import runpy
from datetime import datetime
from pathlib import Path

from personalvibe import vibe_utils


def find_latest_log_file(project_name: str) -> Path:
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


def determine_next_version(project_name: str) -> str:
    base_path = vibe_utils.get_base_path()
    stages_dir = base_path / "prompts" / project_name / "stages"
    stages_dir.mkdir(parents=True, exist_ok=True)

    files = list(stages_dir.glob("*.py")) + list(stages_dir.glob("*.md"))
    version_tuples = []

    for f in files:
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)\..*$", f.name)
        if match:
            major, sprint, bugfix = map(int, match.groups())
            version_tuples.append((major, sprint, bugfix))

    if not version_tuples:
        return "1.1.0"

    # Get the latest milestone and sprint
    version_tuples.sort()
    latest_major, latest_sprint, _ = version_tuples[-1]

    # Increment sprint under latest major
    next_version = f"{latest_major}.{latest_sprint + 1}.0"
    return next_version


def extract_and_save_code_block(project_name: str) -> str:
    base_path = vibe_utils.get_base_path()
    input_file = find_latest_log_file(project_name)
    stages_dir = base_path / "prompts" / project_name / "stages"

    content = input_file.read_text(encoding="utf-8")
    match = re.search(r"```python\n(.*?)\n```", content, re.DOTALL)
    if not match:
        raise ValueError("No ```python block found in the latest log file.")

    extracted_code = match.group(1).strip()

    new_version = determine_next_version(project_name)
    output_file = stages_dir / f"{new_version}.py"

    # Prepare final content with header
    header = f"# python prompts/{project_name}/stages/{new_version}.py\n"
    final_content = f"{header}\n{extracted_code}\n"

    output_file.write_text(final_content, encoding="utf-8")

    print(f"Saved extracted code to: {output_file}")
    return str(output_file)


if __name__ == "__main__":
    """Parse and execute the latest sprint code generation.

    python -m personalvibe.parse_stage
    """
    parser = argparse.ArgumentParser(description="Extract latest prompt output and save as versioned Python file.")
    parser.add_argument("--project_name", required=True, help="Project name (used for path resolution).")
    parser.add_argument("--run", action="store_true", help="Execute the extracted code after saving.")
    args = parser.parse_args()

    saved_file = extract_and_save_code_block(args.project_name)

    if args.run:
        print(f"Running extracted code from: {saved_file}")
        runpy.run_path(saved_file, run_name="__main__")
