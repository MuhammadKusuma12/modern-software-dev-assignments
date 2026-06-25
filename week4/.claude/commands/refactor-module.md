---
argument-hint: <old-path> <new-path>
description: Rename a Python module and fix imports
allowed-tools: Bash Read Write Grep Edit Glob
---

Rename a backend module and update all references.

Steps:
1. cd week4
2. Validate inputs: $ARGUMENTS must be exactly two paths inside `backend/` (e.g. `backend/app/services/extract.py backend/app/services/parser.py`)
3. Refuse if either path is outside `backend/` or does not end with `.py`
4. `git mv "$0" "$1"` (rename file)
5. Update imports in all `.py` files under `backend/` that reference the old module path:
   - Search for old module stem and package references
   - Replace with new path, preserving relative/absolute style
6. Run `make lint` and `make test`
7. Report: list of modified files, lint status, test status
8. If anything fails red, stop and report what to fix manually; do not auto-revert
