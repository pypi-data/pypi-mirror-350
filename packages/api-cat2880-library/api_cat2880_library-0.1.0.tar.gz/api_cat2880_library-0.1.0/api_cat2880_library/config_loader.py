import os
import yaml
from typing import Dict, Any


class ConfigLoader:
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)

        return config

    @staticmethod
    def get_api_config(file_path: str) -> Dict[str, Any]:
        config = ConfigLoader.load_yaml(file_path)

        if 'api' not in config:
            raise KeyError("API configuration not found in YAML file")

        return config['api']

    @staticmethod
    def get_weather_api_config(file_path: str) -> Dict[str, Any]:
        api_config = ConfigLoader.get_api_config(file_path)

        if 'weather' not in api_config:
            raise KeyError("Weather API configuration not found in YAML file")

        return api_config['weather']

    @staticmethod
    def get_twine_credentials(file_path: str) -> Dict[str, str]:
        config = ConfigLoader.load_yaml(file_path)

        if 'run' not in config or 'variables' not in config['run']:
            raise KeyError("Twine credentials not found in YAML file")

        variables = config['run']['variables']

        return {
            'username': variables.get('TWINE_USERNAME', ''),
            'password': variables.get('TWINE_PASSWORD', '')
        }
