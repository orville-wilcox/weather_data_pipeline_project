import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime
from src.validation.validator import validate_weather_payload

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city: str = "São Paulo"):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()   # raises error if API fails (good for debugging)
    return response.json()

if __name__ == "__main__":
    data = fetch_weather()
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/weather_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Saved raw response to: {filename}")
    
    #Validate data
    is_valid, errors = validate_weather_payload(data)
    print(is_valid)
    print(errors)