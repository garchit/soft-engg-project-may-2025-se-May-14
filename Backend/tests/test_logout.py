### Testcases for user and institute logout


# testcase when Successful logout after User login
def test_user_logout_success(client):
    with client:
        # Register user
        client.post("/Finance_Tutor/User/signup", json={
            "full_name": "Amit Kumar",
            "username": "a123",
            "email": "amit@ds.study.in",
            "password": "user ka pass",
            "parents_email": "parent@example.com",
            "dob": "2002-05-01",
            "user_type": "student",
            "institute_id": 1,
            "user_class": "10"
        })

        # Login
        login_response = client.post("/Finance_Tutor/login", json={
            "email": "amit@ds.study.in",
            "password": "user ka pass"
        })
        assert login_response.status_code == 200
        assert "Login is successful" in login_response.get_json()["message"]

        # Logout
        logout_response = client.post("/Finance_Tutor/logout")
        assert logout_response.status_code == 200
        assert logout_response.get_json()["message"] == "Logout successful"


# testcase when Successful logout after Institute login
def test_institute_logout_success(client):
    with client:
        # Register institute
        client.post("/Finance_Tutor/institute/signup", json={
            "name": "Bright Minds School",
            "email": "admin@brightminds.com",
            "password": "adminpass",
            "address": "Knowledge Street"
        })

        # Login
        login_response = client.post("/Finance_Tutor/login", json={
            "email": "admin@brightminds.com",
            "password": "adminpass"
        })
        assert login_response.status_code == 200
        assert "Login is Successful" in login_response.get_json()["message"]

        # Logout
        logout_response = client.post("/Finance_Tutor/logout")
        assert logout_response.status_code == 200
        assert logout_response.get_json()["message"] == "Logout successful"


# testcase when Register and Logout different user
def test_another_user_logout_success(client):
    with client:
        # Register new user
        client.post("/Finance_Tutor/User/signup", json={
            "full_name": "Aarav Singh",
            "username": "aarav_singh",
            "email": "aarav@example.com",
            "password": "password123",
            "parents_email": "parent@home.com",
            "dob": "2005-07-15",
            "user_type": "student",
            "institute_id": 1,
            "user_class": "8"
        })

        # Login
        login_response = client.post("/Finance_Tutor/login", json={
            "email": "aarav@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        assert "Login is successful" in login_response.get_json()["message"]

        # Logout
        logout_response = client.post("/Finance_Tutor/logout")
        assert logout_response.status_code == 200
        assert logout_response.get_json()["message"] == "Logout successful"


# testcase when Logout after re-login with another account
def test_logout_after_switching_users(client):
    with client:
        # Register two users
        client.post("/Finance_Tutor/User/signup", json={
            "full_name": "User One",
            "username": "userone",
            "email": "userone@example.com",
            "password": "passone",
            "parents_email": "parent@one.com",
            "dob": "2001-02-01",
            "user_type": "student",
            "institute_id": 1,
            "user_class": "11"
        })

        client.post("/Finance_Tutor/User/signup", json={
            "full_name": "User Two",
            "username": "usertwo",
            "email": "usertwo@example.com",
            "password": "passtwo",
            "parents_email": "parent@two.com",
            "dob": "2002-03-02",
            "user_type": "student",
            "institute_id": 1,
            "user_class": "12"
        })

        # Login as User One
        client.post("/Finance_Tutor/login", json={
            "email": "userone@example.com",
            "password": "passone"
        })

        client.post("/Finance_Tutor/logout")  # Logout User One

        # Login as User Two
        login_response = client.post("/Finance_Tutor/login", json={
            "email": "usertwo@example.com",
            "password": "passtwo"
        })
        assert login_response.status_code == 200
        assert "Login is successful" in login_response.get_json()["message"]

        # Logout User Two
        logout_response = client.post("/Finance_Tutor/logout")
        assert logout_response.status_code == 200
        assert logout_response.get_json()["message"] == "Logout successful"
