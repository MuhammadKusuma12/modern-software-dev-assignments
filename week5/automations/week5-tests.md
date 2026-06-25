---
description: Run week5 pytest suite with optional path/marker; report coverage on success
argument-hint: [pytest-path-or-marker e.g. backend/tests/test_notes.py or -k search]
allowed-tools: Bash, Read, Grep
---

Run the Week 5 test suite from the `week5/` directory.

## Context
- Working directory: `week5/`
- Default test command: `PYTHONPATH=. pytest -q backend/tests --maxfail=1 -x`
- Optional filter from user: `$ARGUMENTS`

## Steps
1. `cd week5` (or confirm cwd is `week5/`).
2. If `$ARGUMENTS` is non-empty, run:
   ```bash
   PYTHONPATH=. pytest -q backend/tests --maxfail=1 -x $ARGUMENTS
   ```
   Otherwise run the default command above.
3. If tests **fail**:
   - Summarize each failure (test name, assertion, file:line if shown).
   - Suggest the smallest next fix (do not refactor unrelated code).
   - Stop; do not run coverage.
4. If tests **pass**:
   - Run coverage:
     ```bash
     PYTHONPATH=. pytest -q backend/tests --cov=backend/app --cov-report=term-missing
     ```
   - List modules below 80% coverage, if any.
5. Output a short summary: pass/fail count, coverage percentage, and recommended next step.

## Safety
- Only run pytest/black/ruff inside `week5/`.
- Do not modify production DB files under `week5/data/` except via test fixtures.
- Do not skip failing tests without explicit user approval.