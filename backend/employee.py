from typing import Any
from animal import Animal
from visitor import Visitor

class Employee:

    def __init__(self, id: str, name: str, salary: int = 10):
        self.id = id
        self.name = name
        self.salary = salary 
    
    
class Caretaker(Employee):

    def __init__(self, id: str, name: str):
        super().__init__(id, name, salary = 10)

    def feedAnimal(self, animal: Animal):
        """Tier füttern"""



class Vet(Employee):

    def __init__(self, id: str, name: str):
        super().__init__(id, name, salary = 10)

    def healAnimal(self, animal: Animal):
        """Tier heilen"""


class Cashier(Employee):

    def __init__(self, id: str, name: str):
        super().__init__(id, name, salary = 10)

    def sellTicket(self, visitor: Visitor):
        """Ticket verkaufen"""
