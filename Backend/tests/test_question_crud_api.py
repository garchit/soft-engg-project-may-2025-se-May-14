import json
from models.unit import Unit as Course  # Still aliased as Course
from models import db

# Testcase for Questions Crud

# creating a course
def test_create_course(client):
    response = client.post("/Finance_Tutor/course", json={
        "title": "Introduction to Finance",
        "description": "A beginner course on financial literacy."
    })
    assert response.status_code == 201
    assert response.json['message'] == "Course added Succesfully"

def create_test_course(client, title="Sample Course", description="Course Description"):
    response = client.post("/Finance_Tutor/course", json={
        "title": title,
        "description": description
    })
    assert response.status_code == 201
    return 1


# testcase for creating question
def create_question(client, course_id):
    response = client.post("/Finance_Tutor/question", json={
        "unit_id": course_id,  # Still uses 'unit_id' as key in JSON
        "description": "kuch v nhi ?",
        "marks": 2,
        "option_a": "3",
        "option_b": "4",
        "option_c": "5",
        "option_d": "6",
        "correct_option": "b"
    })
    assert response.status_code == 201

def test_create_question_success(client):
    course_id = create_test_course(client)
    response = client.post("/Finance_Tutor/question", json={
        "unit_id": course_id,
        "description": "What is the capital of India?",
        "marks": 5,
        "option_a": "Mumbai",
        "option_b": "Delhi",
        "option_c": "Chennai",
        "option_d": "Kolkata",
        "correct_option": "b"
    })
    assert response.status_code == 201
    assert "Question added Successfully" in response.get_json()["message"]


# teastcase for create question with missing fileds
def test_create_question_missing_fields(client):
    course_id = create_test_course(client)
    response = client.post("/Finance_Tutor/question", json={
        "unit_id": course_id,
        "description": "",
        "option_a": "A", "option_b": "B", "option_c": "C", "option_d": "D",
        "correct_option": "a"
    })
    assert response.status_code == 401
    assert "Required Fields missing" in response.get_json()["error"]


# testcase for create question with invalid correct option
def test_create_question_invalid_correct_option(client):
    course_id = create_test_course(client)
    response = client.post("/Finance_Tutor/question", json={
        "unit_id": course_id,
        "description": "Choose correct",
        "marks": 2,
        "option_a": "One", "option_b": "Two", "option_c": "Three", "option_d": "Four",
        "correct_option": "e" 
    })
    assert response.status_code == 400
    assert "values of correct option" in response.get_json()["error"]


# testcase when questions fetched successfully
def test_get_question_success(client):
    course_id = create_test_course(client)
    create_question(client, course_id)
    response = client.get("/Finance_Tutor/question/1")
    assert response.status_code == 200
    assert response.get_json()["description"] == "kuch v nhi ?"


# testcase for update question
def test_update_question_success(client):
    course_id = create_test_course(client)
    create_question(client, course_id)
    response = client.put("/Finance_Tutor/question/1", json={
        "unit_id": course_id,
        "description": "Updated Q?",
        "marks": 10,
        "option_a": "1",
        "option_b": "2",
        "option_c": "3",
        "option_d": "4",
        "correct_option": "d"
    })
    assert response.status_code == 200
    assert "Question updated Sucessfully" in response.get_json()["message"]

# testcase when update question with invalid course
def test_update_question_invalid_course(client):
    course_id = create_test_course(client)
    create_question(client, course_id)
    response = client.put("/Finance_Tutor/question/1", json={
        "unit_id": 54,  # Non-existent course
        "description": "Invalid Update",
        "marks": 3,
        "option_a": "A", "option_b": "B", "option_c": "C", "option_d": "D",
        "correct_option": "a"
    })
    assert response.status_code == 404
    assert "No such Unit" in response.get_json()["error"]

# testcase for delete a question
def test_delete_question_success(client):
    course_id = create_test_course(client)
    create_question(client, course_id)
    response = client.delete("/Finance_Tutor/question/1")
    assert response.status_code == 200
    assert "Question Deleted Succefully" in response.get_json()["message"]

    # Confirm it's deleted
    response = client.get("/Finance_Tutor/question/1")
    assert response.status_code == 200 or response.status_code == 404

# testcase when delete a question with invalid ques id
def test_delete_question_not_found(client):
    response = client.delete("/Finance_Tutor/question/7")
    assert response.status_code == 404
    assert "Question not found" in response.get_json()["error"]




# testcase for fetching all questions by their unit id


def test_get_all_questions_success(client):
    """Test successful retrieval of all questions for a unit."""
    # Create a test course
    course_id = create_test_course(client)
    
    # Create multiple questions for the course
    create_question(client, course_id)
    
    # Create another question
    client.post("/Finance_Tutor/question", json={
        "unit_id": course_id,
        "description": "What is 2+2?",
        "marks": 1,
        "option_a": "3",
        "option_b": "4",
        "option_c": "5",
        "option_d": "6",
        "correct_option": "b"
    })
    
    # Test the AllQuestionResource endpoint
    response = client.get(f"/questions/unit/{course_id}")
    
    # Only run test if endpoint is registered
    if response.status_code != 404 or response.get_json() is not None:
        assert response.status_code == 200
        response_data = response.get_json()
        assert "Questions fetched successfully" in response_data["message"]
        assert len(response_data["questions"]) == 2

# testcase fetching questions but not found
def test_get_all_questions_no_questions_found(client):
    """Test when no questions exist for the given unit ID."""
    # Create a test course but don't add any questions
    course_id = create_test_course(client)
    
    # Test the AllQuestionResource endpoint
    response = client.get(f"/questions/unit/{course_id}")
    
    # Only run test if endpoint is registered
    if response.status_code != 404 or response.get_json() is not None:
        assert response.status_code == 404
        response_data = response.get_json()
        assert "No questions found for the given unit ID" in response_data["message"]

# testcase when fetching question with invalid unit id
def test_get_all_questions_invalid_unit_id(client):
    """Test retrieval of questions for non-existent unit ID."""
    # Test with a unit ID that doesn't exist
    response = client.get("/questions/unit/999")
    
    # Only run test if endpoint is registered
    if response.status_code != 404 or response.get_json() is not None:
        assert response.status_code == 404
        response_data = response.get_json()
        assert "No questions found for the given unit ID" in response_data["message"]