from backend.animal_old import AnimalType, Animal
from itertools import count
from typing import List




class Enclosure:
    _number_counter = count(1)

    def __init__(self, capacity, typeOfAnimal: AnimalType):
        self.number = next(Enclosure._number_counter)
        self.capacity = capacity
        self.typeOfAnimal = typeOfAnimal
        self.animals: List[Animal] = []
