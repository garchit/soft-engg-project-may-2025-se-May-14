import pytest
import json
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from sqlalchemy.exc import SQLAlchemyError


# Testcase for student link with teacher and teacher wise prgress

def create_test_institute(client):
    response = client.post("/Finance_Tutor/institute/signup", json={
        "name": "alpha Institute",
        "email": "alpha@example.com",
        "password": "python",
        "address": "nepal"
    })
    assert response.status_code == 201
    return 1  # Assuming ID is 1

def create_test_teacher(client, class_teacher=5, institute_id=1):
    response = client.post("/Finance_Tutor/teacher", json={
        "name": "amrita",
        "password": "alphabeta",
        "institute_id": institute_id,
        "email": "amrita@gmail.com",
        "class_teacher": class_teacher
    })
    assert response.status_code == 201
    return response.get_json().get("id", 1)

def create_test_user(client, user_class="5", institute_id=1):
    response = client.post("/Finance_Tutor/User/signup", json={
        "full_name": "John Doe",
        "username": "johndoe123",
        "email": "john@example.com",
        "password": "secure123",
        "parents_email": "parent@example.com",
        "dob": "2000-01-01",
        "user_type": "student",
        "institute_id": institute_id,
        "user_class": user_class
    })
    assert response.status_code == 201
    return response.get_json().get("id", 1)

def create_test_course(client):
    response = client.post("/Finance_Tutor/course", json={
        "title": "Finance Course",
        "description": "Basic finance concepts",
        "duration": "30 days"
    })
    assert response.status_code in [200, 201]
    return response.get_json().get("id", 1)

# Test Cases

# Link user to teacher successfully
def test_link_user_to_teacher_success(client):
    institute_id = create_test_institute(client)
    create_test_teacher(client, class_teacher=5, institute_id=institute_id)
    user_id = create_test_user(client, user_class="5", institute_id=institute_id)

    response = client.post(f"/Finance_Tutor/user_teacher/{user_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Linked student to teacher"

# Link fails: user does not exist
def test_link_user_not_found(client):
    response = client.post("/Finance_Tutor/user_teacher/999")
    assert response.status_code == 404
    assert "No such user" in response.get_json()["error"]

# Link fails user already assigned to a teacher
def test_user_already_assigned_to_teacher(client):
    institute_id = create_test_institute(client)
    create_test_teacher(client, class_teacher=5, institute_id=institute_id)
    user_id = create_test_user(client, user_class="5", institute_id=institute_id)

    client.post(f"/Finance_Tutor/user_teacher/{user_id}")
    response = client.post(f"/Finance_Tutor/user_teacher/{user_id}")

    assert response.status_code == 401
    assert "User is already assigned to a teacher" in response.get_json()["error"]

# Link fails no teacher for user’s class
def test_link_user_no_teacher_for_class(client):
    institute_id = create_test_institute(client)
    create_test_teacher(client, class_teacher=5, institute_id=institute_id)
    user_id = create_test_user(client, user_class="10", institute_id=institute_id)

    response = client.post(f"/Finance_Tutor/user_teacher/{user_id}")

    assert response.status_code == 401
    assert "There is no teacher assigned to this class" in response.get_json()["error"]

# Get teacher-wise progress: success
def test_teacher_progress_success(client):
    institute_id = create_test_institute(client)
    create_test_course(client)
    create_test_teacher(client, class_teacher=5, institute_id=institute_id)
    user_id = create_test_user(client, user_class="5", institute_id=institute_id)
    client.post(f"/Finance_Tutor/user_teacher/{user_id}")

    response = client.get(f"/Finance_Tutor/teacher_wise_progress/{institute_id}")
    assert response.status_code == 200
    assert isinstance(response.get_json()["teacher_progress"], list)

# Get teacher-wise progress: teacher with no students
def test_teacher_progress_no_students(client):
    institute_id = create_test_institute(client)
    create_test_teacher(client, class_teacher=5, institute_id=institute_id)

    response = client.get(f"/Finance_Tutor/teacher_wise_progress/{institute_id}")
    assert response.status_code == 200
    assert isinstance(response.get_json()["teacher_progress"], list)

# Get teacher-wise progress no teachers in institute
def test_teacher_progress_no_teachers(client):
    institute_id = create_test_institute(client)

    response = client.get(f"/Finance_Tutor/teacher_wise_progress/{institute_id}")
    assert response.status_code == 200
    assert isinstance(response.get_json()["teacher_progress"], list)

# Get teacher-wise progress invalid institute ID format
def test_teacher_progress_invalid_institute_id_format(client):
    response = client.get("/Finance_Tutor/teacher_wise_progress/invalid")
    assert response.status_code == 404  
