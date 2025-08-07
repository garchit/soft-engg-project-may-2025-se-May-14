## Testcases for Verify students ##
import uuid
from datetime import date

from flask import json
from models import db
from models.user import User
from models.teacher import Teacher

def create_test_institute(client):
    response = client.post("/Finance_Tutor/institute/signup", json={
        "name": "Test Institute",
        "email": "test@example.com",
        "password": "test_password",
        "address": "123 Test Street"
    })
    assert response.status_code == 201
    return 1  # Adjust if your API returns ID in the response


def create_test_teacher_data(institute_id, class_teacher_num=10):
    """Insert a test teacher directly into the database."""
    teacher = Teacher(
        name="Test Teacher",
        email=f"teacher_{uuid.uuid4().hex[:8]}@example.com",
        password="hashed_password_here",
        institute_id=institute_id,
        class_teacher=class_teacher_num
    )
    db.session.add(teacher)
    db.session.commit()
    return teacher.id


def create_unverified_student_data(institute_id, user_class="10", class_teacher_num=10):
    student = User(
        full_name="Test Student",
        username=f"student_{uuid.uuid4().hex[:8]}",
        email=f"student_{uuid.uuid4().hex[:8]}@example.com",
        password="hashed_password_here",
        dob=date(2005, 1, 15),
        user_type=False,
        institute_id=institute_id,
        user_class=user_class,
        verified=0
    )
    db.session.add(student)
    db.session.commit()
    return student.id


# Test Cases

def test_get_unverified_students_success(client):
    institute_id = create_test_institute(client)
    create_unverified_student_data(institute_id)

    response = client.get(f"/Finance_Tutor/unverified_students/{institute_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Successfully fetched unverified students."
    assert len(data["students"]) == 1
    assert data["students"][0]["name"] == "Test Student"
    assert data["students"][0]["class"] == "10"


def test_get_unverified_students_institute_not_found(client):
    response = client.get("/Finance_Tutor/unverified_students/19")
    assert response.status_code == 404

    data = response.get_json()
    assert "Institution with id 19 does not exist" in data["message"]
    assert data["students"] == []


def test_get_unverified_students_empty_list(client):
    institute_id = create_test_institute(client)

    response = client.get(f"/Finance_Tutor/unverified_students/{institute_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Successfully fetched unverified students."
    assert len(data["students"]) == 0


def test_verify_student_success(client):
    institute_id = create_test_institute(client)
    create_test_teacher_data(institute_id, 10)
    student_id = create_unverified_student_data(institute_id, "10", 10)

    response = client.put(f"/Finance_Tutor/verify_student/{student_id}", json={"verified": 1})
    assert response.status_code == 200

    data = response.get_json()
    assert f"User {student_id} has been successfully verified" in data["message"]


def test_verify_student_invalid_verified_value(client):
    institute_id = create_test_institute(client)
    student_id = create_unverified_student_data(institute_id)

    response = client.put(f"/Finance_Tutor/verify_student/{student_id}", json={"verified": 2})
    assert response.status_code == 400

    data = response.get_json()
    assert "Invalid value for 'verified'. Must be 1 (verify) or -1 (reject)" in data["message"]


def test_verify_student_not_found(client):
    response = client.put("/Finance_Tutor/verify_student/999", json={"verified": 1})
    assert response.status_code == 404

    data = response.get_json()
    assert "User with id 999 not found" in data["message"]


def test_verify_student_missing_verified_field(client):
    institute_id = create_test_institute(client)
    student_id = create_unverified_student_data(institute_id)

    response = client.put(f"/Finance_Tutor/verify_student/{student_id}", json={"some_other_field": "value"})
    assert response.status_code == 400

    data = response.get_json()
    assert "Missing 'verified' field in request body" in data["message"]


def test_verify_student_no_teacher_found(client):
    institute_id = create_test_institute(client)
    student_id = create_unverified_student_data(institute_id, "12B", 12)  # No teacher for 12

    response = client.put(f"/Finance_Tutor/verify_student/{student_id}", json={"verified": 1})
    assert response.status_code == 404

    data = response.get_json()
    assert "No teacher found for the given class and institute" in data["message"]


def test_reject_student_success(client):
    institute_id = create_test_institute(client)
    create_test_teacher_data(institute_id, 10)
    student_id = create_unverified_student_data(institute_id, "10", 10)

    response = client.put(f"/Finance_Tutor/verify_student/{student_id}", json={"verified": -1})
    assert response.status_code == 200

    data = response.get_json()
    assert f"User {student_id} has been successfully rejected" in data["message"]
