import requests
import os

class ApiAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPEN_WEATHER_KEY')
         
    def get_weather(self, city="Los Angeles"):
        """Fetch the weather for a given city using the OpenWeatherMap API."""
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Weather in {city}: {data['weather'][0]['description']}")
        else:
            print("Failed to retrieve weather data.")
