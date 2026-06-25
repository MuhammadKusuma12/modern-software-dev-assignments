#!/usr/bin/env python3
"""Open and display the contents of README.md in week7."""

import sys
from pathlib import Path


def main():
    readme_path = Path(__file__).parent / "README.md"

    if not readme_path.exists():
        print(f"Error: README.md not found at {readme_path}", file=sys.stderr)
        sys.exit(1)

    content = readme_path.read_text(encoding="utf-8")
    print(content)


if __name__ == "__main__":
    main()