from backend.animal_old import AnimalType
from typing import List
from simulation_engine import get_current_day

class Food:
    def __init__(self, name: str, animalTypes: List[AnimalType], shelfLife: int, pricePerKg: int):
        self.name = name
        self.animalTypes = animalTypes
        self.shelfLife = shelfLife
        self.pricePerKg = pricePerKg



class FoodItem:
    def __init__(self, type: Food, weight: int):
        self.type = type
        self.weight = weight
        self.bestBefore = get_current_day() + self.type.shelfLife
        self.price = self.type.pricePerKg * self.weight

