import os
import sys

# Define the project structure and file contents
project_name = "weather_project"
app_name = "weather_app"

# Configuration contents
requirements_txt = """Django==5.0.2
python-dotenv==1.0.0
requests==2.31.0
gunicorn==20.1.0
"""

env_file = """OPENWEATHER_API_KEY=33759db38860ae0f1e7ca418fe919121
OPENWEATHER_API_URL=https://api.openweathermap.org/data/2.5/weather
DEBUG=True
SECRET_KEY=django-insecure-weather-app-secret-key-998877
"""

procfile = f"""web: gunicorn {project_name}.wsgi"""

manage_py = f"""#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""

# Project Inner Files
settings_py = f"""
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '{app_name}',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{project_name}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{project_name}.wsgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

AUTH_PASSWORD_VALIDATORS = [
    {{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
"""

urls_py = f"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('{app_name}.urls')),
]
"""

wsgi_py = f"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
application = get_wsgi_application()
"""

# App Files
app_views_py = f"""
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
            params = {{'q': city, 'appid': api_key, 'units': 'metric'}}
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

                    weather_data = {{
                        'city': data['name'],
                        'temp': round(data['main']['temp']),
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'icon': icon_image
                    }}
                else:
                    error_message = "City not found"
            except Exception as e:
                error_message = "Connection error"
        else:
            error_message = "Please enter a city name"

    return render(request, '{app_name}/index.html', {{
        'weather_data': weather_data, 
        'error_message': error_message
    }})
"""

app_urls_py = """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
"""

# HTML Content
index_html = f"""{{% load static %}}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Weather</title>
    <link rel="stylesheet" href="{{% static 'css/style.css' %}}">
</head>
<body>
    <div class="card">
        <form method="POST" class="search">
            {{% csrf_token %}}
            <input type="text" name="city" placeholder="enter city name" spellcheck="false" required>
            <button type="submit"><img src="{{% static 'images/search.png' %}}" alt="search"></button>
        </form>

        {{% if error_message %}}
        <div class="error" style="display: block;">
            <p>{{{{ error_message }}}}</p>
        </div>
        {{% endif %}}

        {{% if weather_data %}}
        <div class="weather" style="display: block;">
            <img src="{{% static weather_data.icon %}}" class="weather-icon">
            <h1 class="temp">{{{{ weather_data.temp }}}}°C</h1>
            <h2 class="city">{{{{ weather_data.city }}}}</h2>
            <div class="details">
                <div class="col">
                    <img src="{{% static 'images/humidity.jpg' %}}">
                    <div>
                        <p class="humidity">{{{{ weather_data.humidity }}}}%</p>
                        <p>Humidity</p>
                    </div>
                </div>
                <div class="col">
                    <img src="{{% static 'images/wind.png' %}}" alt="wind"> 
                    <div>
                        <p class="wind">{{{{ weather_data.wind_speed }}}} km/h</p>
                        <p>Wind Speed</p>
                    </div>
                </div>
            </div>
        </div>
        {{% endif %}}
    </div>
</body>
</html>
"""

# CSS Content
style_css = """
*{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
body{ background: #222; }
.card{
    width: 90%; max-width: 470px; background: linear-gradient(135deg, #00feba, #5b548a);
    color: #fff; margin: 100px auto 0; border-radius: 20px; padding: 40px 35px; text-align: center;
}
.search{ width: 100%; display: flex; align-items: center; justify-content: space-between; }
.search input{
    border: 0; outline: 0; background: #ebfffc; color: #555; padding: 10px 25px;
    height: 60px; border-radius: 30px; flex: 1; margin-right: 16px; font-size: 18px;
}
.search button{
    border: 0; outline: 0; background: #ebfffc; border-radius: 50%; width: 60px; height: 60px; cursor: pointer;
}
.search button img{ width: 30px; }
.weather-icon{ width: 170px; margin-top: 30px; }
.weather h1{ font-size: 80px; font-weight: 500; }
.weather h2{ font-size: 40px; font-weight: 400; margin-top: -10px; }
.details{ display: flex; align-items: center; padding: 0 20px; justify-content: space-between; margin-top: 50px; }
.col{ display: flex; align-items: center; text-align: left; }
.col img{ width: 40px; margin-right: 10px; }
.humidity, .wind{ font-size: 28px; margin-top: -6px; }
.error{ text-align: left; margin-left: 10px; font-size: 14px; margin-top: 10px; color: #ffcccc; display: none; }
"""

def create_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

def main():
    # 1. Create Directories
    dirs = [
        project_name,
        f"{project_name}/{project_name}",
        app_name,
        f"{app_name}/migrations",
        f"{app_name}/templates",
        f"{app_name}/templates/{app_name}",
        f"{app_name}/static",
        f"{app_name}/static/css",
        f"{app_name}/static/images",
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        # Create __init__.py for python packages
        if "static" not in d and "templates" not in d:
             open(os.path.join(d, "__init__.py"), 'a').close()

    # 2. Write Files
    create_file("requirements.txt", requirements_txt)
    create_file(".env", env_file)
    create_file("Procfile", procfile)
    create_file("manage.py", manage_py)
    
    # Project Settings
    create_file(f"{project_name}/{project_name}/settings.py", settings_py)
    create_file(f"{project_name}/{project_name}/urls.py", urls_py)
    create_file(f"{project_name}/{project_name}/wsgi.py", wsgi_py)
    
    # App Logic
    create_file(f"{app_name}/views.py", app_views_py)
    create_file(f"{app_name}/urls.py", app_urls_py)
    
    # Static & Templates
    create_file(f"{app_name}/templates/{app_name}/index.html", index_html)
    create_file(f"{app_name}/static/css/style.css", style_css)

    print("\n" + "="*50)
    print(" PROJECT GENERATED SUCCESSFULLY! ")
    print("="*50)
    print("Next Steps:")
    print(f"1. Move your image files (search.png, clear.jpg, etc.) into: {app_name}/static/images/")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: python manage.py migrate")
    print("4. Run: python manage.py runserver")

if __name__ == "__main__":
    main()