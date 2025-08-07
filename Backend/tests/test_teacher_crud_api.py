## Testcase for Teacher Crud ####

# create Institute
def create_test_institute(client):
    response = client.post("/Finance_Tutor/institute/signup", json={
        "name": "alpha Institute",
        "email": "alpha@example.com",
        "password": "python",
        "address": "nepal"
    })
    assert response.status_code == 201


# Create Teacher
def create_test_teacher(client):
    create_test_institute(client)
    response = client.post("/Finance_Tutor/teacher", json={
        "name": "amrita",
        "password": "alphabeta",
        "institute_id": 1,
        "email": "amrita@gmail.com",
        "class_teacher": 5
    })
    assert response.status_code == 201

# Testcase when teacher fetched successfully
def test_get_teacher_success(client):
    create_test_teacher(client)
    response = client.get("/Finance_Tutor/teacher/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "amrita"
    assert data["email"] == "amrita@gmail.com"
    assert data["class_teacher"] == 5

# testcase when trying to fetched teacher but that teacher is not registred
def test_get_teacher_not_found(client):
    response = client.get("/Finance_Tutor/teacher/2")
    assert response.status_code in [401, 404] 

# testcase when teacher details updated
def test_update_teacher_success(client):
    create_test_teacher(client)
    response = client.put("/Finance_Tutor/teacher/1", json={
        "name": "abhi",
        "password": "newpass",
        "class_teacher": 10
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "Teacher Updated Successfully"

    # Confirm update
    get_resp = client.get("/Finance_Tutor/teacher/1")
    data = get_resp.get_json()
    assert data["name"] == "abhi"
    assert data["class_teacher"] == 10

# testcase when teacher is updated with invalid class
def test_update_teacher_invalid_class(client):
    create_test_teacher(client)
    response = client.put("/Finance_Tutor/teacher/1", json={
        "name": "Teacher",
        "password": "pass",
        "class_teacher": 15   
    })
    assert response.status_code == 400
    assert "Invalind Class" in response.get_json()["error"]

# testcase when teacher deleted successfully
def test_delete_teacher_success(client):
    create_test_teacher(client)
    response = client.delete("/Finance_Tutor/teacher/1")
    assert response.status_code == 200
    assert "Teacher is Successfully Removed" in response.get_json()["message"]

    # Verify deletion
    get_response = client.get("/Finance_Tutor/teacher/1")
    assert get_response.status_code in [401, 404]

# testcase when trying to delete teacher but that teacher not found
def test_delete_teacher_not_found(client):
    response = client.delete("/Finance_Tutor/teacher/10")
    assert response.status_code == 401
    assert "no such teacher" in response.get_json()["error"].lower()

# testcase when teacher created successfully
def test_create_teacher_success(client):
    create_test_institute(client)
    response = client.post("/Finance_Tutor/teacher", json={
        "name": "abhay",
        "password": "pkworf",
        "institute_id": 1,
        "email": "abhay@example.com",
        "class_teacher": 4
    })
    assert response.status_code == 201
    assert "Teacher Added Successfully" in response.get_json()["message"]

# testcase when teacher created with misssing fields
def test_create_teacher_missing_fields(client):
    create_test_institute(client)
    response = client.post("/Finance_Tutor/teacher", json={
        "name": "naman",
        "password": "",
        "institute_id": 1,
        "email": "naman@example.com",
        "class_teacher": 6
    })
    assert response.status_code == 401
    assert "Required Field is Missing" in response.get_json()["error"]



