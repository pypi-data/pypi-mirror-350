At this stage, we want to reflect on the project and propose a new milestone direction.

The user will recommend how many sprints they want to perform as part of this milestone.

We have build significant information in the PRD and codefiles.
The challenge is that to generate all required technical code assets of the project would likely exceed the output capabilities of a large language model.

With that in mind, lets take the assumption that a large langauge model could output 16_000 characters of text maximum per sprint.

Your task is to do the following:

1. Evaluate the current state of the project
2. Determine a next major milestone
3. Evaluate the approximate total project size in terms of characters of the next major milestone
4. Determine the best approach to split the work into manageable chunks of output, with respect to chunking the work by logical separation of concerns, so as to test and confirm expected behaviour, language model output limits, and also human time spent performing work over chunks
5. Rank order the list of chunks by your recommendation of which chunk to start first, with respect to most needed in terms of scaffolding
6. Provide a introductory two paragraphs explaining your reasoning and approach, and then, how it applies to the prompt brief provided

You must list chunks in terms of numbers, do not use lettering.
They should always be referred to as `Chunk 1`, `Chunk 2`, `Chunk n`
Never as `1- Chunk` or `4) Chunk` etc.

While your task at this stage does not require actual execution of code, this is more of a planning step, the following is useful context:

Assume that you are being run from an unknown folder within the codebase - use the following code to find the root repo path
from personalvibe import vibe_utils
REPO = vibe_utils.get_base_path()

## Glossary — one-liners for unambiguous parsing
- PRD – Product Requirements Document; high-level narrative of goals, scope, and constraints.
- Milestone – A group of up to five sprints that advance the product toward a headline objective.
- Sprint – A discrete, testable chunk of work (≤ 16 k output tokens) within a milestone.
- Bugfix – Patch-level sprint focused solely on correcting defects; YAML mode: bugfix, file saved as <major>.<minor>.<patch>.md.
- SemVer – Semantic versioning string major.minor.patch (e.g. 7.1.1); minor = sprint, patch = bugfix iteration.
- YAML config – A .yaml file describing a task run; mandatory keys include project_name, mode, and execution_details.
- YAML naming – The convention that filenames mirror SemVer (e.g. 7.2.0.yaml) and live in prompts/<project>/configs/.
- Execution details – Free-form logs, traces, or test output embedded in the YAML to give the agent runtime context.
- parse_stage – CLI tool (python -m personalvibe.parse_stage) that validates YAML, stamps version, and saves outputs.
- Prompt-only execution – A smoke-test mode that renders a prompt without hitting external APIs; verifies import paths.
- max_tokens – Upper bound on LLM completion tokens; default 16_000, override via CLI --max_tokens.
- DX – Developer Experience; all efforts that shorten feedback loops, improve clarity, or reduce cognitive load.
