
import requests
import os
from django.shortcuts import render

def index(request):
    weather_data = None
    error_message = None
    icon_image = 'images/clear.jpg' # Default

    if request.method == 'POST':
        city = request.POST.get('city')
        api_key = os.getenv('OPENWEATHER_API_KEY')
        api_url = os.getenv('OPENWEATHER_API_URL')

        if city:
            params = {'q': city, 'appid': api_key, 'units': 'metric'}
            try:
                response = requests.get(api_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    weather_main = data['weather'][0]['main']
                    
                    if weather_main == "Clouds":
                        icon_image = 'images/clouds.png'
                    elif weather_main == "Clear":
                        icon_image = 'images/clear.jpg'
                    elif weather_main == "Rain":
                        icon_image = 'images/rainy.jpg'
                    elif weather_main == "Drizzle":
                        icon_image = 'images/drizzle.jpg'
                    elif weather_main == "Mist":
                        icon_image = 'images/mistt.jpg'

                    weather_data = {
                        'city': data['name'],
                        'temp': round(data['main']['temp']),
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'icon': icon_image
                    }
                else:
                    error_message = "City not found"
            except Exception as e:
                error_message = "Connection error"
        else:
            error_message = "Please enter a city name"

    return render(request, 'weather_app/index.html', {
        'weather_data': weather_data, 
        'error_message': error_message
    })
