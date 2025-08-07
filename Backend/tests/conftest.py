# conftest.py
import sys
import os

# Add the parent directory of your project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from factory import create_app
from models import db
from config import TestingConfig

@pytest.fixture(scope="function")
def test_app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()

@pytest.fixture(scope="function")
def client(test_app):
    return test_app.test_client()
