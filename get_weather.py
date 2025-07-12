import requests

WEATHER_API_KEY = 'a61019d898eb1475d0762593c6196ddb'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/forecast'


def get_city_weather(city, country_code=None):
    try:
        query = f"{city},{country_code}" if country_code else city
        params = {
            'q': query,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        response = requests.get(WEATHER_URL, params=params)
        data = response.json()

        if data['cod'] != '200':
            return None, None, "Город не найден. Попробуйте еще раз."

        city_name = data['city']['name']
        country = data['city']['country']

        weather_by_day = {}
        for forecast in data['list']:
            date, time = forecast['dt_txt'].split()
            temp = forecast['main']['temp']
            desc = forecast['weather'][0]['description']
            if date not in weather_by_day:
                weather_by_day[date] = []
            weather_by_day[date].append((time, temp, desc))

        weather_report = f"Погода в {city_name}, {country}:\n\n"

        for date, forecasts in weather_by_day.items():
            weather_report += f"📅 {date}:\n"
            for time, temp, desc in forecasts:
                label = ''
                if '06:00:00' in time:
                    label = '🌅 Утро'
                elif '12:00:00' in time:
                    label = '🌞 День'
                elif '18:00:00' in time:
                    label = '🌆 Вечер'
                if label:
                    weather_report += f"{label} — {temp}°C, {desc.capitalize()}\n"
            weather_report += "\n"

        return city_name, country, weather_report.strip()

    except Exception as e:
        print(f"Error: {e}")
        return None, None, "Ошибка при получении погоды."
