import sys
import os
import pytest
from unittest.mock import MagicMock
import pandas as pd

# Add the project root directory to sys.path so Python can find mlops_project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import signup, login, predict  # Import from app.py
from pydantic import BaseModel

# Mocking the User model
class MockUser:
    def __init__(self, username, email, hashed_password):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

# Mock session (replace the actual database session)
@pytest.fixture
def db():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None  # No user exists initially
    return db

# Test signup function
def test_signup(db):
    # Test creating a new user
    db.query.return_value.filter.return_value.first.return_value = None  # No user exists
    user_data = {"username": "testuser", "email": "testuser@example.com", "password": "password123"}
    user_create = signup(user_data, db=db)  # Adjusted to pass UserCreate model
    response = user_create.dict()  # Pydantic model to dict conversion
    assert response["message"] == "User created successfully"

    # Test username already exists
    db.query.return_value.filter.return_value.first.return_value = MockUser("testuser", "testuser@example.com", "hashedpassword123")
    with pytest.raises(ValueError):
        signup(user_data, db=db)

# Test login function
def test_login(db):
    # Test valid login
    mock_user = MockUser("testuser", "testuser@example.com", "hashedpassword123")
    db.query.return_value.filter.return_value.first.return_value = mock_user
    user_data = {"username": "testuser", "password": "password123"}
    user_login = login(user_data, db=db)  # Adjusted to pass UserLogin model
    response = user_login.dict()  # Pydantic model to dict conversion
    assert response["message"] == "Login successful"

    # Test invalid username
    db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(ValueError):
        login(user_data, db=db)

    # Test invalid password
    db.query.return_value.filter.return_value.first.return_value = mock_user
    with pytest.raises(ValueError):
        login(user_data, db=db)

# Test prediction function
def test_predict():
    # Mocking the model's predict method
    class MockModel:
        def predict(self, df):
            return [25.0]  # Fake predicted temperature value

    model = MockModel()
    data = {"humidity": 60.0, "wind_speed": 10.0}
    response = predict(model, data)  # Correct the way we pass the data
    assert response["temperature"] == 25.0
