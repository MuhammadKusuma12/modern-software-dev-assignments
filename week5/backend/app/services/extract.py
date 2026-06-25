import re


def extract_action_items(text: str) -> list[str]:
    """Extract action items from text.
    Detects lines starting with '- [ ]' (markdown task) or '- TODO:' or ending with '!'."""
    items = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        # Markdown task: - [ ] or * [ ]
        if re.match(r"^[-*]\s*\[ \]\s*", stripped):
            items.append(re.sub(r"^[-*]\s*\[ \]\s*", "", stripped))
        # Explicit TODO:
        elif stripped.lower().startswith("todo:"):
            items.append(stripped)
        # Ends with !
        elif stripped.endswith("!"):
            # Remove leading bullet if present
            items.append(stripped.lstrip("- *"))
        # Starts with - or * as a bullet
        elif re.match(r"^[-*]\s+", stripped):
            potential = re.sub(r"^[-*]\s+", "", stripped)
            if potential.lower().startswith("todo:"):
                items.append(potential)
    return [item.strip() for item in items]


def extract_hashtags(text: str) -> list[str]:
    """Extract unique hashtags from text."""
    tags = re.findall(r"#(\w+)", text)
    return list(dict.fromkeys(tags))  # dedup preserving order


def extract_from_note(text: str) -> dict:
    """Run all extractors and return structured results."""
    return {
        "hashtags": extract_hashtags(text),
        "action_items": extract_action_items(text),
    }