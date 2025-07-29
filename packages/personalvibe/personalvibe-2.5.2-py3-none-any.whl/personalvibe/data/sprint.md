At this stage, we have confirmed the next milestone for this project.

The milestone document also contains information on how to 'chunk'. It is useful to have small iterations such that it is a managable size for human review, and to stay within 20k ouput character LLM limitations.

Use a maximum of 20,000 output characters to deliver on your output chunk.

Reminder: ONLY GENERATE code relating to the mentioned sprint and additional detail provided.

Your response must conform to the following requirements:

- Produce an executable python script within ```python``` tags
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

Given your response will already be surrounded by ```python ```, do not use further backticks in the code or documentation examples

2. triple quoted strings

Similar to the above, you may need to use triple quoted strings within triple quoted strings
Recommend to use single quoted for the python patch, and double quoted for the code to be inserted i.e.

outer = '''

inner = """hello"""

'''

3. Be careful with escaping quotes

If you follow the above rule, you shouldnt need to do any escaping i.e. /"/"/"
