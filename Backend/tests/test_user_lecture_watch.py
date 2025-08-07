from datetime import date
from models import db
from models.user import User
from models.lecture import Lecture
from models.unit import Unit as Course
from models.user_lecture import UserLecture
import pytest

###  Test cases for User Lecture Watch API ###

# creating user
def create_test_user():
    user = User(
        full_name="Test User",
        username="testuser",
        password="hashedpassword",
        email="test@example.com",
        dob=date(1990, 1, 1),
        user_type=False,
        institute_id=1
    )
    db.session.add(user)
    db.session.commit()
    return user.id

def create_test_unit():
    unit = Course(title="Unit A", description="Basic unit")
    db.session.add(unit)
    db.session.commit()
    return unit.id


# creating lecture
def create_test_lecture(unit_id):
    lecture = Lecture(
        title="Test Lecture",
        description="Test description", 
        link="https://testlink.com",
        unit_id=unit_id
    )
    db.session.add(lecture)
    db.session.commit()
    return lecture.id

# Test for Successfully watch a lecture
def test_user_lecture_watch_success(client):
    user_id = create_test_user()
    unit_id = create_test_unit()
    lecture_id = create_test_lecture(unit_id)

    response = client.post(f"/Finance_Tutor/user_lecture_watched/{user_id}/{lecture_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Succesfully Watched Lecture"

    # Verify record was created
    user_lecture = db.session.query(UserLecture).filter_by(
        user_id=user_id, lecture_id=lecture_id
    ).first()
    assert user_lecture is not None

# Test  when User doesn't exist - Current API returns 200 with no body
def test_user_does_not_exist(client):
    unit_id = create_test_unit()
    lecture_id = create_test_lecture(unit_id)

    response = client.post(f"/Finance_Tutor/user_lecture_watched/9999/{lecture_id}")
    # Your current API doesn't handle this properly - it returns 200 with None
    assert response.status_code == 200
    assert response.get_json() is None

# Test when Lecture doesn't exist - Current API returns 200 with no body
def test_lecture_does_not_exist(client):
    user_id = create_test_user()

    response = client.post(f"/Finance_Tutor/user_lecture_watched/{user_id}/9999")
    # Your current API doesn't handle this properly - it returns 200 with None
    assert response.status_code == 200
    assert response.get_json() is None

# Testcase when  Watch same lecture twice 
def test_duplicate_watch_causes_error(client):
    user_id = create_test_user()
    unit_id = create_test_unit()
    lecture_id = create_test_lecture(unit_id)

    # First watch succeeds
    response1 = client.post(f"/Finance_Tutor/user_lecture_watched/{user_id}/{lecture_id}")
    assert response1.status_code == 200
    assert response1.get_json()["message"] == "Succesfully Watched Lecture"

    # Second watch will cause database IntegrityError due to unique constraint
    with pytest.raises(Exception):  # This will catch the IntegrityError
        client.post(f"/Finance_Tutor/user_lecture_watched/{user_id}/{lecture_id}")

# Test 5: Multiple different lectures for same user
def test_multiple_lectures_same_user(client):
    user_id = create_test_user()
    unit_id = create_test_unit()
    
    # Create two lectures
    lecture1_id = create_test_lecture(unit_id)
    lecture2 = Lecture(title="Lecture 2", description="Desc 2", link="link2", unit_id=unit_id)
    db.session.add(lecture2)
    db.session.commit()
    lecture2_id = lecture2.id
    
    # Watch both lectures
    response1 = client.post(f"/Finance_Tutor/user_lecture_watched/{user_id}/{lecture1_id}")
    response2 = client.post(f"/Finance_Tutor/user_lecture_watched/{user_id}/{lecture2_id}")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.get_json()["message"] == "Succesfully Watched Lecture"
    assert response2.get_json()["message"] == "Succesfully Watched Lecture"
    
    # Verify both records exist
    count = db.session.query(UserLecture).filter(UserLecture.user_id == user_id).count()
    assert count == 2

# Test when  Multiple users watching same lecture
def test_multiple_users_same_lecture(client):
    # Create two users
    user1_id = create_test_user()
    user2 = User(
        full_name="Test User 2",
        username="testuser2",
        password="hashedpassword2",
        email="test2@example.com",
        dob=date(1991, 1, 1),
        user_type=False,
        institute_id=1
    )
    db.session.add(user2)
    db.session.commit()
    user2_id = user2.id
    
    # Create lecture
    unit_id = create_test_unit()
    lecture_id = create_test_lecture(unit_id)
    
    # Both users watch same lecture
    response1 = client.post(f"/Finance_Tutor/user_lecture_watched/{user1_id}/{lecture_id}")
    response2 = client.post(f"/Finance_Tutor/user_lecture_watched/{user2_id}/{lecture_id}")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both records exist
    count = db.session.query(UserLecture).filter(UserLecture.lecture_id == lecture_id).count()
    assert count == 2