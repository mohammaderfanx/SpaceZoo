"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""

from animalSimulation.habits import FoodPreference
from animalSimulation.animal import Animal
from itertools import count
from typing import List




class Enclosure:
    """A numbered habitat that houses animals of a given diet type up to a capacity."""

    _number_counter = count(1)

    def __init__(self, capacity, foodPreference: FoodPreference):
        self.number = next(Enclosure._number_counter)
        self.capacity = capacity
        self.typeOfAnimal = foodPreference
        self.animals: List[Animal] = []
        self.cleanliness: float = 1

    def getCleaned(self):
        """Enclosure cleanliness to 100%
        
        Args:
            self
        
        Returns:
            None
        
        Tests:
            enclosure is dirty -> cleanliness to 1
            enclosure is already clean -> nothing changes"""
        self.cleanliness = 1
