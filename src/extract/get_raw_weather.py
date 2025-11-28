import os
import requests
from dotenv import load_dotenv

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
    print(data)
