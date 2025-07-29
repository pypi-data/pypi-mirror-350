# Copyright © 2025 by Nick Jenkins. All rights reserved
# mypy: ignore-errors
import hashlib
import html
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List, Union

import dotenv
import pathspec
import tiktoken
from jinja2 import Environment, FileSystemLoader

if TYPE_CHECKING:
    from personalvibe.run_pipeline import ConfigModel  # noqa: F401

from openai import OpenAI

from personalvibe.yaml_utils import sanitize_yaml_text

dotenv.load_dotenv()
# -----------------------------------------------------------------
# Ensure wheel smoke-tests never abort if the user forgot to export
# an OPENAI key – we create a harmless placeholder *once*.
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "DUMMY_KEY"

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

log = logging.getLogger(__name__)


def get_prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def find_existing_hash(root_dir: Union[str, Path], hash_str: str) -> Union[Path, None]:
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if hash_str in filename:
                return Path(dirpath) / filename
    return None


# ------------------------------------------------------------------
# --- PERSONALVIBE PATCH C ANCHOR: save_prompt (do not delete) -----
# ------------------------------------------------------------------
def save_prompt(prompt: str, root_dir: Path, input_hash: str = "") -> Path:
    """Persist *one* prompt to disk and return its Path.

    Behaviour
    ----------
    • Uses SHA-256(prompt)[:10] to create a stable short-hash.
    • If a file containing that hash already exists, nothing is written
      and the *existing* Path is returned.
    • New files are named   <timestamp>[_<input_hash>]_ <hash>.md
    • Every file is terminated with an extra line::

          ### END PROMPT

      to make `grep -A999 '^### END PROMPT$'` trivially reliable.
    """
    # Timestamp + hash bits
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    hash_str = get_prompt_hash(prompt)[:10]

    if existing := find_existing_hash(root_dir, hash_str):
        log.info("Duplicate prompt detected. Existing file: %s", existing)
        return existing

    # Compose filename
    if input_hash:
        filename = f"{timestamp}_{input_hash}_{hash_str}.md"
    else:
        filename = f"{timestamp}_{hash_str}.md"
    filepath = Path(root_dir) / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Write prompt + END-marker
    filepath.write_text(
        f"""{prompt}
### END PROMPT
""",
        encoding="utf-8",
    )
    log.info("Prompt saved to: %s", filepath)
    return filepath


def get_vibed(
    prompt: str,
    contexts: Union[List[Path], None] = None,
    project_name: str = "",
    model: str = "o3",
    max_completion_tokens: int = 100_000,
    *,
    workspace: Union[Path, None] = None,
) -> str:
    """Wrapper for O3 vibecoding – **now workspace-aware**."""
    if contexts is None:
        contexts = []

    workspace = workspace or get_workspace_root()

    base_input_path = get_data_dir(project_name, workspace) / "prompt_inputs"
    base_input_path.mkdir(parents=True, exist_ok=True)
    prompt_file = save_prompt(prompt, base_input_path)
    input_hash = prompt_file.stem.split("_")[-1]

    # -- build messages ---------------------------------------------------
    messages = []
    for context in contexts:
        part = {"role": "user" if "prompt_inputs" in context.parts else "assistant"}
        part["content"] = [{"type": "text", "text": context.read_text()}]
        messages.append(part)

    messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})

    message_chars = len(str(messages))
    message_tokens = num_tokens(str(messages), model=model)
    log.info("Prompt size – Tokens: %s, Chars: %s", message_tokens, message_chars)

    response = (
        client.chat.completions.create(model=model, messages=messages, max_completion_tokens=max_completion_tokens)
        .choices[0]
        .message.content
    )

    # -- save assistant reply --------------------------------------------
    base_output_path = get_data_dir(project_name, workspace) / "prompt_outputs"
    base_output_path.mkdir(parents=True, exist_ok=True)
    _ = save_prompt(response, base_output_path, input_hash=input_hash)

    return response


def get_context(filenames: List[str], extension: str = ".txt") -> str:
    big_string = ""
    base_path = get_base_path()
    log.debug(f"Base path is {base_path}")

    gitignore_spec = load_gitignore(base_path)

    for name in filenames:
        file_path = base_path / name

        if not file_path.exists():
            print(f"Warning: {file_path} does not exist. {os.getcwd()}")
            continue

        lines = file_path.read_text(encoding="utf-8").splitlines()
        unique_lines = sorted(set(lines))
        file_path.write_text("\n".join(unique_lines) + "\n", encoding="utf-8")

        for line in unique_lines:
            if not line.strip():
                continue

            line_path = base_path / line
            log.debug(f"Working on codepath {line_path}")

            if any(char in line for char in "*?[]"):
                matches = sorted(base_path.glob(line))
                if not matches:
                    log.warning(f"No matches found for wildcard pattern: {line}")
                for match in matches:
                    rel_match = str(match.relative_to(base_path))
                    if gitignore_spec.match_file(rel_match):
                        continue
                    if match.is_file():
                        try:
                            big_string += _process_file(match)
                        except UnicodeDecodeError:
                            message = f"Unable to parse {line} in {name} - {match}"
                            logging.error(message)
            else:
                if not line_path.exists():
                    message = f"Warning: {line_path} does not exist. {os.getcwd()}"
                    log.error(message)
                    raise ValueError(message)

                rel_line = str(line_path.relative_to(base_path))
                if gitignore_spec.match_file(rel_line):
                    continue

                big_string += _process_file(line_path)

    return big_string


def _process_file(file_path: Path) -> str:
    """Helper to read and return file content with appropriate markdown code fences."""
    rel_path = file_path.relative_to(get_base_path())
    extension = file_path.suffix.lower()

    # Map file extensions to markdown languages
    extension_to_lang = {
        ".py": "python",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript",
        ".json": "json",
        ".html": "html",
        ".md": "",  # Markdown files don’t need code fences, show raw content
        ".toml": "toml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".txt": "",  # Plain text, no code highlighting
        ".sh": "bash",
        ".cfg": "",
        ".ini": "",
    }

    language = extension_to_lang.get(extension, "")  # Default to no highlighting if unknown

    content = file_path.read_text(encoding="utf-8")
    content = html.unescape(content)

    if extension == ".md":
        # For markdown files, don't wrap in code fences
        return f"\n#### Start of {rel_path}\n{content}\n#### End of {rel_path}\n"
    else:
        return f"\n#### Start of {rel_path}\n" f"```{language}\n" f"{content}\n" f"```\n" f"#### End of {rel_path}\n"


from pathlib import Path as _PvPath


def load_gitignore(base_path: _PvPath) -> pathspec.PathSpec:
    gitignore_path = base_path / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
        return spec
    return pathspec.PathSpec([])  # Empty spec if no .gitignore


# ----------------------------------------------------------------------
# ✨  New workspace-root helpers  (Chunk B)
# ----------------------------------------------------------------------
_SENTINEL_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def get_workspace_root() -> Path:
    """Return the directory where **runtime artefacts** should live.

    Resolution order
    ----------------
    1. Environment variable ``PV_DATA_DIR`` (if set & non-empty)
    2. **Mono-repo fallback** – if the current process is running from
       within the original Personalvibe source checkout (detected by the
       presence of *prompts/* beside ``src/``), we keep the *old* behaviour
       so that developer workflows stay unchanged.
    3. Finally, just ``Path.cwd()`` (suits ``pip install personalvibe`` in
       any third-party project).
    """
    env = os.getenv("PV_DATA_DIR")
    if env:
        return Path(env).expanduser().resolve()

    # inside mono-repo?  -> use legacy base-path crawl
    if _SENTINEL_PROMPTS_DIR.exists():
        from warnings import warn

        warn(
            "⚠️  get_workspace_root() fell back to repo-root because "
            "$PV_DATA_DIR is unset and prompts/ directory exists.  "
            "Set PV_DATA_DIR to silence this message.",
            stacklevel=2,
        )
        return get_base_path()  # type: ignore[arg-type]

    # default
    return Path.cwd().resolve()


def get_data_dir(project_name: str, workspace: Union[Path, None] = None) -> Path:
    """<workspace>/data/<project_name> (mkdir-p, but *not* the sub-folders)."""
    root = workspace or get_workspace_root()
    p = root / "data" / project_name
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_logs_dir(workspace: Union[Path, None] = None) -> Path:
    """<workspace>/logs  (mkdir-p)."""
    root = workspace or get_workspace_root()
    p = root / "logs"
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_base_path(base: str = "personalvibe") -> Path:
    """Returns the base folder directory for the entire github project."""
    new_parts = []
    for part in Path(os.getcwd()).parts:
        new_parts.append(part)
        if part == base:
            break
    return Path(*new_parts)


def num_tokens(text: str, model: str = "o3") -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))


def render_prompt_template(template_path: str, replacements: dict) -> str:
    """
    Renders a prompt template using Jinja2.

    Args:
        template_path (str): Path to the Jinja2 template file, relative to templates_base.
        replacements (dict): Variables to inject into the template.

    Returns:
        str: Rendered prompt as a string.
    """
    prompt_base = Path(get_base_path(), "prompts")
    env = Environment(
        loader=FileSystemLoader(prompt_base),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template(template_path)
    return template.render(**replacements)


def _get_error_text(config: "ConfigModel") -> str:
    error_path = Path(get_base_path(), "prompts", config.project_name, "errors", config.error_file_name)
    # NOTE TO LLM: improve the handling here as per my usual codestyle
    return error_path.read_text()


def _get_milestone_text(config: "ConfigModel") -> str:
    stages_path = Path(get_base_path(), "prompts", config.project_name, "stages")
    milestone_ver, _, _ = config.version.split(".")
    current_major = int(milestone_ver)

    milestone_files = [Path(stages_path, f"{current_major}.0.0.md")]

    # No longer use multi
    # milestone_files = sorted(
    #     [p for p in stages_path.glob("*.0.0.md") if p.is_file() and int(p.stem.split(".")[0]) <= current_major],
    #     key=lambda x: int(x.stem.split(".")[0]),
    # )

    if not milestone_files:
        raise ValueError(f"No valid milestone files found in {stages_path} for major <= {current_major}")
    data = """The following are all milestones related to this project.
    The latest milestone text proposes next work needed, this is what sprints focus on:
    """
    data += "\n\n".join(p.read_text() for p in milestone_files)
    return data


def _get_replacements_v1(config: "ConfigModel", code_context: str) -> dict:
    """
    Build the Jinja replacement map once.

    * Milestone mode injects a standard execution task by default
      unless the YAML overrides it.
    """
    log.info(f"Running config version: {config.version}")
    log.info(f"Running mode = {config.mode}")
    milestone_ver, sprint_ver, bugfix_ver = config.version.split(".")
    if config.mode == "prd":
        exec_task = config.execution_task
        instructions = ""
    elif config.mode == "milestone":
        exec_task = "conduct milestone analysis according to guidelines"
        # Note to AI assistant: src works for now, but what about for an installed version?
        instructions = Path(get_base_path(), "src/personalvibe/data", "milestone.md").read_text()
    elif config.mode == "sprint":
        exec_task = f"perform the sprint number marked {sprint_ver}"
        instructions = (
            Path(get_base_path(), "src/personalvibe/data", "sprint.md").read_text() + "\n" + _get_milestone_text(config)
        )
    elif config.mode == "validate":
        exec_task = f"validate the following logs following the generation of sprint {sprint_ver}"
        instructions = (
            Path(get_base_path(), "src/personalvibe/data", "validate.md").read_text()
            + "\n"
            + _get_milestone_text(config)
            + "\n"
            + _get_error_text(config)
        )

    return {
        "execution_task": exec_task,
        "execution_details": config.execution_details,
        "instructions": instructions,
        "code_context": code_context,
    }


import logging as _logging

# ----------------------------------------------------------------------
# PERSONALVIBE CHUNK 2 – Resource loader
# ----------------------------------------------------------------------
from importlib import resources
from pathlib import Path as _Path

_log = _logging.getLogger(__name__)


def _load_template(fname: str) -> str:
    """Return the *text* of a template shipped as package-data.

    Resolution order
    ----------------
    1. `importlib.resources.files('personalvibe.data')/fname`
    2. Legacy path  src/personalvibe/commands/<fname>
    """
    try:
        pkg_file = resources.files("personalvibe.data").joinpath(fname)
        return pkg_file.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        legacy = _Path(__file__).parent / "data" / fname
        if legacy.exists():
            _log.debug("Template %s loaded from legacy path %s", fname, legacy)
            return legacy.read_text(encoding="utf-8")
        raise FileNotFoundError(f"Template {fname!s} not found in package or legacy path")


# -----------------------------
def get_replacements(config: "ConfigModel", code_context: str) -> dict:  # type: ignore[override]
    """Build the Jinja replacement map (rev-2 using _load_template)."""

    _log.info("Running config version: %s", config.version)
    _log.info("Running mode = %s", config.mode)
    milestone_ver, sprint_ver, bugfix_ver = config.version.split(".")  # noqa: F841

    if config.mode == "prd":
        exec_task = config.execution_task
        instructions = ""
    elif config.mode == "milestone":
        exec_task = "conduct milestone analysis according to guidelines"
        instructions = _load_template("milestone.md")
    elif config.mode == "sprint":
        exec_task = f"perform the sprint number marked {sprint_ver}"
        instructions = _load_template("sprint.md") + "\n" + _get_milestone_text(config)
    elif config.mode == "validate":
        exec_task = f"validate the following logs following the generation of sprint {sprint_ver}"
        instructions = (
            _load_template("validate.md") + "\n" + _get_milestone_text(config) + "\n" + _get_error_text(config)
        )
    else:  # pragma: no cover
        raise ValueError(f"Unsupported mode {config.mode}")

    return {
        "execution_task": exec_task,
        "execution_details": config.execution_details,
        "instructions": instructions,
        "code_context": code_context,
    }


import logging as _pv_log

# === detect_project_name (chunk 2)
from pathlib import Path as _PvPath


def detect_project_name(cwd: _PvPath | None = None) -> str:
    """Best-effort inference of the **project_name**.

    Strategy
    --------
    1. If *cwd* (or its parents) path contains ``prompts/<name>`` → return
       that immediate directory name.
    2. Else walk *upwards* until a folder with ``prompts/`` is found:
         • if that ``prompts`` dir contains exactly ONE sub-directory we
           assume it is the project.
    3. Otherwise raise ``ValueError`` explaining how to fix.

    This keeps the common cases zero-config while remaining explicit when
    multiple projects coexist.
    """
    cwd = (cwd or _PvPath.cwd()).resolve()
    parts = cwd.parts
    if "prompts" in parts:
        idx = parts.index("prompts")
        if idx + 1 < len(parts):
            return parts[idx + 1]

    for parent in [cwd, *cwd.parents]:
        p_dir = parent / "prompts"
        if p_dir.is_dir():
            sub = [d for d in p_dir.iterdir() if d.is_dir()]
            if len(sub) == 1:
                return sub[0].name
            break  # ambiguous – fallthrough to error
    raise ValueError(
        "Unable to auto-detect project_name; pass --project_name or run " "from within prompts/<name>/… directory."
    )
