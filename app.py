
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User, Base
from database import engine, get_db
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd


app = FastAPI()

# Add CORS middleware
origins = ["http://localhost:3000"]  # React frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
Base.metadata.create_all(bind=engine)

# Password hashing using Passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models to validate incoming request data
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Helper function to hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to get user by username
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Signup Endpoint
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = get_user(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create new user
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    
    return {"message": "User created successfully"}

# Login Endpoint
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Check if the user exists
    existing_user = get_user(db, user.username)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify the password
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    return {"message": "Login successful"}


# Add CORS middleware to allow requests from any origin
origins = [
    "http://localhost",  # Allow local frontend
    "http://localhost:3000",  # Allow React on localhost
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Load the model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.post("/predict")
def predict(data: dict):
    humidity = data["humidity"]
    wind_speed = data["wind_speed"]
    df = pd.DataFrame([[humidity, wind_speed]], columns=["Humidity", "Wind Speed"])
    prediction = model.predict(df)
    return {"temperature": prediction[0]}
