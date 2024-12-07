from sqlalchemy.orm import Session
import pandas as pd
import pickle

# Mock Database
DATABASE = []

# Mock User Class
class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

# Signup function
def signup(username: str, email: str, password: str):
    # Check if username already exists
    for user in DATABASE:
        if user.username == username:
            raise ValueError("Username already exists")
    
    # Add new user
    new_user = User(username=username, email=email, password=password)
    DATABASE.append(new_user)
    return {"message": "User created successfully"}

# Login function
def login(username: str, password: str):
    # Search for user
    for user in DATABASE:
        if user.username == username:
            if user.password == password:
                return {"message": "Login successful"}
            else:
                raise ValueError("Incorrect password")
    raise ValueError("User not found")

# Mock Model for Prediction
class MockModel:
    def predict(self, df: pd.DataFrame):
        # A simple formula for mock temperature prediction
        return [df['humidity'][0] * 0.5 + df['wind_speed'][0] * 0.2 + 10]

# Prediction function
def predict(model, humidity: float, wind_speed: float):
    df = pd.DataFrame([[humidity, wind_speed]], columns=["humidity", "wind_speed"])
    temperature = model.predict(df)[0]
    return {"temperature": temperature}

# Testing the Code
if __name__ == "__main__":
    try:
        # Signup Test
        print("----- Signup Test -----")
        print(signup(username="hamza", email="hamza@example.com", password="1234"))
        
        # Signup with existing username
        try:
            print(signup(username="hamza", email="hamza@example.com", password="1234"))
        except ValueError as e:
            print("Error:", e)
        
        # Login Test
        print("\n----- Login Test -----")
        print("Login with correct credentials:")
        print(login(username="hamza", password="1234"))
        
        print("Login with incorrect credentials:")
        try:
            print(login(username="hamza", password="wrongpass"))
        except ValueError as e:
            print("Error:", e)
        
        print("Login with non-existing user:")
        try:
            print(login(username="unknown", password="1234"))
        except ValueError as e:
            print("Error:", e)
        
        # Prediction Test
        print("\n----- Prediction Test -----")
        model = MockModel()
        humidity = 80.0
        wind_speed = 10.0
        print("Prediction Input: Humidity = 80.0, Wind Speed = 10.0")
        print(predict(model, humidity, wind_speed))
    
    except ValueError as e:
        print("Error:", e)
