import requests
import sys
from datetime import datetime


class WttrWeatherAPI:
    BASE_URL = "https://wttr.in/"

    def get_weather(self, city: str) -> str:
        url = f"{self.BASE_URL}{city}?format=%t"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text.strip()
        except Exception as e:
            print(f"Error while fetching weather data: {e}")
            sys.exit()


class WeatherCLI:

    def __init__(self):
        self._weather_api = WttrWeatherAPI()

    @staticmethod
    def validate_city(city: str) -> str:
        if not city:
            print("City name is required.")
            sys.exit()
        return city

    def run(self):
        city = self.validate_city(input("Enter city name: "))
        weather_data = self._weather_api.get_weather(city)
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Temperature in {city.capitalize()} on {current_date} is {weather_data}")


if __name__ == "__main__":
    cli = WeatherCLI()
    cli.run()
