"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""

from abc import ABC, abstractmethod

from backend.animalSimulation.animal import Animal
from backend.zooManagement.enclosure import Enclosure


class WorkingHours:
    """Represents an employee's daily shift start and end hours."""

    def __init__(self, startOfShift: int, endOfShift: int):
        self.startOfShift = startOfShift
        self.endOfShift = endOfShift


class Employee(ABC):
    """Abstract base class for zoo staff with shared identity and shift behavior."""

    def __init__(self, name: str, workingHours: WorkingHours, salary: int = 10, x: int = 0, y: int = 0):
        self.id = name
        self.name = name
        self.workingHours = workingHours
        self.salary = salary
        self.busyFor: int = 0
        self.x: int = x
        self.y: int = y
        self.status: str = "Idle"

    def isOnShift(self, elapsedHours: int | None = None) -> bool:
        """Returns whether the employee is on shift at the specified hour.

        Args:
            elapsedHours: Optional current hour of the simulation day.

        Returns:
            bool: True when the employee is working.

        Tests:
            shift does not cross midnight, hour inside range -> returns True
            shift does not cross midnight, hour outside range -> returns False
            shift crosses midnight, hour inside wrapped range -> returns True
            shift crosses midnight, hour outside wrapped range -> returns False
        """
        if elapsedHours is None:
            return True
        if self.workingHours.startOfShift < self.workingHours.endOfShift:
            return self.workingHours.startOfShift <= elapsedHours < self.workingHours.endOfShift
        return elapsedHours >= self.workingHours.startOfShift or elapsedHours < self.workingHours.endOfShift

    def to_dict(self) -> dict:
        """Serializes the employee state into a dictionary for UI consumption.

        Returns:
            dict: Employee state with ID, name, type, status, salary, and position.

        Tests:
            employee with position -> dictionary includes position tuple
            employee salary set -> dictionary records salary
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
            "status": self.status,
            "salary": self.salary,
            "position": (self.x, self.y),
        }

    @abstractmethod
    def performDuty(self, target: object) -> None:
        """Performs a role-specific duty on a target object."""
        raise NotImplementedError()


class Caretaker(Employee):
    """Employee responsible for feeding and cleaning enclosures."""

    def __init__(self, name: str, workingHours: WorkingHours):
        super().__init__(name, workingHours, salary=10)

    def feedAnimal(self, animal: Animal, percentHungerQuelled: float) -> None:
        """Feeds the given animal and marks the caretaker busy.

        Args:
            animal: the animal to feed
            percentHungerQuelled: fraction of hunger satisfied

        Tests:
            healthy animal receives feed -> saturation increases
            busy caretaker still performs duty and busyFor increments
        """
        animal.feed(percentHungerQuelled)
        self.busyFor += 1

    def cleanEnclosure(self, enclosure: Enclosure) -> None:
        """Cleans the enclosure and marks the caretaker busy."""
        enclosure.getCleaned()
        self.busyFor += 1

    def performDuty(self, target: object) -> None:
        """Performs a duty on an enclosure or animal target."""
        if isinstance(target, Animal):
            self.feedAnimal(target, 1.0)
        elif isinstance(target, Enclosure):
            self.cleanEnclosure(target)


class Vet(Employee):
    """Employee responsible for healing sick animals."""

    def __init__(self, name: str, workingHours: WorkingHours):
        super().__init__(name, workingHours, salary = 10)

    def healAnimal(self, animal: Animal):
        """Heals the given animal, occupying the vet for one tick.

        Args:
            self
            animal: the animal being healed

        Returns:
            None

        Tests:
            called on a free vet -> busyFor increases by 1
            called repeatedly -> busyFor keeps incrementing
        """
        self.busyFor += 1

    def performDuty(self, target: object) -> None:
        """Perform a vet duty on a sick animal target."""
        if isinstance(target, Animal):
            self.healAnimal(target)


class Cashier(Employee):
    """Employee responsible for selling tickets to visitors."""

    def __init__(self, name: str, workingHours: WorkingHours):
        super().__init__(name, workingHours, salary = 10)

    def sellTicket(self):
        """Sells a ticket to a visitor.

        Args:
            self

        Tests:
            visitor buys a ticket -> visitor count and budget increase
            no visitor present -> no-op
        """
        self.busyFor += 1

    def performDuty(self, target: object) -> None:
        """Perform cashier duty by selling a ticket."""
        self.sellTicket()

