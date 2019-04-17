import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


# Create your views here.


def index(request):
    # OpenWeatherMap API endpoint
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}'
    api_key = 'c4af811c05a1cdeea2526001714ae63c'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    # instantiate Form
    form = CityForm()

    # get all cities
    cities = City.objects.all()

    # where we will store our data
    weather_data = []

    # loop through cities, get weather data for each, store in weather_data
    for city in cities:
        r = requests.get(url.format(city, api_key)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'country': r['sys']['country']
        }

        weather_data.append(city_weather)

    # display recently added city first
    weather_data.reverse()

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)
