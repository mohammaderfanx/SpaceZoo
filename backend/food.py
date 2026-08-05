from backend.animal_old import AnimalType
from typing import List

class Food:
    def __init__(self, name: str, animalTypes: List[AnimalType], shelfLife: int, pricePerKg: int):
        self.name = name
        self.animalTypes = animalTypes
        self.shelfLife = shelfLife
        self.pricePerKg = pricePerKg


class Meat(Food):
    def __init__(self):
        super().__init__("Meat", [AnimalType.CARNIVORE], 10, 3)

class Hay(Food):
    def __init__(self):
        super().__init__("Hay", [AnimalType.HERBIVORE], 25, 1)

class Fish(Food):
    def __init__(self):
        super().__init__("Fish", [AnimalType.CARNIVORE], 7, 5)



class FoodItem:
    def __init__(self, type: Food, weight: int, elapsedDays: int):
        self.type = type
        self.weight = weight
        self.bestBefore = elapsedDays + self.type.shelfLife
        self.price = self.type.pricePerKg * self.weight

