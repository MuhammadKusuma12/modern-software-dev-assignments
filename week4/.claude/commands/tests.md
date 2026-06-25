---
argument-hint: [pytest-path-or-marker]
description: Run tests with optional coverage in week4
allowed-tools: Bash Read
---

Run tests in the week4 starter app.

Steps:
1. cd week4
2. If $ARGUMENTS is provided, run `PYTHONPATH=. pytest -q backend/tests $ARGUMENTS --maxfail=1 -x`
3. Otherwise run `PYTHONPATH=. pytest -q backend/tests --maxfail=1 -x`
4. If tests pass, run `PYTHONPATH=. pytest -q backend/tests --cov=backend/app --cov-report=term-missing`
5. Summarize: failing files, error count, coverage percentage
6. If red, suggest next debugging step (e.g. "Run failing test in isolation", "Check conftest.py DB fixture")
