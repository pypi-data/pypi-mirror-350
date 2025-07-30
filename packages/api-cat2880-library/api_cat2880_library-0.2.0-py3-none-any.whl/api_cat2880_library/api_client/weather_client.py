import requests
from typing import Dict, Any, Optional


class WeatherApiClient:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.headers.update({
            'Accept': 'application/json',
        })

    def get_weather(self) -> Dict[str, Any]:
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching weather data: {str(e)}")