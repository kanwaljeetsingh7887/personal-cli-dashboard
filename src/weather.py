import requests


def get_weather(api_key, city):
    if not api_key:
        return None
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    resp = requests.get(url, params=params, timeout=6)
    resp.raise_for_status()
    data = resp.json()
    return {
        'desc': data['weather'][0]['description'].title(),
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'wind': data['wind'].get('speed', None)
    }
