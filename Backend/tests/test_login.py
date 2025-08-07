#### Testcase for user and institute login ####

# testcase when user login successfully
def test_user_login_success(client):
    # First, create an institute that the user can link to
    client.post("/Finance_Tutor/institute/signup", json={
        "name": "Test Institute",
        "email": "testinstitute@example.com",
        "password": "inst123",
        "address": "City Road"
    })

    # Now create a user linked to that institute
    client.post("/Finance_Tutor/User/signup", json={
        "full_name": "Rajeev Kumar",
        "username": "rajeev123",
        "email": "rajeev@example.com",
        "password": "test1234",
        "parents_email": "parent@example.com",
        "dob": "2000-01-01",
        "user_type": "student",
        "institute_id": 1,  # This must match the created institute
        "user_class": "10"
    })

    # Now test login
    response = client.post("/Finance_Tutor/login", json={
        "email": "rajeev@example.com",
        "password": "test1234"
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "Login is successful"

# testcase when user trying to login with missing fields
def test_login_missing_fields(client):
    response = client.post("/Finance_Tutor/login", json={
        "email": "", "password": ""
    })
    assert response.status_code == 400
    assert response.get_json()["error"] == "Email and password are required."

# testcase when user login with wrong password
def test_login_wrong_password(client):
    # Create user
    client.post("/Finance_Tutor/institute/signup", json={
        "name": "WrongPassInstitute",
        "email": "wp@example.com",
        "password": "inst123",
        "address": "Somewhere"
    })

    client.post("/Finance_Tutor/User/signup", json={
        "full_name": "Test User",
        "username": "testuser123",
        "email": "user@example.com",
        "password": "correctpass",
        "parents_email": "parent@example.com",
        "dob": "2002-05-10",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "12"
    })

    # Try wrong password
    response = client.post("/Finance_Tutor/login", json={
        "email": "user@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.get_json()["error"] == "Wrong password. Invalid credentials."


# Testcase when institute login successfully
def test_institute_login_success(client):
    client.post("/Finance_Tutor/institute/signup", json={
        "name": "Inst A",
        "email": "inst@example.com",
        "password": "instpass",
        "address": "Delhi"
    })

    response = client.post("/Finance_Tutor/login", json={
        "email": "inst@example.com",
        "password": "instpass"
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "Login is Successful"
    assert response.get_json()["name"] == "Inst A"


# Testcase when institute login with wrong password
def test_institute_login_wrong_password(client):
    client.post("/Finance_Tutor/institute/signup", json={
        "name": "Inst B",
        "email": "instb@example.com",
        "password": "correctinstpass",
        "address": "Mumbai"
    })

    response = client.post("/Finance_Tutor/login", json={
        "email": "instb@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid Credentials"

#Testcase when institute login with empty email and password
def test_login_with_empty_email_and_password(client):
    response = client.post("/Finance_Tutor/login", json={
        "email": "",
        "password": ""
    })
    assert response.status_code == 400
    assert response.get_json()["error"] == "Email and password are required."

