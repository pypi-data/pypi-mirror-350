At this stage, we want to reflect on the project and propose a new milestone direction.

We have build significant information in the PRD and codefiles.
The challenge is that to generate all required technical code assets of the project would likely exceed the output capabilities of a large language model.

With that in mind, lets take the assumption that a large langauge model could output 20,000 characters of text maximum.

Your task is to do the following:

1. Evaluate the current state of the project
2. Determine a next major milestone
3. Evaluate the approximate total project size in terms of characters of the next major milestone
4. Determine the best approach to split the work into manageable chunks of output, with respect to chunking the work by logical separation of concerns, so as to test and confirm expected behaviour, language model output limits, and also human time spent performing work over chunks (i.e. not more than 5 chunks)
5. Rank order the list of chunks by your recommendation of which chunk to start first, with respect to most needed in terms of scaffolding
6. Provide a introductory two paragraphs explaining your reasoning and approach, and then, how it applies to the prompt brief provided

You must list chunks in terms of numbers, do not use lettering.
They should always be referred to as `Chunk 1`, `Chunk 2`, `Chunk n`
Never as `1- Chunk` or `4) Chunk` etc.

While your task at this stage does not require actual execution of code, this is more of a planning step, the following is useful context:

Assume that you are being run from an unknown folder within the codebase - use the following code to find the root repo path
from personalvibe import vibe_utils
REPO = vibe_utils.get_base_path()
