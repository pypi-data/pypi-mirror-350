# Copyright © 2025 by Nick Jenkins. All rights reserved
"""Orchestrates YAML → prompt rendering → vibecoding."""

import argparse
import logging
import re
import textwrap
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator

from personalvibe import logger, vibe_utils
from personalvibe.yaml_utils import sanitize_yaml_text


class ConfigModel(BaseModel):
    # --- field validation --------------------------------------------------
    @field_validator("model", mode="before")
    def validate_model(cls, v: str) -> str:  # noqa: D401,N805,ANN101
        if v in ("", None):
            return ""
        if isinstance(v, str) and re.match(r"^[^/]+/.+$", v.strip()):
            return v.strip()
        raise ValueError("model must be <provider>/<model_name>")

    """Schema **v2**

    • adds optional ``conversation_history`` (list of {role, content})
    • drops *required* ``milestone_file_name`` (legacy keys tolerated)
    """
    version: str
    project_name: str
    mode: str = Field(..., pattern="^(prd|milestone|sprint|validate|bugfix)$")
    model: Optional[str] = None
    execution_task: Optional[str] = None
    execution_details: str = ""
    code_context_paths: List[str]
    # ---- NEW --------------------------------------------------------
    conversation_history: Optional[List[dict[str, str]]] = None
    # ---- still used by validate flow --------------------------------
    error_file_name: str = ""

    class Config:
        extra = "ignore"  # silently discard unknown legacy fields


def load_config(config_path: str) -> ConfigModel:
    """Load YAML then validate. Auto-fills *project_name* if missing."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            _raw = f.read()
            _yaml_txt = textwrap.dedent(_raw)
            _yaml_txt = sanitize_yaml_text(_yaml_txt, origin=config_path)
            raw = yaml.safe_load(_yaml_txt)
            raw["version"] = Path(config_path).stem

        # ---- auto-detect project_name if missing ----
        if not raw.get("project_name"):
            try:
                raw["project_name"] = vibe_utils.detect_project_name()
            except ValueError as e:
                raise RuntimeError("project_name absent from YAML and auto-detection failed.") from e

        return ConfigModel(**raw)

    except ValidationError as e:
        logging.getLogger(__name__).error("Config validation failed:\n%s", e)
        raise


def main() -> None:
    """Run an iteration of personal vibe based on a config file.

    i.e. subl prompts/personalvibe/configs/2.1.0.yaml

    python -m personalvibe.run_pipeline --config prompts/personalvibe/configs/2.1.0.yaml --prompt_only
    """
    parser = argparse.ArgumentParser(description="Run the Personalvibe Workflow.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    parser.add_argument("--verbosity", choices=["verbose", "none", "errors"], default="none", help="Console log level")
    parser.add_argument("--prompt_only", action="store_true", help="If set, only generate the prompt.")
    parser.add_argument("--max_retries", type=int, default=5, help="Maximum attempts for sprint validation")
    parser.add_argument("--max_tokens", type=int, default=20000, help="Maximum completion tokens for LLM")
    args = parser.parse_args()

    # 1️⃣  Parse config first – we need the semver to derive run_id
    config = load_config(args.config)
    run_id = f"{config.version}_base"

    # workspace aware ----------------------------------------------------
    workspace = vibe_utils.get_workspace_root()

    # 2️⃣  Bootstrap logging (console + per-semver file)
    logger.configure_logging(args.verbosity, run_id=run_id, log_dir=workspace / "logs")
    logger.configure_logging(args.verbosity, run_id=run_id)
    log = logging.getLogger(__name__)
    log.info("P  E  R  S  O  N  A  L  V  I  B  E  – run_id=%s", run_id)

    # 3️⃣  Render prompt template ------------------------------------------------
    code_context = vibe_utils.get_context(config.code_context_paths)
    replacements = vibe_utils.get_replacements(config, code_context)
    template_path = f"{config.project_name}/prd.md"
    if not template_path:
        log.error("Unsupported mode '%s'.", config.mode)
        return

    prompt = vibe_utils.render_prompt_template(template_path, replacements=replacements)

    if args.prompt_only:
        base_input_path = vibe_utils.get_data_dir(config.project_name, workspace) / "prompt_inputs"
        base_input_path.mkdir(parents=True, exist_ok=True)
        _ = vibe_utils.save_prompt(prompt, base_input_path)
    else:
        vibe_utils.get_vibed(
            prompt,
            project_name=config.project_name,
            max_completion_tokens=args.max_tokens,
            workspace=workspace,
            model=(config.model or None),
        )


if __name__ == "__main__":  # pragma: no cover
    main()
