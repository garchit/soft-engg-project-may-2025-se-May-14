
def test_user_not_found(client):
    response = client.get('/Finance_Tutor/User/999')
    assert response.status_code == 404
    assert response.get_json()['error'] == "User not found"

def test_create_user(client):
    payload = {
        "full_name": "John Doe",
        "username": "johndoe123",
        "email": "john@example.com",
        "password": "secure123",
        "parents_email": "parent@example.com",
        "dob": "2000-01-01",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "10"
    }

    response = client.post("/Finance_Tutor/User/signup", json=payload)

    assert response.status_code == 201
    assert response.get_json()["message"] == "User created successfully"

def test_duplicate_email(client):
    payload = {
        "full_name": "Alice",
        "username": "alice123",
        "email": "john@example.com",
        "password": "pass123",
        "parents_email": "parent@example.com",
        "dob": "2001-01-01",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "9"
    }
    client.post("/Finance_Tutor/User/signup", json=payload)
    payload["username"] = "anotheruser"
    response = client.post("/Finance_Tutor/User/signup", json=payload)
    assert response.status_code == 400
    assert "Email is already in use" in response.get_json()["error"]

def test_duplicate_username(client):
    payload = {
        "full_name": "Bob",
        "username": "bob123",
        "email": "bob@example.com",
        "password": "pass123",
        "parents_email": "parent@example.com",
        "dob": "2002-02-02",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "8"
    }
    client.post("/Finance_Tutor/User/signup", json=payload)
    payload["email"] = "bob2@example.com"
    response = client.post("/Finance_Tutor/User/signup", json=payload)
    assert response.status_code == 400
    assert "Username is already taken" in response.get_json()["error"]


# dob is not in correct format
def test_invalid_dob_format(client):
    payload = {
        "full_name": "Charlie",
        "username": "charlie123",
        "email": "charlie@example.com",
        "password": "pass123",
        "parents_email": "parent@example.com",
        "dob": "01-02-2002",  # wrong format
        "user_type": "student",
        "institute_id": 1,
        "user_class": "10"
    }
    response = client.post("/Finance_Tutor/User/signup", json=payload)
    assert response.status_code == 400
    assert "DOB must be in YYYY-MM-DD format" in response.get_json()["error"]

def test_invalid_user_type(client):
    payload = {
        "full_name": "Daisy",
        "username": "daisy123",
        "email": "daisy@example.com",
        "password": "pass123",
        "parents_email": "parent@example.com",
        "dob": "2000-05-05",
        "user_type": "teacher",  # invalid
        "institute_id": 1,
        "user_class": "10"
    }
    response = client.post("/Finance_Tutor/User/signup", json=payload)
    assert response.status_code == 400
    assert "Invalid user_type" in response.get_json()["error"]
