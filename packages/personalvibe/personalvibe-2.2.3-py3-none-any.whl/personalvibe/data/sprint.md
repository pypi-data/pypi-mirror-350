At this stage, a large amount of project material and templated assets have been created, as well as a chunking strategy.

The challenge is that to generate all required technical code assets of the project would likely exceed the output capabilities of a large language model

Use a maximum of 20,000 output characters to deliver on the output chunk.

Reminder: ONLY GENERATE code relating to the mentioned sprint

Your response should be an executable python file with the following characteristics
- Will touch/mkdir for any new files (however, reuse existing files as much as possible)
- Write code text to the files (patch existing code as required)
- Print further directions and context to the command line

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
