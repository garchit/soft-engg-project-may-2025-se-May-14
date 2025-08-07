import json
import pytest
from datetime import date
from models import db
from models.unit import Unit as Course
from models.user import User
from models.user_course import UserCourse

# Helper function to create a user
def create_user(username="progressuser", email="p@example.com"):
    user = User(
        full_name="Test User",
        username=username,
        password="pass123",
        email=email,
        dob=date(1990, 1, 1),
        user_type=True,
        institute_id=1
    )
    db.session.add(user)
    db.session.commit()
    return user

# Helper function to create a course
def create_course(title):
    course = Course(title=title, description=f"Desc for {title}")
    db.session.add(course)
    db.session.commit()
    return course

# ---------------------------- Course CRUD Tests ----------------------------

# Test case for creating a course
def test_create_course(client):
    response = client.post("/Finance_Tutor/course", json={
        "title": "Introduction to Finance",
        "description": "A beginner course on financial literacy."
    })
    assert response.status_code == 201
    assert response.json['message'] == "Course added Succesfully"

# Test case for creating a course with a duplicate title
def test_create_duplicate_course(client):
    course = Course(title="Finance 101", description="Basics")
    db.session.add(course)
    db.session.commit()

    response = client.post("/Finance_Tutor/course", json={
        "title": "Finance 101",
        "description": "New desc"
    })
    assert response.status_code == 400
    assert "Title Already Exist" in response.json['error']

# Test case for fetching all courses
def test_get_all_courses(client):
    db.session.add(Course(title="A", description="A Desc"))
    db.session.add(Course(title="B", description="B Desc"))
    db.session.commit()

    response = client.get("/Finance_Tutor/course")
    assert response.status_code == 200
    assert "course_detail" in response.json
    assert len(response.json["course_detail"]) == 2

# Test case for updating course details
def test_update_course(client):
    course = Course(title="Old", description="Old Desc")
    db.session.add(course)
    db.session.commit()

    response = client.put(f"/Finance_Tutor/course/{course.id}", json={
        "title": "New Title",
        "description": "New Description"
    })
    assert response.status_code == 200
    assert response.json['title'] == "New Title"

# Test case for deleting a course
def test_delete_course(client):
    course = Course(title="ToDelete", description="Delete Me")
    db.session.add(course)
    db.session.commit()

    response = client.delete(f"/Finance_Tutor/course/{course.id}")
    assert response.status_code == 200
    assert response.json["message"] == "Course Deleted Successfully"

# ---------------------- User Course Completion Tests ----------------------

# Test case for successful course completion marking
def test_mark_course_completed_success(client):
    user = create_user("testuser", "test@example.com")
    course = create_course("Test Course")

    response = client.post(f"/Finance_Tutor/user_course_completed/{user.id}", json={
        "course_id": course.id
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == "Successfully added"

# Test case for missing course_id in request
def test_mark_course_completed_missing_course_id(client):
    user = create_user("testuser2", "test2@example.com")

    response = client.post(f"/Finance_Tutor/user_course_completed/{user.id}", json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == "Missing course_id"

# Test case for invalid user ID
def test_mark_course_completed_invalid_user(client):
    course = create_course("Test Course")

    response = client.post("/Finance_Tutor/user_course_completed/9999", json={
        "course_id": course.id
    })
    assert response.status_code == 404
    assert response.get_json()['error'] == "No such user"

# Test case for invalid course ID
def test_mark_course_completed_invalid_course(client):
    user = create_user("testuser3", "test3@example.com")

    response = client.post(f"/Finance_Tutor/user_course_completed/{user.id}", json={
        "course_id": 9999
    })
    assert response.status_code == 404
    assert response.get_json()['error'] == "No such course exists"

# Test case for duplicate course completion
def test_mark_course_completed_duplicate_entry(client):
    user = create_user("testuser4", "test4@example.com")
    course = create_course("Test Course")

    db.session.add(UserCourse(user_id=user.id, course_id=course.id))
    db.session.commit()

    response = client.post(f"/Finance_Tutor/user_course_completed/{user.id}", json={
        "course_id": course.id
    })
    assert response.status_code == 409
    assert response.get_json()['error'] == "Course already marked as completed by user"

# Test case for null course_id
def test_mark_course_completed_null_course_id(client):
    user = create_user("testuser5", "test5@example.com")

    response = client.post(f"/Finance_Tutor/user_course_completed/{user.id}", json={
        "course_id": None
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == "Missing course_id"

# Test case for invalid JSON payload
def test_mark_course_completed_invalid_json(client):
    user = create_user("testuser6", "test6@example.com")

    response = client.post(f"/Finance_Tutor/user_course_completed/{user.id}", 
                           data="invalid json", content_type='application/json')
    assert response.status_code == 400

# Test case for string value as course_id
def test_mark_course_completed_string_course_id(client):
    user = create_user("testuser7", "test7@example.com")

    response = client.post(f"/Finance_Tutor/user_course_completed/{user.id}", json={
        "course_id": "invalid_id"
    })
    assert response.status_code == 404
    assert response.get_json()['error'] == "No such course exists"

# ------------------------ Course Progress API Tests ------------------------

# Test case for progress API with non-existing user
def test_course_progress_user_not_found(client):
    response = client.get("/Finance_Tutor/course_progress/99999")
    assert response.status_code == 404
    assert response.json == {"error": "No such user"}

# Test case for user with no courses
def test_course_progress_no_courses(client):
    user = create_user("user1", "user1@example.com")

    response = client.get(f"/Finance_Tutor/course_progress/{user.id}")
    assert response.status_code == 200
    assert response.json == {
        "course_progress": [],
        "overall_progress": 0.0
    }

# Test case for user with courses but none completed
def test_course_progress_uncompleted_courses(client):
    user = create_user("user2", "user2@example.com")
    create_course("Finance A")
    create_course("Finance B")

    response = client.get(f"/Finance_Tutor/course_progress/{user.id}")
    assert response.status_code == 200
    data = response.get_json()

    assert len(data["course_progress"]) == 2
    assert all(progress == 0.0 for course in data["course_progress"] for progress in course.values())
    assert data["overall_progress"] == 0.0
