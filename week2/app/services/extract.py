from __future__ import annotations

import re
from typing import List

from ollama import chat

from ..config import get_settings
from ..schemas import ActionItemsLLMResult

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    return _dedupe_preserve_order(extracted)


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def _dedupe_preserve_order(items: List[str]) -> List[str]:
    """Remove duplicate action items while preserving original order."""
    seen: set[str] = set()
    unique: List[str] = []
    for item in items:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


# --- LLM-powered extraction (Exercise 1) ---


def extract_action_items_llm(text: str) -> List[str]:
    """
    Extract action items from free-form notes using an Ollama LLM with structured JSON output.

    Uses Pydantic schema enforcement via Ollama's `format` parameter so the model returns
    a predictable JSON object: {"items": ["...", ...]}.
    """
    stripped = text.strip()
    if not stripped:
        return []

    settings = get_settings()
    response = chat(
        model=settings.ollama_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract actionable tasks from meeting notes and free-form text. "
                    "Return only concrete, imperative action items as a JSON object with an "
                    "'items' array of strings. Strip bullet markers, checkboxes, and prefixes "
                    "like 'todo:' from each item. Ignore narrative or descriptive sentences "
                    "that are not tasks."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Extract all action items from the notes below. Return as JSON.\n\n"
                    f"{stripped}"
                ),
            },
        ],
        format=ActionItemsLLMResult.model_json_schema(),
        options={"temperature": 0},
    )

    result = ActionItemsLLMResult.model_validate_json(response.message.content)
    cleaned = [item.strip() for item in result.items if item.strip()]
    return _dedupe_preserve_order(cleaned)
