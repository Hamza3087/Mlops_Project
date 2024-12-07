from sqlalchemy.orm import Session
from models import User
import pickle
import pandas as pd

# Signup function
def signup(db: Session, username: str, email: str, password: str):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise ValueError("Username already exists")
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

# Login function
def login(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise ValueError("User not found")
    if user.password != password:
        raise ValueError("Incorrect password")
    return {"message": "Login successful"}

# Prediction function
def predict(model, humidity: float, wind_speed: float):
    df = pd.DataFrame([[humidity, wind_speed]], columns=["humidity", "wind_speed"])
    temperature = model.predict(df)[0]
    return {"temperature": temperature}
