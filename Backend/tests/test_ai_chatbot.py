import pytest
import json
import pytest

# Test 1: Valid finance-related question
def test_chatbot_valid_finance_question(client):
    response = client.post("/Finance_Tutor/ai_chatbot", json={"question": "What is a stock?"})
    data = response.get_json()

    assert response.status_code == 200
    assert "question" in data
    assert data["question"] == "What is a stock?"
    assert isinstance(data["answer"], str)
    assert data["answer"].strip() != ""

# Test 2: Casual small talk
def test_chatbot_casual_small_talk(client):
    response = client.post("/Finance_Tutor/ai_chatbot", json={"question": "How are you today?"})
    data = response.get_json()

    assert response.status_code == 200
    assert "how" in data["question"].lower()
    assert isinstance(data["answer"], str)
    assert data["answer"].strip() != ""

# Test 3: Completely unrelated question
def test_chatbot_unrelated_question(client):
    response = client.post("/Finance_Tutor/ai_chatbot", json={"question": "How to fix a car engine?"})
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data["answer"], str)
    assert "sorry" in data["answer"].lower() or "out of my scope" in data["answer"].lower()

# Test 4: Long and detailed finance question
def test_chatbot_long_detailed_question(client):
    question = "Can you explain the difference between options and futures contracts with examples and use cases?"
    response = client.post("/Finance_Tutor/ai_chatbot", json={"question": question})
    data = response.get_json()

    assert response.status_code == 200
    assert data["question"] == question
    assert isinstance(data["answer"], str)
    assert len(data["answer"].strip()) > 20

# Test 5: Special characters and finance abbreviations
def test_chatbot_question_with_special_characters(client):
    response = client.post("/Finance_Tutor/ai_chatbot", json={"question": "What is ROI? @#&!"})
    data = response.get_json()

    assert response.status_code == 200
    assert "roi" in data["question"].lower()
    assert isinstance(data["answer"], str)
    assert data["answer"].strip() != ""

# Test 6: No repeated lines in the answer
def test_chatbot_no_duplicate_lines_in_answer(client):
    response = client.post("/Finance_Tutor/ai_chatbot", json={"question": "Define finance"})
    data = response.get_json()

    assert response.status_code == 200
    answer_lines = [line.strip() for line in data["answer"].splitlines() if line.strip()]
    assert len(answer_lines) == len(set(answer_lines)), "Answer contains repeated lines"
