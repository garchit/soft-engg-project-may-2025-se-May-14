def create_test_institute(client):
    response = client.post("/Finance_Tutor/institute/signup", json={
        "name": "ABC Institute",
        "email": "abc@example.com",
        "password": "just a pass",
        "address": "123 Main Street"
    })
    assert response.status_code == 201


def test_get_institute_success(client):
    create_test_institute(client)
    response = client.get("/Finance_Tutor/institute/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["Name"] == "ABC Institute"
    assert data["email"] == "abc@example.com"

def test_get_institute_not_found(client):
    response = client.get("/Finance_Tutor/institute/10")
    assert response.status_code == 404
    assert "No such User" in response.get_json()["error"]


def test_update_institute_success(client):
    create_test_institute(client)
    response = client.put("/Finance_Tutor/institute/1", json={
        "name": "new Institute",
        "address": "456 New Address"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "Successfully Updated"

    response = client.get("/Finance_Tutor/institute/1")
    data = response.get_json()
    assert data["Name"] == "new Institute"
    assert data["Address"] == "456 New Address"

def test_update_institute_invalid_name(client):
    create_test_institute(client)
    response = client.put("/Finance_Tutor/institute/1", json={
        "name": "", 
        "address": "456 Another Address"
    })
    assert response.status_code == 400
    assert "bad Request" in response.get_json()["error"]

def test_delete_institute_success(client):
    create_test_institute(client)
    response = client.delete("/Finance_Tutor/institute/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Deleted Succesfully"

    # Confirm deletion
    response = client.get("/Finance_Tutor/institute/1")
    assert response.status_code == 404

def test_delete_institute_not_found(client):
    response = client.delete("/Finance_Tutor/institute/6")
    assert response.status_code == 404
    assert "No such Institute" in response.get_json()["error"]
