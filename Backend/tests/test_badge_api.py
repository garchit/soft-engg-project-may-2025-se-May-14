## Testcase for Badge Crud ##

import pytest
from models.badges import Badge
from models import db


# creating a badge
def test_create_badge_success(client):
    res = client.post("/Finance_Tutor/badge", json={
        "name": "SimpleBadge",
        "description": "A test badge",
        "points": 10
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["badge"]["name"] == "SimpleBadge"
    assert data["badge"]["points"] == 10


# creating a badge with missing fields
def test_create_badge_missing_fields(client):
    res1 = client.post("/Finance_Tutor/badge", json={"description": "desc", "points": 1})
    assert res1.status_code == 400
    assert "'name' field is required." in res1.get_json().get("error", "")

    res2 = client.post("/Finance_Tutor/badge", json={"name": "NoPoints", "description": "desc"})
    assert res2.status_code == 400
    assert "'points' field is required." in res2.get_json().get("error", "")

# creating a badge with missing fields
def test_create_duplicate_badge_name(client):
    payload = {"name": "Dup", "description": "first", "points": 5}
    r1 = client.post("/Finance_Tutor/badge", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/Finance_Tutor/badge", json=payload)
    assert r2.status_code == 400
    assert "already exists" in r2.get_json().get("error", "")


# trying to get all badges but not found
def test_get_all_badges_empty(client):
    res = client.get("/Finance_Tutor/badge")
    assert res.status_code == 200
    data = res.get_json()
    assert "list_badges" in data
    assert isinstance(data["list_badges"], list)
    assert len(data["list_badges"]) == 0


# get all badges with relevant data
def test_get_all_badges_with_data(client):
    client.post("/Finance_Tutor/badge", json={"name": "B1", "description": "d1", "points": 1})
    client.post("/Finance_Tutor/badge", json={"name": "B2", "description": "d2", "points": 2})
    res = client.get("/Finance_Tutor/badge")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["list_badges"]) == 2


# trying to fetch single badge but not found in database
def test_get_single_badge_not_found(client):
    res = client.get("/Finance_Tutor/badge/12")
    assert res.status_code == 404
    assert "not found" in res.get_json()["message"].lower()


# get single badge successfully
def test_get_single_badge_success(client):
    created = client.post("/Finance_Tutor/badge", json={"name": "One", "description": "desc", "points": 3})
    badge_id = created.get_json()["badge"]["id"]
    res = client.get(f"/Finance_Tutor/badge/{badge_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["id"] == badge_id
    assert data["name"] == "One"

# update badge
def test_update_badge_success(client):
    created = client.post("/Finance_Tutor/badge", json={"name": "Old", "description": "old", "points": 4})
    badge_id = created.get_json()["badge"]["id"]
    res = client.put(f"/Finance_Tutor/badge/{badge_id}", json={
        "name": "New",
        "description": "new",
        "points": 8
    })
    assert res.status_code == 200
    updated = res.get_json()["badge"]
    assert updated["name"] == "New"
    assert updated["points"] == 8

# update badge with invalid badge point
def test_update_badge_invalid_points(client):
    created = client.post("/Finance_Tutor/badge", json={"name": "P", "description": "x", "points": 2})
    badge_id = created.get_json()["badge"]["id"]
    res = client.put(f"/Finance_Tutor/badge/{badge_id}", json={
        "name": "P",
        "description": "x",
        "points": -5
    })
    assert res.status_code == 400
    assert "non-negative integer" in res.get_json()["message"].lower()


# delete badge successfully
def test_delete_badge_success(client):
    created = client.post("/Finance_Tutor/badge", json={"name": "ToDelete", "description": "d", "points": 1})
    badge_id = created.get_json()["badge"]["id"]
    res = client.delete(f"/Finance_Tutor/badge/{badge_id}")
    assert res.status_code == 200
    # verify deletion
    res2 = client.get(f"/Finance_Tutor/badge/{badge_id}")
    assert res2.status_code == 404

# trying to delete badge but badge not found
def test_delete_badge_not_found(client):
    res = client.delete("/Finance_Tutor/badge/123456")
    assert res.status_code == 404
    assert "not found" in res.get_json()["message"].lower()
