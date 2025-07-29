# personalvibe

Shared utilities reused by multiple hobby projects (importable as `personalvibe`).


## Prompt persistence & hashing

Every prompt (input *and* LLM output) is written to
`data/<project>/prompt_[in|out]puts` with a filename that embeds:

1. A timestamp – human searchable
2. An optional upstream *input* hash (so output files can be paired)
3. The first 10 chars of **SHA-256(prompt)** – collision-safe ID

The helper `personalvibe.vibe_utils.save_prompt()` de-duplicates using the
hash so re-runs never flood the directory; it simply returns the existing
`Path` when a match is found.  Each file is suffixed with

```text
### END PROMPT
```

which makes shell/grep extraction of individual prompts trivial.
## CLI usage
After installation a *console-script* named `pv` is available:

pv --help                         # global help
pv milestone --config 1.0.0.yaml  # run milestone analysis
pv sprint    --config 1.0.0.yaml  # execute a sprint
pv validate  --config 1.0.0.yaml  # lint/tests against the log file
