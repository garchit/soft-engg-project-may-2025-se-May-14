import pytest
from datetime import date
from models import db
from models.unit import Unit as Course
from models.user import User
from models.user_course import UserCourse


def create_user(username="progressuser", email="p@example.com"):
    """Creates and returns a test user"""
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

def create_course(title):
    """Creates and returns a test course"""
    course = Course(title=title, description=f"Desc for {title}")
    db.session.add(course)
    db.session.commit()
    return course

def validate_recommendation_response(response):
    """Common validation for recommendation API responses"""
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert "Recommended_Courses" in data
    assert isinstance(data["Recommended_Courses"], list)
    return data["Recommended_Courses"]

# ------------------------ Test Cases ------------------------

# 1. User with completed courses should get recommendations
def test_recommended_courses_with_completed_courses(client):
    user = create_user("recuser1", "rec1@example.com")
    completed = create_course("Python Basics")
    create_course("Data Science")
    create_course("Machine Learning")
    
    db.session.add(UserCourse(user_id=user.id, course_id=completed.id))
    db.session.commit()

    response = client.get(f"/Finance_Tutor/recommended_courses/{user.id}")
    validate_recommendation_response(response)

# 2. New user with no completed courses should get all courses as recommendations
def test_recommended_courses_no_completed_courses(client):
    user = create_user("recuser2", "rec2@example.com")
    create_course("Finance 101")
    create_course("Investment Basics")
    create_course("Banking Fundamentals")

    response = client.get(f"/Finance_Tutor/recommended_courses/{user.id}")
    validate_recommendation_response(response)

# 3. User who completed all courses should get an empty recommendation list
def test_recommended_courses_all_courses_completed(client):
    user = create_user("recuser3", "rec3@example.com")
    courses = [create_course(name) for name in ["Course A", "Course B", "Course C"]]

    for course in courses:
        db.session.add(UserCourse(user_id=user.id, course_id=course.id))
    db.session.commit()

    response = client.get(f"/Finance_Tutor/recommended_courses/{user.id}")
    recommended = validate_recommendation_response(response)
    assert recommended == []

# 4. Non-existent user ID should return 404 or 200 with empty list
def test_recommended_courses_nonexistent_user(client):
    create_course("Test Course")
    response = client.get("/Finance_Tutor/recommended_courses/99999")

    assert response.status_code in [200, 400, 404]
    if response.status_code == 200:
        recommended = validate_recommendation_response(response)
        assert recommended == []

# 5. Invalid user ID format (non-numeric) should raise 400/404/422
def test_recommended_courses_invalid_user_id_format(client):
    create_course("Test Course")
    response = client.get("/Finance_Tutor/recommended_courses/invalid_id")
    assert response.status_code in [400, 404, 422]

# 6. No courses in system should return an empty recommendation list
def test_recommended_courses_no_courses_available(client):
    user = create_user("recuser4", "rec4@example.com")
    response = client.get(f"/Finance_Tutor/recommended_courses/{user.id}")
    recommended = validate_recommendation_response(response)
    assert recommended == []
