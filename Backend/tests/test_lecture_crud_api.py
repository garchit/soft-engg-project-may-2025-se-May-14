from models.lecture import Lecture
from models.unit import Unit as Course
from models import db

### Testacse for Lecture Crud ###

# create a course before adding lectures
def create_test_unit():
    unit = Course(title="Unit A", description="Basic unit")
    db.session.add(unit)
    db.session.commit()
    return unit.id

# Testcase for creating a lecture successfully
def test_create_lecture_success(client):
    unit_id = create_test_unit()
    response = client.post("/Finance_Tutor/lecture", json={
        "title": "Lecture 1",
        "description": "Intro to Finance",
        "link": "https://lecturelink.com",
        "unit_id": unit_id
    })
    assert response.status_code == 201
    assert "Lecture added successfully" in response.get_json()["message"]

# Testcase for creating lecture with duplicate title in same unit
def test_create_duplicate_lecture(client):
    unit_id = create_test_unit()
    client.post("/Finance_Tutor/lecture", json={
        "title": "Duplicate Lecture",
        "description": "Some desc",
        "link": "http://link.com",
        "unit_id": unit_id
    })

    response = client.post("/Finance_Tutor/lecture", json={
        "title": "Duplicate Lecture",
        "description": "Another desc",
        "link": "http://link2.com",
        "unit_id": unit_id
    })
    assert response.status_code == 400
    assert "already exists" in response.get_json()["error"]

# Testcase for getting a lecture
def test_get_lecture_success(client):
    unit_id = create_test_unit()
    lecture = Lecture(title="Test L", description="test desc", link="link", unit_id=unit_id)
    db.session.add(lecture)
    db.session.commit()

    response = client.get(f"/Finance_Tutor/lecture/{lecture.id}")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Test L"

# Testcase for getting a non-existent lecture
def test_get_lecture_not_found(client):
    response = client.get("/Finance_Tutor/lecture/999")
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"]

# Testcase for updating lecture
def test_update_lecture_success(client):
    unit_id = create_test_unit()
    lecture = Lecture(title="To Update", description="Old", link="link", unit_id=unit_id)
    db.session.add(lecture)
    db.session.commit()

    response = client.put(f"/Finance_Tutor/lecture/{lecture.id}", json={
        "title": "Updated",
        "description": "Updated Desc",
        "link": "updated_link",
        "unit_id": unit_id
    })
    assert response.status_code == 200
    assert response.get_json()["title"] == "Updated"

# Testcase for updating with duplicate title in same unit
def test_update_lecture_duplicate_title(client):
    unit_id = create_test_unit()
    l1 = Lecture(title="Original", description="1", link="1", unit_id=unit_id)
    l2 = Lecture(title="Duplicate", description="2", link="2", unit_id=unit_id)
    db.session.add_all([l1, l2])
    db.session.commit()

    response = client.put(f"/Finance_Tutor/lecture/{l1.id}", json={
        "title": "Duplicate",  # Title of l2
        "description": "updated",
        "link": "updated",
        "unit_id": unit_id
    })
    assert response.status_code == 400
    assert "already exists" in response.get_json()["error"]

# Testcase for  Delete Lecture
def test_delete_lecture_success(client):
    unit_id = create_test_unit()
    lecture = Lecture(title="To Delete", description="desc", link="link", unit_id=unit_id)
    db.session.add(lecture)
    db.session.commit()

    response = client.delete(f"/Finance_Tutor/lecture/{lecture.id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.get_json()["message"]

# Test Delete Non-existent Lecture
def test_delete_lecture_not_found(client):
    response = client.delete("/Finance_Tutor/lecture/999")
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"]
