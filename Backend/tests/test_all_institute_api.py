import pytest
def create_test_institute(client, name, email):
    response = client.post("/Finance_Tutor/institute/signup", json={
        "name": name,
        "email": email,
        "password": "pass123",
        "address": "Sample Address"
    })
    assert response.status_code == 201

def test_get_all_institutes_with_data(client):
    create_test_institute(client, "CR International School", "xyz@cr.study.in")
    create_test_institute(client, "Green Valley High School", "contact@greenvalley.edu")
    create_test_institute(client, "XYZ School", "abc123@gmail.com")
    create_test_institute(client, "Green new Valley High School", "contact122222@greenvalley.edu")

    response = client.get("/Finance_Tutor/all_institute")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 4  

    emails = [inst["email"] for inst in data if "email" in inst]
    assert "xyz@cr.study.in" in emails
    assert "abc123@gmail.com" in emails

def test_get_all_institutes_empty(client):
    response = client.get("/Finance_Tutor/all_institute")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) == 0

def test_institute_with_no_students(client):
    create_test_institute(client, "new School", "new@school.com")

    response = client.get("/Finance_Tutor/all_institute")
    assert response.status_code == 200
    data = response.get_json()

    assert any(
        inst["name"] == "new School" and inst["total_students"] == 0 for inst in data if "name" in inst
    )
