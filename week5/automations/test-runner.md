---
description: Warp Drive Automation — Run week5 test suite with coverage reporting
argument-hint: [optional pytest args like -k search]
---

# Week 5 Test Runner

Run the Week 5 test suite and coverage report from the `week5/` directory.

## Usage

```bash
# Run all tests with coverage
bash week5/automations/run-tests.sh

# Run specific tests
bash week5/automations/run-tests.sh -k search

# Run a specific test file
bash week5/automations/run-tests.sh backend/tests/test_notes.py
```

## What it does
1. Runs `pytest` with `--maxfail=1 -x` (stop on first failure)
2. If tests pass, runs coverage with `--cov=backend/app --cov-report=term-missing`
3. Reports modules below 80% coverage
4. If tests fail, shows the failure details without running coverage

## Saved Prompt (copy into Warp Drive)

```
Title: Week 5 Test + Coverage
Prompt:
Run the week5 test suite from the week5/ directory:
1. cd week5
2. PYTHONPATH=. python -m pytest -q backend/tests --maxfail=1 -x
3. If all pass, run: PYTHONPATH=. python -m pytest -q backend/tests --cov=backend/app --cov-report=term-missing
4. Show pass/fail count, coverage %, and any modules below 80% coverage