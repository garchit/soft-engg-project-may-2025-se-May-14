def create_test_unit(client):
    response = client.post("/Finance_Tutor/unit", json={
        "title": "unit 1",
        "chapter_id": 1 
    })
    assert response.status_code == 201

def create_test_lecture(client):
    create_test_unit(client)
    response = client.post("/Finance_Tutor/lecture", json={
        "title": "Introduction to finance",
        "description": "Basics of finance",
        "link": "http://example.com/finance",
        "unit_id": 1
    })
    assert response.status_code == 201
    return response.get_json()["id"]

def test_create_lecture_success(client):
    create_test_unit(client)
    response = client.post("/Finance_Tutor/lecture", json={
        "title": "finance intro",
        "description": "Lecture 1",
        "link": "http://example.com/fi",
        "unit_id": 1
    })
    assert response.status_code == 201
    assert "Lecture added successfully" in response.get_json()["message"]

def test_create_lecture_missing_fields(client):
    create_test_unit(client)
    response = client.post("/Finance_Tutor/lecture", json={
        "description": "there is no title",
        "link": "http://example.com/missing",
        "unit_id": 1
    })
    assert response.status_code == 400
    assert "Title and Unit ID are required" in response.get_json()["error"]

def test_create_lecture_duplicate_title(client):
    create_test_lecture(client)
    response = client.post("/Finance_Tutor/lecture", json={
        "title": "Introduction to finance",  # same title, same unit
        "description": "Duplicate check",
        "link": "http://example.com/dup",
        "unit_id": 1
    })
    assert response.status_code == 400
    assert "already exists" in response.get_json()["error"]

def test_get_lecture_success(client):
    lecture_id = create_test_lecture(client)
    response = client.get(f"/Finance_Tutor/lecture/{lecture_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Introduction to finance"

def test_get_lecture_not_found(client):
    response = client.get("/Finance_Tutor/lecture/10")
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"]

def test_update_lecture_success(client):
    lecture_id = create_test_lecture(client)
    response = client.put(f"/Finance_Tutor/lecture/{lecture_id}", json={
        "title": "Updated finance Lecture",
        "description": "Updated description",
        "link": "http://example.com/updated",
        "unit_id": 1
    })
    assert response.status_code == 200
    assert "updated successfully" in response.get_json()["message"]

def test_update_lecture_invalid_unit(client):
    lecture_id = create_test_lecture(client)
    response = client.put(f"/Finance_Tutor/lecture/{lecture_id}", json={
        "title": "Bad Update",
        "description": "Invalid unit",
        "link": "http://example.com/invalid",
        "unit_id": 11  
    })
    assert response.status_code == 400
    assert "Invalid unit_id" in response.get_json()["error"]

def test_update_lecture_duplicate_title(client):
    create_test_lecture(client)
    client.post("/Finance_Tutor/lecture", json={
        "title": "Another Lecture",
        "description": "Desc",
        "link": "link",
        "unit_id": 1
    })
    # try updating lecture 2 with lecture 1's title
    response = client.put("/Finance_Tutor/lecture/2", json={
        "title": "Introduction to finance",
        "description": "Dup title",
        "link": "link",
        "unit_id": 1
    })
    assert response.status_code == 400
    assert "already exists in the unit" in response.get_json()["error"]

def test_delete_lecture_success(client):
    lecture_id = create_test_lecture(client)
    response = client.delete(f"/Finance_Tutor/lecture/{lecture_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.get_json()["message"]

    # Confirm deletion
    get_resp = client.get(f"/Finance_Tutor/lecture/{lecture_id}")
    assert get_resp.status_code == 404

def test_delete_lecture_not_found(client):
    response = client.delete("/Finance_Tutor/lecture/5")
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"]
