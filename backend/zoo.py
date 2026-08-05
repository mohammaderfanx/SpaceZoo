from typing import List

from backend.animal_old import Animal
from employee import Employee
from inventory import Inventory
from visitor import Visitor

class Zoo:
    def __init__(self):
        self.budget = 100
        self.animals: List[Animal] = []
        self.staff: List[Employee] = []
        self.visitors: List[Visitor] = []
        self.inventory: Inventory

