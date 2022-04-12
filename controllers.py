import json
import requests

from models import *
from tools import add_url_parameter

GEOLOCATION_API_URL = "http://ip-api.com/json/"
OPEN_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
OPEN_WEATHER_API_KEY = 'b97aac961b6899d1caf2b26a2b88e534'


def get_location(ip: str = '', lang: str = 'en') -> Location:
    '''
    Get latitude and longitude by IPv4
    :param ip: IPv4 address to consult
    :param lang: language code (ISO 639) for names (city, region...), default English
    :return: Location object
    :raise:
        :Exception: Geolocation API service problems
    '''
    url = add_url_parameter(GEOLOCATION_API_URL + ip, {'lang': lang})
    response = requests.request("GET", url, headers={}, data={})

    if response.status_code == 200:
        response_json = json.loads(response.text)
        if response_json['status'] == 'fail':
            raise Exception(
                "Geolocalisation service: %s, IP address %s" % (response_json['message'], response_json['query']))
        return Location(response_json['lat'], response_json['lon'], response_json['city'])
    else:
        raise Exception("There's something wrong with the geolocalisation service")


def get_locations(ip_list: list, lang: str) -> list[Location]:
    '''
    Get lattitude and longitude by IPv4 list
    :param ip_list: IPv4 addresses to consult
    :param lang: language code (ISO 639) for names (city, region...), default English
    :return: list of Location object
    '''
    return list(map(lambda ip: get_location(ip, lang), ip_list))


def get_weather(lat: float, lon: float, lang: str, units: str = 'metric') -> Weather:
    '''
    Request weather forecast for the geolocation
    :param lat: float value representating the lattitude
    :param lon: float value representating the longitud
    :param lang: language code (ISO 639) for names (city, region...), default English
    :return: a Weather object
    :raise:
        :Exception: Weather API service problems
    '''

    # As the parameter units is setted manually by default in the code, the following strings represents the default measure units
    default_temperature_unit = 'Cº'
    default_wind_unit = 'm/s'

    url = add_url_parameter(OPEN_WEATHER_API_URL,
                            {'lang': lang, 'lat': lat, 'lon': lon, 'appid': OPEN_WEATHER_API_KEY, 'units': units})
    response = requests.request("GET", url, headers={}, data={})

    if response.status_code == 200:
        response_json = json.loads(response.text)
        coord_json = response_json['coord']
        weather_descriptions_json = response_json['weather']
        temperature_json = response_json['main']
        wind_json = response_json['wind']

        weather_descriptions = list(
            map(lambda weather_description: WeatherDescription(weather_description['main'],
                                                               weather_description['description'],
                                                               weather_description['icon']), weather_descriptions_json))
        location = Location(coord_json['lat'], coord_json['lon'], response_json['name'])
        temperature = WeatherTemperature(temperature_json['temp'], temperature_json['temp_min'],
                                         temperature_json['temp_max'], default_temperature_unit,
                                         temperature_json['feels_like'])
        wind = WeatherWind(wind_json['speed'], wind_json['deg'], default_wind_unit)

        return Weather(weather_descriptions, temperature, wind, location, lang)
    else:
        error_content = json.loads(response.content)
        raise Exception("Weather service: %s" % (error_content['message']))
        # Exception("There's something wrong with the weather service")


def get_weather_by_location(location: Location, lang: str) -> Weather:
    '''
    Request weather forecast for the geolocation by location object
    :param location: a Location instance
    :param lang: language code (ISO 639) for names (city, region...), default English
    :return: a Weather object
    '''
    return get_weather(location.lat, location.lon, lang)
