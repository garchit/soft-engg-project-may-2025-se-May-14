import pytest
from models import db
from models.unit import Unit
from models.lecture import Lecture

## Testcases for video summary ##

def test_video_summary_success(client):
    """Test successful video summary generation"""
    
    unit = Unit(title="Finance Unit", description="Finance basics unit")
    db.session.add(unit)
    db.session.commit()

    lecture = Lecture(
        unit_id=unit.id,
        title="Sample Lecture",
        description="Lecture with valid YouTube link",
        link="https://www.youtube.com/watch?v=5MgBikgcWnY"
    )
    db.session.add(lecture)
    db.session.commit()

    response = client.get(f"/Finance_Tutor/video_summary/{lecture.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["lecture_id"] == lecture.id
    assert "summary" in data
    assert isinstance(data["summary"], str)
    assert data["summary"].strip() != ""
    assert "generated_at" in data


def test_video_summary_lecture_not_found(client):
    """Test when lecture ID doesn't exist"""
    response = client.get("/Finance_Tutor/video_summary/9999")
    data = response.get_json()

    assert response.status_code == 404
    assert "error" in data
    assert data["error"] == "Lecture not found or missing link."


def test_video_summary_missing_link(client):
    """Test when lecture has no link"""
    unit = Unit(title="No Link Unit", description="Test")
    db.session.add(unit)
    db.session.commit()

    lecture = Lecture(
        unit_id=unit.id,
        title="Missing Link Lecture",
        description="No link provided",
        link=None
    )
    db.session.add(lecture)
    db.session.commit()

    response = client.get(f"/Finance_Tutor/video_summary/{lecture.id}")
    data = response.get_json()

    assert response.status_code == 404
    assert "error" in data
    assert data["error"] == "Lecture not found or missing link."


def test_video_summary_empty_link(client):
    """Test when lecture link is an empty string"""
    unit = Unit(title="Empty Link Unit", description="Empty link test")
    db.session.add(unit)
    db.session.commit()

    lecture = Lecture(
        unit_id=unit.id,
        title="Empty Link Lecture",
        description="Lecture with empty string link",
        link=""
    )
    db.session.add(lecture)
    db.session.commit()

    response = client.get(f"/Finance_Tutor/video_summary/{lecture.id}")
    data = response.get_json()

    assert response.status_code == 404
    assert "error" in data
    assert data["error"] == "Lecture not found or missing link."




def test_video_summary_duplicate_lecture(client):
    """Test if duplicate lectures with same link are handled separately"""
    unit = Unit(title="Duplicate Lecture Unit", description="Duplicate test")
    db.session.add(unit)
    db.session.commit()

    link = "https://www.youtube.com/watch?v=5MgBikgcWnY"

    lecture1 = Lecture(unit_id=unit.id, title="Lecture 1", description="First", link=link)
    lecture2 = Lecture(unit_id=unit.id, title="Lecture 2", description="Second", link=link)
    
    db.session.add(lecture1)
    db.session.add(lecture2)
    db.session.commit()

    response1 = client.get(f"/Finance_Tutor/video_summary/{lecture1.id}")
    response2 = client.get(f"/Finance_Tutor/video_summary/{lecture2.id}")

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.get_json()["summary"] == response2.get_json()["summary"]


def test_video_summary_non_integer_id(client):
    """Test when lecture ID is non-integer (invalid path param)"""
    response = client.get("/Finance_Tutor/video_summary/abc")
    assert response.status_code in (404, 422)  
