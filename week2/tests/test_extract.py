"""Unit tests for action item extraction (heuristic and LLM-powered)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from week2.app.services.extract import extract_action_items, extract_action_items_llm


# --- Heuristic extractor tests (starter) ---


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# --- LLM extractor tests (Exercise 2) ---


def _mock_ollama_response(items: list[str]) -> MagicMock:
    """Build a fake Ollama chat response with structured JSON content."""
    mock_response = MagicMock()
    mock_response.message.content = json.dumps({"items": items})
    return mock_response


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_bullet_list(mock_chat):
    mock_chat.return_value = _mock_ollama_response(
        ["Set up database", "Implement API endpoint", "Write tests"]
    )
    text = """
    - [ ] Set up database
    - Implement API endpoint
    - Write tests
    """
    items = extract_action_items_llm(text)
    assert items == ["Set up database", "Implement API endpoint", "Write tests"]
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_keyword_prefixes(mock_chat):
    mock_chat.return_value = _mock_ollama_response(
        ["Review pull request", "Deploy to staging"]
    )
    text = """
    todo: Review pull request
    action: Deploy to staging
    """
    items = extract_action_items_llm(text)
    assert "Review pull request" in items
    assert "Deploy to staging" in items


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_empty_input(mock_chat):
    items = extract_action_items_llm("")
    assert items == []
    items = extract_action_items_llm("   \n  ")
    assert items == []
    mock_chat.assert_not_called()


@patch("week2.app.services.extract.chat")
def test_extract_action_items_llm_deduplicates(mock_chat):
    mock_chat.return_value = _mock_ollama_response(
        ["Fix bug", "fix bug", "Add tests"]
    )
    items = extract_action_items_llm("Fix bug\nfix bug\nAdd tests")
    assert items == ["Fix bug", "Add tests"]
