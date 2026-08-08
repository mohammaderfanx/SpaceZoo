from enum import Enum

class Weather(Enum):
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"


class environmentalFactors:

    def __init__(self):
        self.temperature: int
        self.windSpeed: int
        self.weather: Weather

    def getVisitorAttractiveness(self):
        #switch case
        weatherCoefficient = self.getWeatherCoefficient()
        windSpeedCoefficient = self.getWindSpeedCoefficient()
        temperatureCoefficient = self.getTemperatureCoefficient()
        return weatherCoefficient * windSpeedCoefficient * temperatureCoefficient

    def getWeatherCoefficient(self):
        weatherCoefficient: float
        if self.weather == Weather.SUNNY:
            weatherCoefficient = 1.5
        elif self.weather == Weather.CLOUDY:
            weatherCoefficient = 1
        else:
            weatherCoefficient = 0.5
        return weatherCoefficient


    def getWindSpeedCoefficient(self):
        if self.windSpeed < 50:
            return 1
        return 0.3 # toooo windy for noobs

    
    def getTemperatureCoefficient(self):
        deviationFromOptimum = abs(self.temperature - 25)
        if deviationFromOptimum == 0:
            return 1.5
        elif deviationFromOptimum < 5:
            return 1
        else:
            return 0.5


