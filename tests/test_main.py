from fastapi import HTTPException
from passlib.context import CryptContext
from unittest.mock import MagicMock
import pytest

# Assuming these are your actual models and functions
from app import signup, login, UserCreate, UserLogin

# Mocking the user model and its password hashing
class MockUser:
    def __init__(self, username, email, hashed_password):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

    def verify_password(self, plain_password):
        # Dummy function for the purpose of the test
        return self.hashed_password == plain_password

# Set up password context for hashing (mimicking your actual app behavior)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

@pytest.fixture
def db():
    # Mock the db session
    db = MagicMock()
    return db

def test_signup(db):
    # Test creating a new user
    db.query.return_value.filter.return_value.first.return_value = None  # No user exists
    user_data = UserCreate(username="testuser", email="testuser@example.com", password="testpassword")
    user_create = signup(user_data, db=db)  # Pass Pydantic model instead of dictionary
    response = user_create  # Return the dict directly from FastAPI endpoint
    assert response["message"] == "User created successfully"

    # Test username already exists
    db.query.return_value.filter.return_value.first.return_value = MockUser("testuser", "testuser@example.com", hash_password("testpassword"))
    with pytest.raises(HTTPException):
        signup(user_data, db=db)

def test_login(db):
    # Test valid login
    mock_user = MockUser("testuser", "testuser@example.com", hash_password("testpassword"))
    db.query.return_value.filter.return_value.first.return_value = mock_user
    user_data = UserLogin(username="testuser", password="testpassword")  # Correctly pass the password field
    user_login = login(user_data, db=db)  # Pass Pydantic model instead of dictionary
    assert user_login  # Make appropriate assertions based on your login function

    # Test invalid password (wrong password)
    db.query.return_value.filter.return_value.first.return_value = mock_user
    user_data = UserLogin(username="testuser", password="wrongpassword")
    with pytest.raises(HTTPException):
        login(user_data, db=db)
