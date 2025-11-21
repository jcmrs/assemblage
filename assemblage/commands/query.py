"""
assemblage.commands.query

Logic for the 'query' command.
"""

import sys

from assemblage import code_search

RED = "\033[0;31m"
NC = "\033[0m"


def run(args):
    """Handler for the 'query' command."""
    print("--- Control Plane: Executing 'query' ---")
    try:
        results = code_search.search_index(args.query)
        if not results:
            print("No relevant code snippets found.")
        else:
            print(f"**Top {len(results)} Results:**\n")
            for i, res in enumerate(results):
                print("---")
                print(f"**{i+1}. File:** `{res['path']}`")
                print(f"**Lines:** {res['line']}")
                print(f"**Confidence Score:** {res['score']:.2f}\n")
                print(f"```python\n{res['content']}\n```")
            print("---\n")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}ERROR: Query failed: {e}{NC}", file=sys.stderr)
        sys.exit(1)
