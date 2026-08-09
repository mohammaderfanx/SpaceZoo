"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""


from typing import List
import statistics

from backend.animalSimulation.animal import Animal, Gender
from backend.zooManagement.employee import Employee, Caretaker, Vet, Cashier, WorkingHours
from backend.zooManagement.inventory import Inventory
from backend.zooManagement.enclosure import Enclosure
from backend.zooManagement.food import Food, FoodItem
from backend.zooManagement.medicine import Medicine, MedicineItem
from backend.animalSimulation.egg import Egg
from backend.animalSimulation.environmentalFactors import EnvironmentalFactors

class Zoo:
    """Central aggregate holding the zoo's animals, staff, enclosures, inventory, and budget, as well as environmental factors and the current visitor score."""

    def __init__(self):
        self.budget = 100
        self.animals: List[Animal] = []
        self.staff: List[Employee] = []
        self.enclosures: List[Enclosure] = []
        self.visitors: int = 0
        self.inventory: Inventory = Inventory()
        self.eggs: List[Egg] = []
        self.environment: EnvironmentalFactors = EnvironmentalFactors()
        self.score: float = 0

    def __getEmployeesByType(self, typeOfEmployee: type[Employee], elapsedHours: int | None = None):
            """Returns staff of the given type who are on shift and not busy.

            Args:
                self
                typeOfEmployee: the Employee subclass to filter by
                elapsedHours: current hour used to check whether the employee is on shift

            Returns:
                list: matching employees currently on shift and free

            Tests:
                matching employees on shift and free -> included in result
                matching employees off shift or busy -> excluded from result
            """
            return [employee for employee in self.staff if isinstance(employee, typeOfEmployee) and employee.isOnShift(elapsedHours) and employee.busyFor == 0]

    def getCaretakers(self, elapsedHours: int | None = None) -> List[Caretaker]:
        """Returns all available caretakers.

        Args:
            self
            elapsedHours: Optional current hour used to check whether the caretaker is on shift.

        Returns:
            List[Caretaker]: caretakers currently on shift and free

        Tests:
            caretakers on shift and free -> included in result
            caretakers off shift or busy -> excluded from result
        """
        return self.__getEmployeesByType(Caretaker, elapsedHours)

    def getVets(self, elapsedHours: int | None = None) -> List[Vet]:
            """Returns all available vets.

            Args:
                self
                elapsedHours: Optional current hour used to check whether the vet is on shift.

            Returns:
                List[Vet]: vets currently on shift and free

            Tests:
                vets on shift and free -> included in result
                vets off shift or busy -> excluded from result
            """
            return self.__getEmployeesByType(Vet, elapsedHours)

    def getCashiers(self, elapsedHours: int | None = None) -> List[Cashier]:
            """Returns all available cashiers.

            Args:
                self
                elapsedHours: Optional current hour used to check whether the cashier is on shift.

            Returns:
                List[Cashier]: cashiers currently on shift and free

            Tests:
                cashiers on shift and free -> included in result
                cashiers off shift or busy -> excluded from result
            """
            return self.__getEmployeesByType(Cashier, elapsedHours)

    def animalDies(self, animal: Animal):
        """Removes the given animal from the zoo and from any enclosure it occupied.

        Args:
            self
            animal: the animal that died

        Tests:
            animal is in self.animals -> it gets removed and its enclosure membership ends
            animal not in self.animals -> raises ValueError
        """
        self.animals.remove(animal)
        for enclosure in self.enclosures:
            if animal in enclosure.animals:
                enclosure.animals.remove(animal)

    def __findCompatibleEnclosure(self, animal: Animal) -> Enclosure | None:
        """Finds an enclosure compatible with the animal's diet and room availability."""
        for enclosure in self.enclosures:
            if len(enclosure.animals) < enclosure.capacity and enclosure.typeOfAnimal == animal.habits.eatingHabit.foodPreference:
                return enclosure
        return None

    def addAnimal(self, animal: Animal):
        """Adds an animal to the zoo and assigns it to a compatible enclosure."""
        enclosure = self.__findCompatibleEnclosure(animal)
        if enclosure is None:
            return {"success": False, "message": "No suitable enclosure available."}
        self.animals.append(animal)
        enclosure.animals.append(animal)
        return {"success": True, "message": f"Added {animal.name} to enclosure {enclosure.number}."}

    def buyNewAnimal(self, animalType: type[Animal], name: str, birthdate: int, gender: Gender):
        """Buys an animal with given species, gender and name.

        Args:
            self
            animalType: the Animal subclass to buy, carrying its purchase price as a class attribute
            name: name for the new animal
            birthdate: day that the animal was born, determines age
            gender: gender of the new animal

        Tests:
            budget covers the chosen animal -> animal is added to the zoo
            budget insufficient -> purchase is rejected
        """
        newAnimal = animalType(name, birthdate, gender)
        if self.budget < newAnimal.price:
            return {"success": False, "message": "Not enough budget."}
        result = self.addAnimal(newAnimal)
        if not result["success"]:
            return result
        self.budget -= newAnimal.price
        return {"success": True, "message": f"Bought {newAnimal.species}."}

    def sellAnimal(self, animal: Animal):
          """Sells a chosen animal.

          Args:
              self
              animal: the animal to sell

          Tests:
              chosen animal exists in the zoo -> animal is removed and budget increases
              no animal selected -> no-op
          """
          if animal not in self.animals:
              return {"success": False, "message": "Animal not found."}
          self.budget += animal.price // 2
          self.animals.remove(animal)
          for enclosure in self.enclosures:
              if animal in enclosure.animals:
                  enclosure.animals.remove(animal)
                  break
          return {"success": True, "message": f"Sold {animal.name}."}

    def hireEmployee(self, employeeType: type[Employee], name: str, workingHours: WorkingHours):
         """Hires a new employee.

         Args:
             self
             employeeType: the Employee subclass to hire
             name: name of the new employee
             workingHours: the new employee's shift hours

         Tests:
             valid employee data provided -> employee is added to staff
             invalid employee data -> hire is rejected
         """
         if not name:
             return {"success": False, "message": "Invalid name."}
         if not (0 <= workingHours.startOfShift <= 23) or not (0 <= workingHours.endOfShift <= 23):
             return {"success": False, "message": "Invalid shift hours."}
         if self.budget < 10:
             return {"success": False, "message": "Not enough budget."}
         self.staff.append(employeeType(name, workingHours))
         self.budget -= 10
         return {"success": True, "message": f"Hired {name}."}

    def buyFood(self, foodType: type[Food], weight: int, elapsedDays: int):
          """Buys chosen food items and adds them to the inventory.

          Args:
              self
              foodType: the Food subclass to buy
              weight: kilograms to buy
              elapsedDays: number of full days elapsed in the simulation, used to compute the food's expiry

          Tests:
              budget covers the chosen food -> items are added to inventory
              budget insufficient -> purchase is rejected
          """
          foodInstance = foodType()
          totalPrice = foodInstance.pricePerKg * weight
          if self.budget < totalPrice:
              return {"success": False, "message": "Not enough budget."}
          self.budget -= totalPrice
          self.inventory.food.append(FoodItem(foodInstance, weight, elapsedDays))
          return {"success": True, "message": f"Bought {weight}kg {foodInstance.name}."}

    def buyMedicine(self, medicine: Medicine, quantity: int):
          """Buys chosen medicine items and adds them to the inventory.

          Args:
              self
              medicine: the medicine to buy
              quantity: number of units to buy

          Tests:
              budget covers the chosen medicine -> items are added to inventory
              budget insufficient -> purchase is rejected
          """
          totalPrice = medicine.price * quantity
          if self.budget < totalPrice:
              return {"success": False, "message": "Not enough budget."}
          self.budget -= totalPrice
          for _ in range(quantity):
              self.inventory.medicine.append(MedicineItem(medicine, 1))
          return {"success": True, "message": f"Bought {quantity}x {medicine.name}."}

    def healAnimal(self, animal: Animal):
        """Heals the given animal by consuming matching medicine from inventory.

        Args:
            animal: the animal to heal

        Returns:
            dict: operation success and a descriptive message

        Tests:
            animal has no illness -> returns success False and inventory is unchanged
            matching medicine in stock -> illness is removed and medicine consumed
            no matching medicine in stock -> returns success False
        """
        if animal.illness is None:
            return {"success": False, "message": "Animal is not sick."}

        matching_medicine = [item for item in self.inventory.medicine if type(item.type.illness) == type(animal.illness)]
        if not matching_medicine:
            return {"success": False, "message": "No matching medicine in inventory."}

        self.inventory.medicine.remove(matching_medicine[0])
        animal.illness = None
        animal.health = min(1.0, animal.health + 0.3)
        return {"success": True, "message": f"Healed {animal.name}."}
       
