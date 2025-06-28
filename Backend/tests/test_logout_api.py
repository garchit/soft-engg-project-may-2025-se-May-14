from datetime import datetime

def test_logout_without_login(client):
    response = client.post("/Finance_Tutor/logout")
    assert response.status_code in (302, 401)


def test_user_logout_success(client):

    with client:
        client.post("/Finance_Tutor/User/signup", json={
            "full_name": "shiksha tiwari",
            "username": "shiksha123",
            "email": "shiksha@ds.study.in",
            "password": "let564",
            "parents_email": "parent@example.com",
            "dob": "2002-02-19",
            "user_type": "student",
            "institute_id": 1,
            "user_class": "10"
        })

        # 2. Login
        login_response = client.post("/Finance_Tutor/login", json={
            "email": "shiksha@ds.study.in",
            "password": "let564"
        })
        assert login_response.status_code == 200
        assert "Login is successful" in login_response.get_json()["message"]

        # 3. Logout
        logout_response = client.post("/Finance_Tutor/logout")
        assert logout_response.status_code == 200
        assert logout_response.get_json()["message"] == "Logout successful"


def test_institute_logout_success(client):

    with client:
        # 1. Sign up institute
        client.post("/Finance_Tutor/institute/signup", json={
            "name": "Bright Future Academy",
            "email": "institute@example.com",
            "password": "admin123",
            "address": "Main Road, City Center"
        })

        # 2. Login as institute
        login_response = client.post("/Finance_Tutor/login", json={
            "email": "institute@example.com",
            "password": "admin123"
        })
        assert login_response.status_code == 200
        assert "Login is Successful" in login_response.get_json()["message"]

        # 3. Logout
        logout_response = client.post("/Finance_Tutor/logout")
        assert logout_response.status_code == 200
        assert logout_response.get_json()["message"] == "Logout successful"


def test_institute_login_wrong_password(client):
    client.post("/Finance_Tutor/institute/signup", json={
        "name": "Future School",
        "email": "future@example.com",
        "password": "rightpass",
        "address": "Metro Road"
    })

    # Attempt login with wrong password
    response = client.post("/Finance_Tutor/login", json={
        "email": "future@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert "Invalid Credentials" in response.get_json()["error"]


def test_user_login_wrong_password(client):
    client.post("/Finance_Tutor/User/signup", json={
        "full_name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "correctpass",
        "parents_email": "parent@example.com",
        "dob": "2000-01-01",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "9"
    })

    # Try wrong password
    response = client.post("/Finance_Tutor/login", json={
        "email": "testuser@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert "Wrong password" in response.get_json()["error"]
