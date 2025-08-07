### Test Cases for User Signup API ###

def test_user_not_found(client):
    """Test GET request for non-existent user"""
    response = client.get('/Finance_Tutor/User/999')
    assert response.status_code == 404
    assert response.get_json()['error'] == "User not found"

def test_create_user(client):
    """Test successful user signup"""
    payload = {
        "full_name": "John Doe",
        "username": "johndoe123",
        "email": "john@example.com",
        "password": "secure123",
        "parents_email": "parent@example.com",
        "dob": "2000-01-01",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "10"
    }
    response = client.post("/Finance_Tutor/User/signup", json=payload)
    assert response.status_code == 201
    assert response.get_json()["message"] == "User created successfully"

def test_duplicate_email(client):
    """Test signup with duplicate email"""
    payload = {
        "full_name": "Alice",
        "username": "alice123",
        "email": "john@example.com",
        "password": "pass123",
        "parents_email": "parent@example.com",
        "dob": "2001-01-01",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "9"
    }
    client.post("/Finance_Tutor/User/signup", json=payload)
    payload["username"] = "anotheruser"
    response = client.post("/Finance_Tutor/User/signup", json=payload)
    assert response.status_code == 400
    assert "Email is already in use" in response.get_json()["error"]

def test_duplicate_username(client):
    """Test signup with duplicate username"""
    payload = {
        "full_name": "Bob",
        "username": "bob123",
        "email": "bob@example.com",
        "password": "pass123",
        "parents_email": "parent@example.com",
        "dob": "2002-02-02",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "8"
    }
    client.post("/Finance_Tutor/User/signup", json=payload)
    payload["email"] = "bob2@example.com"
    response = client.post("/Finance_Tutor/User/signup", json=payload)
    assert response.status_code == 400
    assert "Username is already taken" in response.get_json()["error"]

def test_invalid_dob_format(client):
    """Test signup with incorrect date format"""
    payload = {
        "full_name": "Charlie",
        "username": "charlie123",
        "email": "charlie@example.com",
        "password": "pass123",
        "parents_email": "parent@example.com",
        "dob": "01-02-2002",  # Invalid format
        "user_type": "student",
        "institute_id": 1,
        "user_class": "10"
    }
    response = client.post("/Finance_Tutor/User/signup", json=payload)
    assert response.status_code == 400
    assert "DOB must be in YYYY-MM-DD format" in response.get_json()["error"]

def test_invalid_user_type(client):
    """Test signup with invalid user type"""
    payload = {
        "full_name": "Daisy",
        "username": "daisy123",
        "email": "daisy@example.com",
        "password": "pass123",
        "parents_email": "parent@example.com",
        "dob": "2000-05-05",
        "user_type": "teacher",  # Invalid user type
        "institute_id": 1,
        "user_class": "10"
    }
    response = client.post("/Finance_Tutor/User/signup", json=payload)
    assert response.status_code == 400
    assert "Invalid user_type" in response.get_json()["error"]


### Test Cases for Leaderboard and User Rank APIs ###

def create_test_user(client, username="abhi", email="abhi@example.com"):
    """Helper function to create a test user"""
    response = client.post("/Finance_Tutor/User/signup", json={
        "full_name": "Test User",
        "username": username,
        "email": email,
        "password": "success123",
        "parents_email": "parent@gmail.com",
        "dob": "2001-05-20",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "9"
    })
    assert response.status_code == 201

def test_get_leaderboard_success(client):
    """Test successful leaderboard retrieval with multiple users"""
    create_test_user(client, "student1", "student1@example.com")
    create_test_user(client, "student2", "student2@example.com")
    
    response = client.get("/Finance_Tutor/user_leaderboard")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Successfully fetched leaderboard."
    assert "leaderboard" in data
    assert isinstance(data["leaderboard"], list)

def test_get_leaderboard_no_students(client):
    """Test leaderboard when no students exist"""
    response = client.get("/Finance_Tutor/user_leaderboard")
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "No students found."

def test_leaderboard_structure(client):
    """Test leaderboard response structure"""
    create_test_user(client)
    response = client.get("/Finance_Tutor/user_leaderboard")
    assert response.status_code == 200
    data = response.get_json()
    
    if data["leaderboard"]:
        student = data["leaderboard"][0]
        required_fields = ["rank", "id", "username", "rewards", "streak", "picture"]
        for field in required_fields:
            assert field in student
        assert student["rank"] == 1

def test_get_user_rank_success(client):
    """Test successful user rank retrieval"""
    create_test_user(client)
    response = client.get("/Finance_Tutor/user_rank/abhi")
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "abhi"
    required_fields = ["id", "username", "rewards", "rank", "streak", "points_to_next_rank"]
    for field in required_fields:
        assert field in data

def test_get_user_rank_case_insensitive(client):
    """Test user rank with case insensitive username"""
    create_test_user(client)
    response = client.get("/Finance_Tutor/user_rank/ABHI")
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "abhi"

def test_get_user_rank_not_found(client):
    """Test user rank for non-existent user"""
    response = client.get("/Finance_Tutor/user_rank/nonexistent")
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "User 'nonexistent' not found."

def test_multiple_users_ranking_order(client):
    """Test correct ranking order with multiple users"""
    create_test_user(client, "topstudent", "top@example.com")
    create_test_user(client, "secondstudent", "second@example.com")
    
    response = client.get("/Finance_Tutor/user_leaderboard")
    assert response.status_code == 200
    data = response.get_json()
    
    # Verify ranks are assigned sequentially
    leaderboard = data["leaderboard"]
    for i, student in enumerate(leaderboard):
        assert student["rank"] == i + 1

def test_points_to_next_rank_calculation(client):
    """Test points to next rank calculation"""
    create_test_user(client, "abhi", "abhi@example.com")
    create_test_user(client, "betterstudent", "better@example.com")
    
    response = client.get("/Finance_Tutor/user_rank/abhi")
    assert response.status_code == 200
    data = response.get_json()
    
    # Points to next rank should be >= 0
    assert data["points_to_next_rank"] >= 0


## user streak and user Calendar
import pytest
from datetime import date, timedelta, datetime
from models.user import User
from models.streaklog import StreakLog
from models import db
import pytz

def create_streak_user(client, username="streaker", email="streaker@example.com"):
    payload = {
        "full_name": "Streak User",
        "username": username,
        "email": email,
        "password": "pass123",
        "parents_email": "parent@example.com",
        "dob": "2001-01-01",
        "user_type": "student",
        "institute_id": 1,
        "user_class": "9"
    }
    resp = client.post("/Finance_Tutor/User/signup", json=payload)
    assert resp.status_code == 201
    # fetch created user from DB
    user = User.query.filter_by(username=username).first()
    assert user is not None
    return user

def test_streak_checkin_success(client, test_app):
    """First-time streak checkin should succeed and set streak=1"""
    with test_app.app_context():
        user = create_streak_user(client, "user1", "user1@example.com")

        response = client.post("/Finance_Tutor/user/streak", json={"user_id": user.id})
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Check-in successful!"
        assert data["streak"] == 1
        assert data["user_id"] == user.id
        assert data["latest_timestamp"] is not None

        # Verify log created
        log = StreakLog.query.filter_by(user_id=user.id, checkin_date=date.today()).first()
        assert log is not None

def test_streak_checkin_repeat_same_day(client, test_app):
    """Repeat check-in same day shouldn't increase streak"""
    with test_app.app_context():
        user = create_streak_user(client, "user2", "user2@example.com")

        resp1 = client.post("/Finance_Tutor/user/streak", json={"user_id": user.id})
        assert resp1.status_code == 200
        data1 = resp1.get_json()
        assert data1["streak"] == 1

        resp2 = client.post("/Finance_Tutor/user/streak", json={"user_id": user.id})
        assert resp2.status_code == 200
        data2 = resp2.get_json()
        assert data2["message"] == "Already checked in today."
        assert data2["streak"] == 1

def test_streak_calendar_returns_checkin_and_streak(client, test_app):
    """Calendar endpoint should reflect existing check-in and streak"""
    with test_app.app_context():
        user = create_streak_user(client, "user3", "user3@example.com")

        client.post("/Finance_Tutor/user/streak", json={"user_id": user.id})
        resp = client.get("/Finance_Tutor/user/streak/calendar", query_string={"user_id": user.id})
        assert resp.status_code == 200
        data = resp.get_json()
        today_iso = date.today().isoformat()
        assert today_iso in data["checkins"]
        assert data["streak"] == 1

def test_streak_continuation_across_days(client, test_app):
    """If user checked in yesterday, streak increments"""
    with test_app.app_context():
        user = create_streak_user(client, "user4", "user4@example.com")
        # Manually insert yesterday's log and set streak=1
        yesterday = date.today() - timedelta(days=1)
        user.streak = 1
        user.streak_start_timestamp = datetime.utcnow() - timedelta(days=1)
        user.latest_timestamp = datetime.utcnow() - timedelta(days=1)
        db.session.add(StreakLog(user_id=user.id, checkin_date=yesterday))
        db.session.commit()

        resp = client.post("/Finance_Tutor/user/streak", json={"user_id": user.id})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["streak"] == 2  # streak continued

def test_streak_no_user_id_and_not_authenticated(client, test_app):
    """Without user_id fallback and no login, should get 401"""
    response = client.post("/Finance_Tutor/user/streak", json={})
    assert response.status_code == 401
    data = response.get_json()
    assert "Authentication required" in data.get("message", "") or "provide user_id" in data.get("message", "")

def test_calendar_no_user_id_and_not_authenticated(client):
    """Calendar without user context should fail"""
    response = client.get("/Finance_Tutor/user/streak/calendar")
    assert response.status_code == 401
    data = response.get_json()
    assert "Authentication required" in data.get("message", "") or "provide user_id" in data.get("message", "")
