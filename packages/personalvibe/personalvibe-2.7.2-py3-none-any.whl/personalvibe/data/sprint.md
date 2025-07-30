At this stage, we have confirmed the next milestone for this project.

The milestone document also contains information on how to 'chunk'. It is useful to have small iterations such that it is a managable size for human review, and to stay within 16k ouput character LLM limitations.

Use a maximum of 16_000 output characters to deliver on your output chunk.

Reminder: ONLY GENERATE code relating to the mentioned sprint and additional detail provided.

Your response must conform to the following requirements:

- Produce an executable python script within <python></python> tags
- Executable script must create idempotent changes to codebase files
- Script may include touch / mkdir for any new files, however, you must reuse existing files, modules, and functions as much as is practical
- Script may include python code, documentation, typing as needed to patch codebase as required
- As the last portion of the python script, generate a Print statement with detailed further directions and context on the changes, testing required, and recommended next steps to the command line
- Do not bother putting much detail at the top of the file, put it in the bottom with the print statement for command line

Assume that you are being run from an unknown folder within the codebase - use the following code to find the root repo path
from personalvibe import vibe_utils
REPO = vibe_utils.get_base_path()

You must be particularly careful when generating code such that the following are considered
1. backtick usage
2. triple quoted strings

Similar to the above, you may need to use triple quoted strings within triple quoted strings
Recommend to use single quoted for the python patch, and double quoted for the code to be inserted i.e.

outer = '''

inner = """hello"""

'''

3. Be careful with escaping quotes

If you follow the above rule, you shouldnt need to do any escaping i.e. /"/"/"

<badly_formatted_triple_quotes>
# Fix the batch_processor.py to get model from config
batch_processor_fix = ''' ## Note the python program is declaring a variable and assigning string
# Find the line with PLZ FIX and replace it
import re

batch_processor_path = Path(REPO) / "tr" / "amd_sharp" / "batch_processor.py"
with open(batch_processor_path, 'r') as f:
  content = f.read()

# Replace the hard-coded model with config-based model
old_pattern = r'"""PLZ FIX NOTE TO AI:.*?"""\\s*payload = \\{[^}]+\\}'
new_code = '''# Get model from configuration or metadata ## This inside triple quote is breaking the first set
          model = self.client.config.server_model if hasattr(self.client.config, 'server_model') else "sharp_gemma3_12b_128k"

          payload = {
              "prompt": prompt,
              "model": model,
              "metadata": {"source_file": str(filepath), "item_id": item_id},
          }'''

content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

with open(batch_processor_path, 'w') as f:
  f.write(content)
'''
</badly_formatted_triple_quotes>

This causes problems when executing the parse runner

(bytedtramd-py3.9) bytedance@C02H86S6Q05N transparency_reporting % pv parse-stage --project_name sharp --run
Saved extracted code to: /Users/bytedance/Documents/transparency_reporting/prompts/sharp/stages/2.2.2.py
Running extracted code from: /Users/bytedance/Documents/transparency_reporting/prompts/sharp/stages/2.2.2.py
Traceback (most recent call last):
File "/Users/bytedance/Documents/transparency_reporting/.venv/bin/pv", line 8, in <module>
  sys.exit(app())
File "/Users/bytedance/Documents/transparency_reporting/.venv/lib/python3.9/site-packages/personalvibe/cli.py", line 250, in app
  cli_main()
File "/Users/bytedance/Documents/transparency_reporting/.venv/lib/python3.9/site-packages/personalvibe/cli.py", line 177, in cli_main
  ns.func(ns)  # type: ignore[arg-type]
File "/Users/bytedance/Documents/transparency_reporting/.venv/lib/python3.9/site-packages/personalvibe/cli.py", line 121, in _cmd_parse_stage
  runpy.run_path(saved, run_name="__main__")
File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/runpy.py", line 267, in run_path
  code, fname = _get_code_from_file(run_name, path_name)
File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/runpy.py", line 242, in _get_code_from_file
  code = compile(f.read(), fname, 'exec')
File "/Users/bytedance/Documents/transparency_reporting/prompts/sharp/stages/2.2.2.py", line 555
  model = self.client.config.server_model if hasattr(self.client.config, 'server_model') else "sharp_gemma3_12b_128k"
IndentationError: unexpected indent
(bytedtramd-py3.9) bytedance@C02H86S6Q05N transparency_reporting %

If you are unable to create executable code because of the nature of the
code being modified and it's use of triple quotes, add comments as '## PLZ FIX HUMAN'
to have an experienced programmer address blocking issues

You are generating Python patch-files that will be executed with `runpy`.
Follow every rule exactly.

### 1. QUOTING RULES
• Use ONE quoting convention throughout the file:
– **Outer** “string‐as-file-content” blocks → triple-single-quoted  ''' … '''
– **Inner** docstrings INSIDE the code you are writing to disk → triple-double-quoted  """ … """
• Never nest the same quote style inside itself.
• If you must embed another triple-quoted block inside a string, replace it with the literal token  <TRIPLE_QUOTE>  and add a comment telling a human to restore it.

### 2. INDENTATION & WHITESPACE
• Top-level code starts at column 0.
• When you write multi-line strings that will be written to files, use
  textwrap.dedent('''\n…\n''')   **or**   '''\\\n…\n''' so that the final file has no extra indent.
• Strip trailing spaces.

### 3. ESCAPE-HATCH
If any rule above prevents you from emitting runnable code, output
  ## PLZ FIX HUMAN – reason …
in the exact spot and continue.

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
