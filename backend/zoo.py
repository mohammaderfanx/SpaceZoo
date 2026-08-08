from typing import List

from backend.animal import Animal
from employee import Employee, Caretaker, Vet, Cashier
from inventory import Inventory
from enclosure import Enclosure
from egg import Egg

class Zoo:
    def __init__(self):
        self.budget = 100
        self.animals: List[Animal] = []
        self.staff: List[Employee] = []
        self.enclosures: List[Enclosure] = []
        self.visitors: int = 0
        self.inventory: Inventory
        self.eggs: List[Egg] = []

    def getEmployeesByType(self, typeOfEmployee: type[Employee]):
            availableEmployees: List[Employee] = []
            for employee in self.staff:
                        if employee.__class__() == typeOfEmployee:
                            if employee.isOnShift():
                                availableEmployees.append(employee)
            return availableEmployees

    
    def getCaretakers(self) -> List[Caretaker]:
        return self.getEmployeesByType(Caretaker)

    def getVets(self) -> List[Vet]:
            return self.getEmployeesByType(Vet)

    def getCashiers(self) -> List[Cashier]:
            return self.getEmployeesByType(Cashier)

    def animalDies(self, animal: Animal):
          """stirbt und kommt weg"""

    def buyNewAnimal(self):
          """kriegst ne Auswahl an allen bekannten Typen"""

    def sellAnimal(self):
          """verkaufts ein gewähltes Tier"""

    def buyFood(self):
          """Auswahl an Items, kommt ins Inventory"""

    def buyMedicine(self):
          """Auswahl an Items, kommt ins Inventory"""

    def healAnimal(self, animal: Animal):
          """Auswahl an kranken Tieren, nutzt passende Medizin, wahrscheinlichkeit auf Erfolg hängt von Lethality der Krankheit ab"""
