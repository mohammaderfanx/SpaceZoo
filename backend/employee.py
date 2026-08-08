from typing import Any
from animal import Animal


class WorkingHours:

    def __init__(self, startOfShift: int, endOfShift: int):
        self.startOfShift = startOfShift
        self.endOfShift = endOfShift


class Employee:

    def __init__(self, id: str, name: str, workingHours: WorkingHours, salary: int = 10):
        self.id = id
        self.name = name
        self.workingHours = workingHours
        self.salary = salary 

    def isOnShift(self, elapsedHours: int):
        if self.workingHours.startOfShift < self.workingHours.endOfShift:
            if elapsedHours >= self.workingHours.startOfShift and elapsedHours < self.workingHours.endOfShift:
                return True
            else:
                return False
        else:
            if elapsedHours >= self.workingHours.startOfShift or elapsedHours < self.workingHours.endOfShift:
                return True
            else:
                return False
        
    
    
class Caretaker(Employee):

    def __init__(self, id: str, name: str, workingHours: WorkingHours):
        super().__init__(id, name, workingHours, salary = 10)

    def feedAnimal(self, animal: Animal, percentHungerQuelled: float):
        animal.feed(percentHungerQuelled)
        """Tier füttern"""



class Vet(Employee):

    def __init__(self, id: str, name: str, workingHours: WorkingHours):
        super().__init__(id, name, workingHours, salary = 10)

    def healAnimal(self, animal: Animal):
        """Tier heilen"""


class Cashier(Employee):

    def __init__(self, id: str, name: str, workingHours: WorkingHours):
        super().__init__(id, name, workingHours, salary = 10)

    def sellTicket(self):
        """Ticket verkaufen"""


