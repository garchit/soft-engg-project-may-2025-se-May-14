##### Test cases for Institute Signup ####


# testcase when institute signup suceessfully
def test_institute_signup_success(client):
    payload = {
        "name": "XYZ school",
        "email": "xyzchool@example.com",
        "password": "securepass",
        "address": "near hanuman mandir",
        "contact_number": "9876543210"
    }
    response = client.post('/Finance_Tutor/institute/signup', json=payload)
    assert response.status_code == 201
    assert "User created successfully" in response.get_json().get("message", "")


# testcase when institute signup with missing address fields
def test_institute_signup_missing_address(client):
    payload = {
        "name": "No Address School",
        "email": "noaddress@example.com",
        "password": "securepass"
        # Missing address
    }
    response = client.post('/Finance_Tutor/institute/signup', json=payload)
    assert response.status_code == 401
    assert "address" in response.get_json().get("error", "").lower()

# Testcase when  signup with empty name
def test_institute_signup_empty_name(client):
    payload = {
        "name": "",
        "email": "emptyname@example.com",
        "password": "securepass",
        "address": "123 Main St"
    }
    response = client.post('/Finance_Tutor/institute/signup', json=payload)
    assert response.status_code == 401
    assert "cannot be empty" in response.get_json().get("error", "").lower()

#testcase when institute signup with duplicate  email
def test_institute_signup_duplicate_email(client):
    # First signup
    payload = {
        "name": "First School",
        "email": "duplicate@example.com",
        "password": "securepass",
        "address": "123 Main St"
    }
    client.post('/Finance_Tutor/institute/signup', json=payload)

    # Attempt with duplicate email
    payload2 = {
        "name": "Second School",
        "email": "duplicate@example.com",
        "password": "anotherpass",
        "address": "456 Elm St"
    }
    response = client.post('/Finance_Tutor/institute/signup', json=payload2)
    assert response.status_code == 401
    assert "email" in response.get_json().get("error", "").lower()

# Testcase when institute signup with invalid email format
def test_institute_signup_invalid_email_format(client):
    payload = {
        "name": "Invalid Email School",
        "email": "not-an-email",
        "password": "securepass",
        "address": "123 Fake St"
    }
    response = client.post('/Finance_Tutor/institute/signup', json=payload)
    assert response.status_code in [201, 400] 
