def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    body = r.json()
    assert "items" in body
    assert "total" in body
    assert len(body["items"]) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200
    body = r.json()
    assert "items" in body

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    body = r.json()
    assert len(body["items"]) >= 1


def test_search_pagination_and_sorting(client):
    # Create multiple notes
    for i in range(5):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

    # Test pagination
    r = client.get("/notes/search/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert len(body["items"]) == 2
    assert body["total"] >= 5
    assert body["page"] == 1
    assert body["page_size"] == 2

    # Test sorting by title_asc
    r = client.get("/notes/search/", params={"sort": "title_asc", "page_size": 5})
    assert r.status_code == 200
    body = r.json()
    titles = [item["title"] for item in body["items"]]
    assert titles == sorted(titles)

    # Test case-insensitive search
    r = client.get("/notes/search/", params={"q": "content"})
    assert r.status_code == 200
    body = r.json()
    assert len(body["items"]) >= 5

    r = client.get("/notes/search/", params={"q": "CONTENT"})
    assert r.status_code == 200
    body = r.json()
    assert len(body["items"]) >= 5


def test_list_notes_pagination(client):
    for i in range(3):
        client.post("/notes/", json={"title": f"PageNote {i}", "content": f"Content {i}"})

    r = client.get("/notes/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert len(body["items"]) == 2
    assert body["total"] >= 3


def test_update_note(client):
    r = client.post("/notes/", json={"title": "Original", "content": "Original content"})
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"
    assert r.json()["content"] == "Original content"

    r = client.put(f"/notes/{note_id}", json={"content": "Updated content"})
    assert r.status_code == 200
    assert r.json()["content"] == "Updated content"

    # 404 on non-existent
    r = client.put("/notes/99999", json={"title": "Nope"})
    assert r.status_code == 404


def test_delete_note(client):
    r = client.post("/notes/", json={"title": "Delete me", "content": "Bye"})
    note_id = r.json()["id"]

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404

    # 404 on non-existent
    r = client.delete("/notes/99999")
    assert r.status_code == 404


def test_extract_endpoint(client):
    content = "My note with #hashtag and - [ ] task item!"
    r = client.post("/notes/", json={"title": "Extract test", "content": content})
    note_id = r.json()["id"]

    # Without apply
    r = client.post(f"/notes/{note_id}/extract")
    assert r.status_code == 200
    data = r.json()
    assert "hashtags" in data
    assert "action_items" in data
    assert "hashtag" in data["hashtags"]
    assert len(data["action_items"]) >= 1

    # With apply
    r = client.post(f"/notes/{note_id}/extract", params={"apply": True})
    assert r.status_code == 200

    # Verify action items were created
    r = client.get("/action-items/")
    items = r.json()["items"]
    assert any("task item" in item["description"] for item in items)

    # 404 on non-existent note
    r = client.post("/notes/99999/extract")
    assert r.status_code == 404