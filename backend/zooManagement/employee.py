"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""

from animalSimulation.animal import Animal


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
        """Returns whether the employee is working at the given hour.

        Args:
            self
            elapsedHours: current hour of the simulation day

        Returns:
            bool: True if elapsedHours falls within the employee's shift

        Tests:
            shift does not cross midnight, hour inside range -> returns True
            shift does not cross midnight, hour outside range -> returns False
            shift crosses midnight, hour inside wrapped range -> returns True
            shift crosses midnight, hour outside wrapped range -> returns False
        """
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
        """Feeds the given animal by the specified hunger-quelled percentage.

        Args:
            self
            animal: the animal to feed
            percentHungerQuelled: fraction of the animal's hunger that gets satisfied

        Tests:
            called -> delegates to animal.feed(percentHungerQuelled)
            called -> caretaker's busyFor is incremented
        """
        animal.feed(percentHungerQuelled)
        busyFor += 1



class Vet(Employee):
    """Employee responsible for healing sick animals."""

    def __init__(self, id: str, name: str, workingHours: WorkingHours):
        super().__init__(id, name, workingHours, salary = 10)

    def healAnimal(self, animal: Animal):
        """Heals the given animal, occupying the vet for one tick.

        Args:
            self
            animal: the animal being healed

        Tests:
            called on a free vet -> busyFor increases by 1
            called repeatedly -> busyFor keeps incrementing
        """
        self.busyFor += 1



class Cashier(Employee):
    """Employee responsible for selling tickets to visitors."""

    def __init__(self, id: str, name: str, workingHours: WorkingHours):
        super().__init__(id, name, workingHours, salary = 10)

    def sellTicket(self):
        """Sells a ticket to a visitor.

        Args:
            self

        Tests:
            visitor buys a ticket -> visitor count and budget increase
            no visitor present -> no-op
        """


