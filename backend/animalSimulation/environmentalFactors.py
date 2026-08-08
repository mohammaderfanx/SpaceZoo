"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""

from enum import Enum

class Weather(Enum):
    """Possible weather conditions in the zoo."""

    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"


class EnvironmentalFactors:
    """Current weather and climate conditions, used to compute visitor attractiveness."""

    def __init__(self, temperature: int = 25, windSpeed: int = 40, weather: Weather = Weather.SUNNY):
        self.temperature = temperature
        self.windSpeed = windSpeed
        self.weather = weather

    def getVisitorAttractiveness(self) -> float:
        """Computes overall visitor attractiveness from weather, wind, and temperature."""
        #switch case
        weatherCoefficient = self.__getWeatherCoefficient()
        windSpeedCoefficient = self.__getWindSpeedCoefficient()
        temperatureCoefficient = self.__getTemperatureCoefficient()
        return weatherCoefficient * windSpeedCoefficient * temperatureCoefficient

    def __getWeatherCoefficient(self) -> float:
        """Returns the attractiveness coefficient for the current weather."""
        weatherCoefficient: float
        if self.weather == Weather.SUNNY:
            weatherCoefficient = 1.5
        elif self.weather == Weather.CLOUDY:
            weatherCoefficient = 1
        else:
            weatherCoefficient = 0.5
        return weatherCoefficient


    def __getWindSpeedCoefficient(self) -> float:
        """Returns the attractiveness coefficient for the current wind speed."""
        if self.windSpeed < 50:
            return 1
        return 0.3 # toooo windy for noobs

    
    def __getTemperatureCoefficient(self) -> float:
        """Returns the attractiveness coefficient for the current temperature.

        Args:
            self

        Returns:
            float: temperature coefficient deciding the environment's influence on the visitor score
        
        Tests:
            deviationFromOptimum is 0 (division by 0) -> prevented, returns optimal coefficient
            deviation positive -> returns non-optimal coefficient
            deviation negative -> returns same non-optomal coefficient as positive case
            deviation huge -> coefficient never drops below 0.5
        """
        deviationFromOptimum = abs(self.temperature - 25)
        if deviationFromOptimum == 0:
            return 1.5
        elif deviationFromOptimum < 5:
            return 1
        else:
            return 0.5


