def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    body = r.json()
    assert "items" in body
    assert len(body["items"]) == 1


def test_filter_action_items(client):
    for desc in ["Task A", "Task B", "Task C"]:
        r = client.post("/action-items/", json={"description": desc})
        item_id = r.json()["id"]
        if desc == "Task B":
            client.put(f"/action-items/{item_id}/complete")

    # Filter completed
    r = client.get("/action-items/", params={"completed": True})
    assert r.status_code == 200
    body = r.json()
    assert all(item["completed"] for item in body["items"])

    # Filter incomplete
    r = client.get("/action-items/", params={"completed": False})
    assert r.status_code == 200
    body = r.json()
    assert all(not item["completed"] for item in body["items"])


def test_bulk_complete(client):
    ids = []
    for i in range(3):
        r = client.post("/action-items/", json={"description": f"Bulk item {i}"})
        ids.append(r.json()["id"])

    r = client.post("/action-items/bulk-complete", json=ids)
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["completed"] == 3

    # Verify all completed
    r = client.get("/action-items/", params={"completed": True})
    assert r.status_code == 200
    assert len(r.json()["items"]) >= 3

    # 404 on non-existent ids
    r = client.post("/action-items/bulk-complete", json=[99999])
    assert r.status_code == 404


def test_list_action_items_pagination(client):
    for i in range(3):
        client.post("/action-items/", json={"description": f"Page item {i}"})

    r = client.get("/action-items/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert "items" in body
    assert "total" in body
    assert len(body["items"]) == 2