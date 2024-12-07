import sys
import os
import pytest
from unittest.mock import MagicMock
import pandas as pd
from fastapi import HTTPException
from passlib.context import CryptContext  # Import passlib for password hashing

# Add the project root directory to sys.path so Python can find mlops_project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import signup, login, predict  # Import from app.py
from pydantic import BaseModel

# Define Pydantic models to use for the tests
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

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
    user_data = UserCreate(username="testuser", email="testuser@example.com", password="password123")
    user_create = signup(user_data, db=db)  # Pass Pydantic model instead of dictionary
    response = user_create  # Return the dict directly from FastAPI endpoint
    assert response["message"] == "User created successfully"

    # Test username already exists
    db.query.return_value.filter.return_value.first.return_value = MockUser("testuser", "testuser@example.com", "hashedpassword123")
    with pytest.raises(HTTPException):
        signup(user_data, db=db)

# Test login function
def test_login(db):
    # Initialize password context for hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Mock the hashed password using passlib's context
    hashed_password = pwd_context.hash("password123")
    mock_user = MockUser("testuser", "testuser@example.com", hashed_password)
    db.query.return_value.filter.return_value.first.return_value = mock_user
    user_data = UserLogin(username="testuser", password="password123")  # Pass Pydantic model instead of dictionary

    # Test valid login
    user_login = login(user_data, db=db)  # Pass Pydantic model instead of dictionary
    response = user_login  # Return the dict directly from FastAPI endpoint
    assert response["message"] == "Login successful"

    # Test invalid username
    db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException):
        login(user_data, db=db)

    # Test invalid password (incorrect password)
    db.query.return_value.filter.return_value.first.return_value = mock_user
    # Simulating an incorrect password
    incorrect_user_data = UserLogin(username="testuser", password="wrongpassword")
    with pytest.raises(HTTPException):
        login(incorrect_user_data, db=db)

# Test prediction function
def test_predict():
    # Mocking the model's predict method
    class MockModel:
        def predict(self, df):
            return [25.0]  # Fake predicted temperature value

    model = MockModel()
    data = {"humidity": 60.0, "wind_speed": 10.0}
    # Modify predict call to only pass the necessary arguments
    response = predict(data)  # Pass correct arguments
    assert response["temperature"] == 25.0
