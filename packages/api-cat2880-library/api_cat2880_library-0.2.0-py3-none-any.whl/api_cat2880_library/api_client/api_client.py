import requests
from typing import Dict, Any, Optional

class ApiClient:
    def __init__(self, base_url: str, api_key: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = headers or {}
        self.headers.update({
            'X-RapidAPI-Key': api_key,
            'Content-Type': 'application/json'
        })

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

