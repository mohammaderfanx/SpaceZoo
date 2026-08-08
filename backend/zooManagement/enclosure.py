from backend.animalSimulation.habits import FoodPreference
from backend.animalSimulation.animal import Animal
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
