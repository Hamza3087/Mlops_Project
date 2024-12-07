import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # Import FastAPI app from app.py
from models import User, Base
from database import SessionLocal, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
import pickle

# Mock Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use SQLite for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency override for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override FastAPI dependency with test DB
app.dependency_overrides[get_db] = override_get_db

# Initialize TestClient
client = TestClient(app)


# 1. Test Signup Endpoint
def test_signup_user():
    response = client.post(
        "/signup",
        json={"username": "testuser", "email": "testuser@example.com", "password": "test123"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}


def test_signup_existing_user():
    client.post("/signup", json={"username": "testuser", "email": "testuser@example.com", "password": "test123"})
    response = client.post(
        "/signup",
        json={"username": "testuser", "email": "testuser@example.com", "password": "test123"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists"}


# 2. Test Login Endpoint
def test_login_user():
    client.post("/signup", json={"username": "loginuser", "email": "login@example.com", "password": "pass123"})
    response = client.post(
        "/login", json={"username": "loginuser", "password": "pass123"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}


def test_login_user_not_found():
    response = client.post(
        "/login", json={"username": "unknownuser", "password": "pass123"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_login_incorrect_password():
    client.post("/signup", json={"username": "wrongpassuser", "email": "wrong@example.com", "password": "pass123"})
    response = client.post(
        "/login", json={"username": "wrongpassuser", "password": "wrongpass"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect password"}


# 3. Test Prediction Endpoint
class MockModel:
    def predict(self, df):
        return [25.5]  # Mock prediction value


def test_prediction_valid_data():
    with patch("builtins.open", create=True), patch("pickle.load", return_value=MockModel()):
        response = client.post(
            "/predict", json={"humidity": 50, "wind_speed": 10}
        )
    assert response.status_code == 200
    assert "temperature" in response.json()


def test_prediction_invalid_data():
    response = client.post(
        "/predict", json={"humidity": "not a number", "wind_speed": 10}
    )
    assert response.status_code == 422  # Unprocessable entity
