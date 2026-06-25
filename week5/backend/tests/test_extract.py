from backend.app.services.extract import extract_action_items, extract_hashtags, extract_from_note


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "Ship it!" in items


def test_extract_markdown_tasks():
    text = """
    - [ ] Buy groceries
    - [x] Done task (not extracted)
    * [ ] Another task
    """
    items = extract_action_items(text)
    assert "Buy groceries" in items
    assert "Another task" in items
    assert "Done task" not in items


def test_extract_hashtags():
    text = "Hello #world and #hello again #world"
    tags = extract_hashtags(text)
    assert "world" in tags
    assert "hello" in tags
    # Deduplicated, preserving order
    assert tags == ["world", "hello"]


def test_extract_no_hashtags():
    assert extract_hashtags("no hashtags here") == []


def test_extract_from_note():
    text = """
    #project note
    - [ ] implement feature
    TODO: write docs
    Nothing here
    """.strip()
    result = extract_from_note(text)
    assert "hashtags" in result
    assert "action_items" in result
    assert "project" in result["hashtags"]
    assert "implement feature" in result["action_items"]
    assert "TODO: write docs" in result["action_items"]
