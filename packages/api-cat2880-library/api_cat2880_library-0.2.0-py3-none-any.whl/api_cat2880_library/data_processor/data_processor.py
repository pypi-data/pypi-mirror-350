from typing import Dict, Any, List, Optional
from datetime import datetime


class DataProcessor:
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        return round(kelvin - 273.15, 2)

    @staticmethod
    def format_temperature(temp: float, unit: str = 'K') -> str:
        if unit == 'K':
            temp = DataProcessor.kelvin_to_celsius(temp)
        return f"{temp}°C"

    @staticmethod
    def format_timestamp(timestamp: int) -> str:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def process_weather_data(data: Dict[str, Any]) -> Dict[str, Any]:
        if 'list' in data:
            return DataProcessor._process_forecast_data(data)
        return DataProcessor._process_current_weather_data(data)

    @staticmethod
    def _process_current_weather_data(data: Dict[str, Any]) -> Dict[str, Any]:
        main_data = data.get('main', {})
        weather_data = data.get('weather', [{}])[0]
        wind_data = data.get('wind', {})
        sys_data = data.get('sys', {})

        return {
            'location': f"{data.get('name', 'Unknown')}, {sys_data.get('country', '')}",
            'coordinates': f"Lat: {data.get('coord', {}).get('lat')}, Lon: {data.get('coord', {}).get('lon')}",
            'temperature': DataProcessor.format_temperature(
                main_data.get('temprature', 0),
                main_data.get('temprature_unit', 'K')
            ),
            'feels_like': DataProcessor.format_temperature(
                main_data.get('temprature_feels_like', 0),
                main_data.get('temprature_unit', 'K')
            ),
            'temperature_range': f"{DataProcessor.format_temperature(main_data.get('temprature_min', 0))} - {DataProcessor.format_temperature(main_data.get('temprature_max', 0))}",
            'weather': f"{weather_data.get('main', '')} - {weather_data.get('description', '')}",
            'humidity': f"{main_data.get('humidity', 0)}{main_data.get('humidity_unit', '%')}",
            'pressure': f"{main_data.get('pressure', 0)} {main_data.get('pressure_unit', 'hPa')}",
            'wind': f"{wind_data.get('speed', 0)} {wind_data.get('speed_unit', 'meter/sec')} from {wind_data.get('direction', 'Unknown')}",
            'cloudiness': f"{data.get('clouds', {}).get('cloudiness', 0)}{data.get('clouds', {}).get('unit', '%')}",
            'visibility': f"{data.get('visibility_distance', 0)} {data.get('visibility_unit', 'm')}",
            'sunrise': DataProcessor.format_timestamp(sys_data.get('sunrise', 0)),
            'sunset': DataProcessor.format_timestamp(sys_data.get('sunset', 0)),
            'last_updated': DataProcessor.format_timestamp(data.get('dt', 0))
        }

    @staticmethod
    def print_weather_data(data: Dict[str, Any]):
        processed_data = DataProcessor.process_weather_data(data)

        if 'forecasts' in processed_data:
            city_info = processed_data['city_info']
            forecasts = processed_data['forecasts']

            print("\nWeather Forecast Information")
            print("=" * 50)

            print("\nCity Information")
            print("-" * 20)
            print(f"City: {city_info['name']}, {city_info['country']}")
            print(f"Coordinates: {city_info['coordinates']}")
            print(f"Sunrise: {city_info['sunrise']}")
            print(f"Sunset: {city_info['sunset']}")

            for i, forecast in enumerate(forecasts, 1):
                print(f"\nForecast {i} - {forecast['datetime']}")
                print("-" * 40)
                
                sections = {
                    'Temperature': ['temperature', 'feels_like', 'temperature_range'],
                    'Weather Conditions': ['weather', 'cloudiness', 'visibility'],
                    'Wind & Pressure': ['wind', 'pressure', 'humidity'],
                    'Precipitation': ['precipitation_probability', 'rain', 'snow'],
                    'Additional Info': ['part_of_day']
                }

                for section, fields in sections.items():
                    print(f"\n{section}")
                    print("-" * len(section))
                    for field in fields:
                        if field in forecast:
                            print(f"{field.replace('_', ' ').title()}: {forecast[field]}")
        else:
            sections = {
                'Location Info': ['location', 'coordinates'],
                'Temperature': ['temperature', 'feels_like', 'temperature_range'],
                'Weather Conditions': ['weather', 'cloudiness', 'visibility'],
                'Wind & Pressure': ['wind', 'pressure', 'humidity'],
                'Sun Info': ['sunrise', 'sunset'],
                'Additional Info': ['last_updated']
            }

            print("\nWeather Information")
            print("=" * 50)

            for section, fields in sections.items():
                print(f"\n{section}")
                print("-" * len(section))
                for field in fields:
                    if field in processed_data:
                        print(f"{field.replace('_', ' ').title()}: {processed_data[field]}")


