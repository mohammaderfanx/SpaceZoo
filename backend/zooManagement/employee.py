
from backend.animalSimulation.animal import Animal


class WorkingHours:
    """Start and end hour of an employee's daily shift."""

    def __init__(self, startOfShift: int, endOfShift: int):
        self.startOfShift = startOfShift
        self.endOfShift = endOfShift


class Employee:
    """Base class for zoo staff, tracking identity, shift, and busy state."""

    def __init__(self, id: str, name: str, workingHours: WorkingHours, salary: int = 10):
        self.id = id
        self.name = name
        self.workingHours = workingHours
        self.salary = salary 
        self.busyFor: int = 0

    def isOnShift(self, elapsedHours: int):
        """Returns whether the employee is working at the given hour."""
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
    """Employee responsible for feeding and cleaning up after animals."""

    def __init__(self, id: str, name: str, workingHours: WorkingHours):
        super().__init__(id, name, workingHours, salary = 10)

    def feedAnimal(self, animal: Animal, percentHungerQuelled: float):
        """Feeds the given animal by the specified hunger-quelled percentage."""
        animal.feed(percentHungerQuelled)
        busyFor += 1



class Vet(Employee):
    """Employee responsible for healing sick animals."""

    def __init__(self, id: str, name: str, workingHours: WorkingHours):
        super().__init__(id, name, workingHours, salary = 10)

    def healAnimal(self, animal: Animal):
        """Heals the given animal, occupying the vet for one tick."""
        self.busyFor += 1



class Cashier(Employee):
    """Employee responsible for selling tickets to visitors."""

    def __init__(self, id: str, name: str, workingHours: WorkingHours):
        super().__init__(id, name, workingHours, salary = 10)

    def sellTicket(self):
        """Sells a ticket to a visitor."""


