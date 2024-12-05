import requests
import pandas as pd
from datetime import datetime

API_KEY = "1720969d247faec50cd966e8ac0f922e"
CITY = "Lahore"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

def fetch_weather_data():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        weather_data = []
        for entry in data["list"]:
            weather_data.append({
                "Temperature": entry["main"]["temp"],
                "Humidity": entry["main"]["humidity"],
                "Wind Speed": entry["wind"]["speed"],
                "Weather Condition": entry["weather"][0]["description"],
                "Date Time": entry["dt_txt"]
            })
        df = pd.DataFrame(weather_data)
        df.to_csv("raw_data.csv", index=False)
        print("Weather data saved to raw_data.csv")
    else:
        print("Failed to fetch data:", response.status_code)

if __name__ == "__main__":
    fetch_weather_data()
