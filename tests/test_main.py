import pytest
from unittest.mock import MagicMock
import pandas as pd
from sqlalchemy.orm import Session
from mlops_project.app import signup, login, predict  # Update this path


# Mocking the User model
class MockUser:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

# Mock session (replace the actual database session)
@pytest.fixture
def db():
    db = MagicMock(Session)
    db.query.return_value.filter.return_value.first.return_value = None  # No user exists initially
    return db

# Test signup function
def test_signup(db):
    # Test creating a new user
    db.query.return_value.filter.return_value.first.return_value = None  # No user exists
    response = signup(db, "testuser", "testuser@example.com", "password123")
    assert response["message"] == "User created successfully"

    # Test username already exists
    db.query.return_value.filter.return_value.first.return_value = MockUser("testuser", "testuser@example.com", "password123")
    with pytest.raises(ValueError):
        signup(db, "testuser", "anotheruser@example.com", "password123")

# Test login function
def test_login(db):
    # Test valid login
    mock_user = MockUser("testuser", "testuser@example.com", "password123")
    db.query.return_value.filter.return_value.first.return_value = mock_user
    response = login(db, "testuser", "password123")
    assert response["message"] == "Login successful"

    # Test invalid username
    db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(ValueError):
        login(db, "invaliduser", "password123")

    # Test invalid password
    db.query.return_value.filter.return_value.first.return_value = mock_user
    with pytest.raises(ValueError):
        login(db, "testuser", "wrongpassword")

# Test prediction function
def test_predict():
    # Mocking the model's predict method
    class MockModel:
        def predict(self, df):
            return [25.0]  # Fake predicted temperature value

    model = MockModel()
    response = predict(model, 60.0, 10.0)
    assert response["temperature"] == 25.0

