---
description: Rename a week4 backend module, update imports, then lint and test
argument-hint: [old-path new-path e.g. backend/app/services/extract.py backend/app/services/parser.py]
allowed-tools: Bash, Read, Write, Edit, Grep
---

Safely rename a Python module under `week4/backend/` and verify the repo still passes checks.

## Inputs
User arguments: `$ARGUMENTS` — two paths relative to `week4/`:
- `$0` — current module path (file `.py`)
- `$1` — new module path (file `.py`)

## Steps
1. Validate both paths exist / are plausible; refuse if outside `week4/backend/`.
2. `git mv` (or move + stage) the file from `$0` to `$1`.
3. Grep the repo for imports referencing the old module name; update all references (routers, tests, services).
4. From `week4/` run:
   ```bash
   make format && make lint && make test
   ```
5. Output a checklist:
   - [ ] File renamed
   - [ ] Imports updated (list each file touched)
   - [ ] Lint clean
   - [ ] Tests green
6. If tests fail, revert import changes and report blockers — do not leave the tree half-refactored.

## Safety
- One module rename per invocation.
- Do not rename `main.py`, `db.py`, or `models.py` without explicit confirmation.
- Rollback: `git checkout -- week4/` restores all week4 files.
