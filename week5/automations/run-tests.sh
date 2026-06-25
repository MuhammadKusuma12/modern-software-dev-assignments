#!/usr/bin/env bash
# Warp Drive Automation: Run tests + coverage for week5
# Usage: bash week5/scripts/run-tests.sh [optional pytest args]
set -euo pipefail

cd "$(dirname "$0")/.."

echo "=== Week 5 Test Runner ==="
echo ""

# Run tests
if [ $# -eq 0 ]; then
    echo ">>> Running all tests..."
    PYTHONPATH=. python -m pytest -q backend/tests --maxfail=1 -x
else
    echo ">>> Running tests with args: $*"
    PYTHONPATH=. python -m pytest -q backend/tests --maxfail=1 -x "$@"
fi

TEST_EXIT=$?

if [ $TEST_EXIT -ne 0 ]; then
    echo ""
    echo "!!! TESTS FAILED (exit code $TEST_EXIT)"
    echo "Fix the failures before proceeding."
    exit $TEST_EXIT
fi

echo ""
echo ">>> All tests passed! Running coverage..."

PYTHONPATH=. python -m pytest -q backend/tests --cov=backend/app --cov-report=term-missing

echo ""
echo "=== Done ==="