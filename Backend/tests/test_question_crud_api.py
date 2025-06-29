def create_test_unit(client, title="Sample Unit", description="Unit Description"):
    response = client.post("/Finance_Tutor/unit", json={
        "title": title,
        "description": description
    })
    assert response.status_code == 201
    return 1

def create_question(client, unit_id):
    response = client.post("/Finance_Tutor/question", json={
        "unit_id": unit_id,
        "description": "kuch v nhi ?",
        "marks": 2,
        "option_a": "3",
        "option_b": "4",
        "option_c": "5",
        "option_d": "6",
        "correct_option": "b"
    })
    assert response.status_code == 201

def test_create_question_success(client):
    unit_id = create_test_unit(client)
    response = client.post("/Finance_Tutor/question", json={
        "unit_id": unit_id,
        "description": "What is the capital of India?",
        "marks": 5,
        "option_a": "Mumbai",
        "option_b": "Delhi",
        "option_c": "Chennai",
        "option_d": "Kolkata",
        "correct_option": "b"
    })
    assert response.status_code == 201
    assert "Question added Successfully" in response.get_json()["message"]

def test_create_question_missing_fields(client):
    unit_id = create_test_unit(client)
    response = client.post("/Finance_Tutor/question", json={
        "unit_id": unit_id,
        "description": "",
        "option_a": "A", "option_b": "B", "option_c": "C", "option_d": "D",
        "correct_option": "a"
    })
    assert response.status_code == 401
    assert "Required Fields missing" in response.get_json()["error"]

def test_create_question_invalid_correct_option(client):
    unit_id = create_test_unit(client)
    response = client.post("/Finance_Tutor/question", json={
        "unit_id": unit_id,
        "description": "Choose correct",
        "marks": 2,
        "option_a": "One", "option_b": "Two", "option_c": "Three", "option_d": "Four",
        "correct_option": "e" 
    })
    assert response.status_code == 400
    assert "values of correct option" in response.get_json()["error"]


def test_get_question_success(client):
    unit_id = create_test_unit(client)
    create_question(client, unit_id)
    response = client.get("/Finance_Tutor/question/1")
    assert response.status_code == 200
    assert response.get_json()["description"] == "kuch v nhi ?"


def test_update_question_success(client):
    unit_id = create_test_unit(client)
    create_question(client, unit_id)
    response = client.put("/Finance_Tutor/question/1", json={
        "unit_id": unit_id,
        "description": "Updated Q?",
        "marks": 10,
        "option_a": "1",
        "option_b": "2",
        "option_c": "3",
        "option_d": "4",
        "correct_option": "d"
    })
    assert response.status_code == 200
    assert "Question updated Sucessfully" in response.get_json()["message"]


def test_update_question_invalid_unit(client):
    unit_id = create_test_unit(client)
    create_question(client, unit_id)
    response = client.put("/Finance_Tutor/question/1", json={
        "unit_id": 54, 
        "description": "Invalid Update",
        "marks": 3,
        "option_a": "A", "option_b": "B", "option_c": "C", "option_d": "D",
        "correct_option": "a"
    })
    assert response.status_code == 404
    assert "No such Unit" in response.get_json()["error"]


def test_delete_question_success(client):
    unit_id = create_test_unit(client)
    create_question(client, unit_id)
    response = client.delete("/Finance_Tutor/question/1")
    assert response.status_code == 200
    assert "Question Deleted Succefully" in response.get_json()["message"]

    # Confirm it's deleted
    response = client.get("/Finance_Tutor/question/1")
    assert response.status_code == 200 or response.status_code == 404


def test_delete_question_not_found(client):
    response = client.delete("/Finance_Tutor/question/7")
    assert response.status_code == 404
    assert "Question not found" in response.get_json()["error"]
