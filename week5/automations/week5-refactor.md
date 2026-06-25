---
description: Rename a week5 backend module, update imports, then lint and test
argument-hint: [old-path new-path e.g. backend/app/services/extract.py backend/app/services/parser.py]
allowed-tools: Bash, Read, Write, Edit, Grep
---

Safely rename a Python module under `week5/backend/` and verify the repo still passes checks.

## Inputs
User arguments: `$ARGUMENTS` — two paths relative to `week5/`:
- `$0` — current module path (file `.py`)
- `$1` — new module path (file `.py`)

## Steps
1. Validate both paths exist / are plausible; refuse if outside `week5/backend/`.
2. `git mv` (or move + stage) the file from `$0` to `$1`.
3. Grep the repo for imports referencing the old module name; update all references (routers, tests, services).
4. From `week5/` run:
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
- Rollback: `git checkout -- week5/` restores all week5 files.