"""Minimal text-based interface for the DinoZoo backend simulation.

Run with: python simple_interface/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.core.simulationEngine import SimulationEngine
from backend.animalSimulation.animal import Eagle, Wolf, Rabbit, Gender
from backend.animalSimulation.habits import FoodPreference
from backend.zooManagement.employee import Caretaker, Vet, Cashier, WorkingHours
from backend.zooManagement.food import Meat, Hay, Fish
from backend.zooManagement.medicine import Antibiotic
from backend.zooManagement.enclosure import Enclosure

ANIMALS = {"1": Eagle, "2": Wolf, "3": Rabbit}
EMPLOYEES = {"1": Caretaker, "2": Vet, "3": Cashier}
FOODS = {"1": Meat, "2": Hay, "3": Fish}
DIETS = {"1": FoodPreference.CARNIVORE, "2": FoodPreference.HERBIVORE, "3": FoodPreference.OMNIVORE}


def print_status(engine: SimulationEngine) -> None:
    zoo = engine.zoo
    print(f"\nDay {engine.elapsedDays}, Hour {engine.elapsedHours} | Budget: {zoo.budget} | "
          f"Visitors: {zoo.visitors} | Score: {zoo.score:.2f}")

    print(f"Animals ({len(zoo.animals)}):")
    for animal in zoo.animals:
        sick = " [sick]" if animal.illness else ""
        print(f"  - {animal.name} ({animal.species}) health={animal.health:.2f} "
              f"hunger={animal.get_hunger_percent():.0f}%{sick}")

    print(f"Staff ({len(zoo.staff)}):")
    for employee in zoo.staff:
        print(f"  - {employee.name} ({employee.__class__.__name__}) {employee.status}")

    print(f"Enclosures ({len(zoo.enclosures)}):")
    for enclosure in zoo.enclosures:
        print(f"  - #{enclosure.number} {enclosure.typeOfAnimal.value} "
              f"cleanliness={enclosure.cleanliness:.2f} "
              f"({len(enclosure.animals)}/{enclosure.capacity})")


def prompt_int(label: str, default: int = 0) -> int:
    raw = input(f"{label}: ").strip()
    return int(raw) if raw else default


def buy_animal(engine: SimulationEngine) -> None:
    print("Species: 1) Eagle  2) Wolf  3) Rabbit")
    animal_cls = ANIMALS.get(input("> ").strip())
    if not animal_cls:
        print("Invalid choice.")
        return
    name = input("Name: ").strip() or "Unnamed"
    gender = Gender.FEMALE if input("Gender (f/m): ").strip().lower() == "f" else Gender.MALE

    before = len(engine.zoo.animals)
    engine.zoo.buyNewAnimal(animal_cls, name, engine.elapsedDays, gender)
    if len(engine.zoo.animals) == before:
        print("Not enough budget.")
    else:
        print(f"Bought {name} the {animal_cls.__name__}.")


def add_enclosure(engine: SimulationEngine) -> None:
    print("Diet: 1) Carnivore  2) Herbivore  3) Omnivore")
    diet = DIETS.get(input("> ").strip())
    if not diet:
        print("Invalid choice.")
        return
    capacity = prompt_int("Capacity", 5)
    engine.zoo.enclosures.append(Enclosure(capacity, diet))
    print("Enclosure added.")


def hire_employee(engine: SimulationEngine) -> None:
    print("Role: 1) Caretaker  2) Vet  3) Cashier")
    employee_cls = EMPLOYEES.get(input("> ").strip())
    if not employee_cls:
        print("Invalid choice.")
        return
    name = input("Name: ").strip() or "Unnamed"
    start = prompt_int("Shift start hour (0-23)", 8)
    end = prompt_int("Shift end hour (0-23)", 16)

    before = len(engine.zoo.staff)
    engine.zoo.hireEmployee(employee_cls, name, WorkingHours(start, end))
    if len(engine.zoo.staff) == before:
        print("Could not hire (invalid data).")
    else:
        print(f"Hired {name} as {employee_cls.__name__}.")


def buy_food(engine: SimulationEngine) -> None:
    print("Food: 1) Meat  2) Hay  3) Fish")
    food_cls = FOODS.get(input("> ").strip())
    if not food_cls:
        print("Invalid choice.")
        return
    weight = prompt_int("Weight in kg", 10)

    before = len(engine.zoo.inventory.food)
    engine.zoo.buyFood(food_cls, weight, engine.elapsedDays)
    if len(engine.zoo.inventory.food) == before:
        print("Not enough budget.")
    else:
        print(f"Bought {weight}kg of {food_cls.__name__}.")


def buy_medicine(engine: SimulationEngine) -> None:
    quantity = prompt_int("Quantity of Antibiotic", 1)
    before = len(engine.zoo.inventory.medicine)
    engine.zoo.buyMedicine(Antibiotic(), quantity)
    if len(engine.zoo.inventory.medicine) == before:
        print("Not enough budget.")
    else:
        print(f"Bought {quantity} Antibiotic.")


def heal_animal(engine: SimulationEngine) -> None:
    sick_animals = [animal for animal in engine.zoo.animals if animal.illness is not None]
    if not sick_animals:
        print("No sick animals.")
        return
    for index, animal in enumerate(sick_animals):
        print(f"  {index}) {animal.name} ({animal.species})")
    choice = prompt_int("Choose animal", -1)
    if not (0 <= choice < len(sick_animals)):
        print("Invalid choice.")
        return
    if engine.zoo.healAnimal(sick_animals[choice]):
        print("Animal healed.")
    else:
        print("No matching medicine in stock.")


MENU = """
=== DinoZoo ===
1) Advance time now (time also advances automatically)
2) Buy animal
3) Add enclosure
4) Hire employee
5) Buy food
6) Buy medicine
7) Heal animal
8) Show status
0) Quit
"""

ACTIONS = {
    "2": buy_animal,
    "3": add_enclosure,
    "4": hire_employee,
    "5": buy_food,
    "6": buy_medicine,
    "7": heal_animal,
}


def main() -> None:
    engine = SimulationEngine()
    print_status(engine)
    engine.start()

    try:
        while True:
            print(MENU)
            choice = input("> ").strip()

            if choice == "0":
                break
            elif choice == "1":
                engine.tick_once()
                print_status(engine)
            elif choice == "8":
                print_status(engine)
            elif choice in ACTIONS:
                ACTIONS[choice](engine)
            else:
                print("Invalid choice.")
    finally:
        engine.stop()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
