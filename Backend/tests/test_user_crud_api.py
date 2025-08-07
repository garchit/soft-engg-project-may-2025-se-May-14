## Testacse fort user crud #####


# Test case : Create a new user
def create_test_user(client):
    response = client.post("/Finance_Tutor/User/signup", json={
        "full_name": "abhishek",
        "username": "abhi",
        "email": "abhi@example.com",
        "password": "success123",
        "parents_email": "papa@gmail.com",
        "dob": "2001-05-20",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "9"
    })
    assert response.status_code == 201

# testcase when user fetch successfully
def test_get_user_success(client):
    create_test_user(client)
    response = client.get("/Finance_Tutor/User/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "abhi"
    assert data["email"] == "abhi@example.com"

def test_get_user_not_found(client):
    response = client.get("/Finance_Tutor/User/999")
    assert response.status_code == 404
    assert "User not found" in response.get_json()["error"]

# testcase when user update successfully
def test_update_user_success(client):
    create_test_user(client)
    response = client.put("/Finance_Tutor/User/1", json={
        "full_name": "Updated bhai",
        "user_class": "12",
        "user_type": "admin"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "User updated successfully"

    # Confirm changes
    get_response = client.get("/Finance_Tutor/User/1")
    data = get_response.get_json()
    assert data["full_name"] == "Updated bhai"
    assert data["user_class"] == "12"
    assert data["user_type"] == "admin"

# testcase when user dob in wrong format
def test_update_user_invalid_dob(client):
    create_test_user(client)
    response = client.put("/Finance_Tutor/User/1", json={
        "dob": "31-12-2001"
    })
    assert response.status_code == 400
    assert "DOB must be in YYYY-MM-DD format" in response.get_json()["error"]

# testcase when user deleted successfully
def test_delete_user_success(client):
    create_test_user(client)
    response = client.delete("/Finance_Tutor/User/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "User deleted successfully"

    get_response = client.get("/Finance_Tutor/User/1")
    assert get_response.status_code == 404
    
# testcase when trying to delete user but that user not found
def test_delete_user_not_found(client):
    response = client.delete("/Finance_Tutor/User/999")
    assert response.status_code == 404
    assert "User not found" in response.get_json()["error"]
