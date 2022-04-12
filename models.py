class Location:

    def __init__(self, lat: float, lon: float, city: str):
        self.lat = lat
        self.lon = lon
        self.city = city


class WeatherDescription:

    def __init__(self, main, description, icon):
        # Use is in case of we have the weather description list loaded into our DB
        # self.id = id
        self.main = main
        self.description = description
        self.icon = icon


class WeatherTemperature:

    def __init__(self, temp, temp_min, temp_max, unit, feels_like):
        self.temp = temp
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.unit = unit
        self.feels_like = feels_like


class WeatherWind:

    def __init__(self, speed, deg, gust):
        self.speed = speed
        self.deg = deg
        self.gust = gust


class Weather:

    def __init__(self, description: list[WeatherDescription], temperature: WeatherTemperature, wind: WeatherWind,
                 location: Location,
                 lang):
        self.weather = description
        self.temperature = temperature
        self.location = location
        self.wind = wind
        self.lang = lang
