# Copyright © 2025 by Nick Jenkins. All rights reserved

"""
Renders the PRD-milestone prompt, calls the LLM once, saves I/O, and
returns the raw response (caller can parse or display).

extra_vars lets you push in ad-hoc template vars without changing
the function signature every time.
"""

"""
Interactive sprint executor. Yields every assistant response so the
caller can inspect success/failure and decide to break early.

It loops up to `max_iterations` times, passing previous assistant
output back in as context when needed.
"""
