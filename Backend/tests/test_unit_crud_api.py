def test_create_unit_success(client):
    response = client.post("/Finance_Tutor/unit", json={
        "title": "Math Basics",
        "description": "Introductory math concepts"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Unit added Succesfully"

def test_create_unit_duplicate_title(client):
    client.post("/Finance_Tutor/unit", json={
        "title": "Physics",
        "description": "Physics basics"
    })
    response = client.post("/Finance_Tutor/unit", json={
        "title": "Physics",
        "description": "Duplicate title"
    })
    assert response.status_code == 400
    assert "Title Already Exist" in response.get_json()["error"]

def test_get_unit_success(client):
    client.post("/Finance_Tutor/unit", json={
        "title": "Biology",
        "description": "Life sciences"
    })
    response = client.get("/Finance_Tutor/unit/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Biology"
    assert data["description"] == "Life sciences"

def test_update_unit_success(client):
    client.post("/Finance_Tutor/unit", json={
        "title": "Chemistry",
        "description": "study"
    })
    response = client.put("/Finance_Tutor/unit/1", json={
        "title": "Advanced Chemistry",
        "description": "studies"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Advanced Chemistry"
    assert data["description"] == "studies"

def test_delete_unit_success(client):
    client.post("/Finance_Tutor/unit", json={
        "title": "Geography",
        "description": "Earth study"
    })
    response = client.delete("/Finance_Tutor/unit/1")
    assert response.status_code == 200
    assert "Unit Deleted Successfully" in response.get_json()["message"]

def test_get_unit_not_found(client):
    response = client.get("/Finance_Tutor/unit/12")
    assert response.status_code == 404
    assert "Unit not found" in response.get_json()["error"]
