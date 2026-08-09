"""
Facade layer for SpaceZoo.

This class provides the only bridge between frontend and backend logic.
It exposes native Python data structures only and hides backend implementation
details behind a simple UI-friendly API.
"""

from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Tuple

from backend.core.simulationEngine import SimulationEngine
from backend.animalSimulation.animal import Eagle, Wolf, Rabbit, Gender
from backend.animalSimulation.habits import FoodPreference
from backend.zooManagement.employee import Caretaker, Vet, Cashier, WorkingHours
from backend.zooManagement.enclosure import Enclosure
from backend.zooManagement.food import Meat, Hay, Fish
from backend.zooManagement.medicine import Antibiotic
from database.db_manager import DatabaseManager


class SpaceZooAPI:
    """Facade for the SpaceZoo game logic exposed to the frontend."""

    SPECIES_MAP = {
        "Eagle": Eagle,
        "Wolf": Wolf,
        "Rabbit": Rabbit,
    }

    FOOD_MAP = {
        "Meat": Meat,
        "Hay": Hay,
        "Fish": Fish,
    }

    STAFF_MAP = {
        "Caretaker": Caretaker,
        "Vet": Vet,
        "Cashier": Cashier,
    }

    MEDICINE_MAP = {
        "Antibiotic": Antibiotic,
    }

    def __init__(self) -> None:
        self.db = DatabaseManager()
        self.sim = SimulationEngine()
        self.tick_accumulator = 0.0
        self.player_position = (10, 8)
        self._initialize_demo_zoo()

    def _initialize_demo_zoo(self) -> None:
        # Create enclosures for different diet groups
        herbivore_enclosure = Enclosure(6, FoodPreference.HERBIVORE)
        carnivore_enclosure = Enclosure(4, FoodPreference.CARNIVORE)
        omnivore_enclosure = Enclosure(5, FoodPreference.OMNIVORE)

        self.sim.zoo.enclosures.extend([
            herbivore_enclosure,
            carnivore_enclosure,
            omnivore_enclosure,
        ])

        # Seed a starter roster using only the species defined in backend/.
        demo_animals = [
            (Rabbit("Rabbit-1", 0, Gender.FEMALE), herbivore_enclosure),
            (Rabbit("Rabbit-2", 0, Gender.FEMALE), herbivore_enclosure),
            (Wolf("Wolf-1", 0, Gender.MALE), carnivore_enclosure),
            (Eagle("Eagle-1", 0, Gender.FEMALE), omnivore_enclosure),
            (Eagle("Eagle-2", 0, Gender.MALE), omnivore_enclosure),
        ]

        for animal, enclosure in demo_animals:
            self.sim.zoo.animals.append(animal)
            enclosure.animals.append(animal)

        # Add staff for feeding and ticket sales
        caretaker = Caretaker("Mira", WorkingHours(8, 18))
        cashier = Cashier("Noah", WorkingHours(8, 18))
        vet = Vet("Lina", WorkingHours(9, 17))

        self.sim.zoo.staff.extend([caretaker, cashier, vet])

        # Add initial food stock
        self.sim.zoo.buyFood(Hay, 12, self.sim.elapsedDays)
        self.sim.zoo.buyFood(Meat, 8, self.sim.elapsedDays)
        self.sim.zoo.buyFood(Fish, 4, self.sim.elapsedDays)

        # Prime the score from environment and enclosures
        self.sim.zoo.score = self.sim.calculateVisitorScore()

    def _normalize_animal_positions(self) -> None:
        for index, animal in enumerate(self.sim.zoo.animals):
            if animal.x == 0 and animal.y == 0:
                animal.x = index % 21
                animal.y = (index // 21) % 16

    def _get_day_phase(self) -> str:
        hour = self.sim.elapsedHours
        return "Day" if 6 <= hour < 18 else "Night"

    def tick(self, delta_time: float) -> Dict[str, Any]:
        """Advance the simulation by accumulated real-world seconds.

        Args:
            delta_time: Real seconds elapsed since the last tick call.

        Returns:
            dict: Outcome including tick count and current simulation time.

        Tests:
            delta_time less than tick interval -> returns zero ticks executed
            delta_time greater than tick interval -> executes one or more ticks
        """
        self.tick_accumulator += delta_time
        ticks_executed = 0
        while self.tick_accumulator >= self.sim.secondsPerTick:
            self.sim.tick_once()
            self.tick_accumulator -= self.sim.secondsPerTick
            ticks_executed += 1
        return {
            "success": True,
            "ticks_executed": ticks_executed,
            "elapsed_days": self.sim.elapsedDays,
            "elapsed_hours": self.sim.elapsedHours,
        }

    def advance_tick(self) -> Dict[str, Any]:
        """Advance the simulation by a single discrete tick.

        Returns:
            dict: Outcome including the updated simulation time.

        Tests:
            always advances simulation by one tick
        """
        self.sim.tick_once()
        return {
            "success": True,
            "elapsed_days": self.sim.elapsedDays,
            "elapsed_hours": self.sim.elapsedHours,
        }

    def get_zoo_state(self) -> Dict[str, Any]:
        """Return the complete simulation state in plain Python data structures.

        Returns:
            dict: Full zoo state including animals, staff, enclosures, inventory, environment, and map metadata.

        Tests:
            returns a dictionary with keys 'animals', 'staff', 'enclosures', and 'environment'
            animals include age, health, hunger, and position information
        """
        self._normalize_animal_positions()
        animals = []
        for animal in self.sim.zoo.animals:
            age_days = animal.get_age_days(self.sim.elapsedDays)
            animals.append({
                "id": animal.id,
                "species": animal.species,
                "name": animal.name,
                "age_days": age_days,
                "age_stage": self._get_age_stage(animal, age_days),
                "lifespan_days": int(animal.lifecycle.seniorPhase.endOfPhaseAge),
                "health": float(animal.health),
                "hunger": float(animal.get_hunger_percent()),
                "energy": float(animal.energy),
                "is_sick": animal.illness is not None,
                "awake": animal.awake,
                "position": (animal.x, animal.y),
                "gender": animal.gender.value,
            })

        staff = [
            {
                "id": member.id,
                "name": member.name,
                "type": member.__class__.__name__,
                "status": member.status,
                "salary": member.salary,
                "working_hours": (member.workingHours.startOfShift, member.workingHours.endOfShift),
            }
            for member in self.sim.zoo.staff
        ]
        enclosures = [
            {
                "number": enclosure.number,
                "capacity": enclosure.capacity,
                "cleanliness": float(enclosure.cleanliness),
                "animal_count": len(enclosure.animals),
                "diet": enclosure.typeOfAnimal.value if hasattr(enclosure.typeOfAnimal, "value") else str(enclosure.typeOfAnimal),
            }
            for enclosure in self.sim.zoo.enclosures
        ]

        inventory_items = {}
        for item in self.sim.zoo.inventory.food:
            name = item.type.name
            inventory_items[name] = inventory_items.get(name, 0) + item.weight

        return {
            "money": int(self.sim.zoo.budget),
            "time": {
                "elapsed_days": self.sim.elapsedDays,
                "elapsed_hours": self.sim.elapsedHours,
                "day_phase": self._get_day_phase(),
            },
            "score": float(self.sim.zoo.score),
            "visitors": int(self.sim.zoo.visitors),
            "animals": animals,
            "staff": staff,
            "enclosures": enclosures,
            "inventory": inventory_items,
            "environment": {
                "temperature": int(self.sim.zoo.environment.temperature),
                "windSpeed": int(self.sim.zoo.environment.windSpeed),
                "weather": self.sim.zoo.environment.weather.name,
                "attractiveness": float(self.sim.zoo.environment.getVisitorAttractiveness()),
            },
            "player": {
                "position": self.player_position,
            },
            "map": {
                "grid_width": 21,
                "grid_height": 16,
                "tile_size": 60,
                "tiles": [[{"type": "floor", "walkable": True} for _ in range(21)] for _ in range(16)],
            },
        }

    def get_quick_stats(self) -> Dict[str, Any]:
        """Return high-level KPI values for the frontend dashboard.

        Returns:
            dict: Quick statistics including budget, visitor count, creature count, and time of day.

        Tests:
            returns correct creature count from the zoo state
            returns current day_phase and elapsed_hours values
        """
        state = self.get_zoo_state()
        return {
            "money": state["money"],
            "visitor_count": state["visitors"],
            "creature_count": len(state["animals"]),
            "day_phase": state["time"]["day_phase"],
            "time_of_day": state["time"]["elapsed_hours"],
        }

    def _get_age_stage(self, animal: Any, age_days: int) -> int:
        lifespan = max(1, getattr(animal.lifecycle.seniorPhase, "endOfPhaseAge", 1))
        capped_age = min(age_days, lifespan - 1)
        stage = capped_age * 3 // lifespan + 1
        return min(3, max(1, stage))

    def get_panel_state(self) -> Dict[str, Any]:
        """Return a state slice optimized for UI panel rendering.

        Returns:
            dict: Summary of money, visitors, score, animals, staff, enclosures, inventory, and environment.

        Tests:
            includes the expected dashboard keys
            derived values match get_zoo_state output
        """
        state = self.get_zoo_state()
        return {
            "money": state["money"],
            "visitors": state["visitors"],
            "score": state["score"],
            "elapsed_days": state["time"]["elapsed_days"],
            "elapsed_hours": state["time"]["elapsed_hours"],
            "day_phase": state["time"]["day_phase"],
            "animals": state["animals"],
            "staff": state["staff"],
            "enclosures": state["enclosures"],
            "inventory": state["inventory"],
            "environment": state["environment"],
        }

    def buy_animal(self, species: str) -> Dict[str, Any]:
        """Purchase a new animal of the requested species if the zoo has sufficient budget.

        Args:
            species: species name matching the available species map.

        Returns:
            dict: success flag and descriptive message.

        Tests:
            valid species with enough budget -> returns success True
            invalid species -> returns success False
        """
        if species not in self.SPECIES_MAP:
            return {"success": False, "message": "Unknown species."}
        animal_cls = self.SPECIES_MAP[species]
        gender = random.choice([Gender.FEMALE, Gender.MALE])
        name = f"{species}_{random.randint(1000,9999)}"
        new_animal = animal_cls(name, self.sim.elapsedDays, gender)
        if self.sim.zoo.budget < new_animal.price:
            return {"success": False, "message": "Not enough money."}
        self.sim.zoo.buyNewAnimal(animal_cls, name, self.sim.elapsedDays, gender)
        return {"success": True, "message": f"Bought {species}."}

    def buy_food(self, food_type: str, weight: int = 5) -> Dict[str, Any]:
        """Purchase food of a given type and weight if the zoo has sufficient budget.

        Args:
            food_type: food type name matching the available food map.
            weight: amount of food to buy in kilograms.

        Returns:
            dict: success flag and descriptive message.

        Tests:
            valid food type with enough budget -> returns success True
            invalid food type -> returns success False
        """
        if food_type not in self.FOOD_MAP:
            return {"success": False, "message": "Unknown food type."}
        food_cls = self.FOOD_MAP[food_type]
        if self.sim.zoo.budget < food_cls().pricePerKg * weight:
            return {"success": False, "message": "Not enough money."}
        self.sim.zoo.buyFood(food_cls, weight, self.sim.elapsedDays)
        return {"success": True, "message": f"Bought {weight}kg {food_type}."}

    def buy_medicine(self, medicine_type: str, quantity: int = 1) -> Dict[str, Any]:
        """Purchase medicine items and add them to the zoo inventory.

        Args:
            medicine_type: medicine type name matching the available medicine map.
            quantity: number of units to buy.

        Returns:
            dict: success flag and descriptive message.

        Tests:
            valid medicine type with enough budget -> returns success True
            invalid medicine type -> returns success False
        """
        if medicine_type not in self.MEDICINE_MAP:
            return {"success": False, "message": "Unknown medicine type."}
        med_cls = self.MEDICINE_MAP[medicine_type]
        med_item = med_cls()
        total_cost = med_item.price * quantity
        if self.sim.zoo.budget < total_cost:
            return {"success": False, "message": "Not enough money."}
        self.sim.zoo.budget -= total_cost
        self.sim.zoo.inventory.medicine.extend([med_item] * quantity)
        return {"success": True, "message": f"Bought {quantity}x {medicine_type}."}

    def sell_animal(self) -> Dict[str, Any]:
        """Sell one animal from the zoo inventory if available.

        Returns:
            dict: success flag and descriptive message.

        Tests:
            animals available -> returns success True and adjusts budget
            no animals available -> returns success False
        """
        if not self.sim.zoo.animals:
            return {"success": False, "message": "No animals available to sell."}
        animal = self.sim.zoo.animals.pop()
        self.sim.zoo.budget += int(animal.price / 2)
        for enclosure in self.sim.zoo.enclosures:
            if animal in enclosure.animals:
                enclosure.animals.remove(animal)
                break
        return {"success": True, "message": f"Sold {animal.name}."}

    def fire_staff(self) -> Dict[str, Any]:
        """Fire one staff member from the zoo if any exist."""
        if not self.sim.zoo.staff:
            return {"success": False, "message": "No staff to fire."}
        fired = self.sim.zoo.staff.pop()
        return {"success": True, "message": f"Fired {fired.name}."}

    def heal_animal(self) -> Dict[str, Any]:
        """Heal the first sick animal using any available medicine from inventory."""
        sick_animals = [animal for animal in self.sim.zoo.animals if animal.illness is not None]
        if not sick_animals:
            return {"success": False, "message": "No sick animals found."}
        if not self.sim.zoo.inventory.medicine:
            return {"success": False, "message": "No medicine in inventory."}
        animal = sick_animals[0]
        medicine = self.sim.zoo.inventory.medicine.pop(0)
        animal.illness = None
        animal.health = min(1.0, animal.health + 0.3)
        return {"success": True, "message": f"Healed {animal.name}."}

    def hire_staff(self, staff_type: str, shift_start: int = 8, shift_end: int = 18) -> Dict[str, Any]:
        """Hire a new staff member of the chosen type for the given shift if budget allows."""
        if staff_type not in self.STAFF_MAP:
            return {"success": False, "message": "Unknown staff type."}
        if self.sim.zoo.budget < 10:
            return {"success": False, "message": "Not enough money."}
        staff_cls = self.STAFF_MAP[staff_type]
        name = f"{staff_type}_{random.randint(1000,9999)}"
        working_hours = WorkingHours(shift_start, shift_end)
        before = len(self.sim.zoo.staff)
        self.sim.zoo.hireEmployee(staff_cls, name, working_hours)
        if len(self.sim.zoo.staff) == before:
            return {"success": False, "message": "Could not hire (invalid shift)."}
        self.sim.zoo.budget -= 10
        return {"success": True, "message": f"Hired {staff_type} for {shift_start:02d}:00-{shift_end:02d}:00."}

    def feed_animal(self) -> Dict[str, Any]:
        """Feed the first hungry animal fully."""
        hungry = [animal for animal in self.sim.zoo.animals if animal.get_hunger_percent() > 10]
        if not hungry:
            return {"success": False, "message": "No hungry animals found."}
        animal = hungry[0]
        animal.feed(1.0)
        return {"success": True, "message": f"Fed {animal.name}."}

    def clean_enclosure(self) -> Dict[str, Any]:
        """Clean the first enclosure in the zoo."""
        if not self.sim.zoo.enclosures:
            return {"success": False, "message": "No enclosures exist."}
        enclosure = self.sim.zoo.enclosures[0]
        enclosure.getCleaned()
        return {"success": True, "message": f"Cleaned enclosure {enclosure.number}."}

    def change_weather(self, weather: str) -> Dict[str, Any]:
        """Set the environment weather type to the requested value."""
        current = self.sim.zoo.environment
        if weather.upper() not in ["SUNNY", "CLOUDY", "RAINY"]:
            return {"success": False, "message": "Unknown weather type."}
        current.weather = current.weather.__class__[weather.upper()]
        return {"success": True, "message": f"Weather set to {weather}."}

    def move_player(self, dx: int, dy: int) -> Dict[str, Any]:
        """Move the player avatar by the specified grid offsets."""
        x, y = self.player_position
        self.player_position = (max(0, x + dx), max(0, y + dy))
        return {"success": True, "message": "Player moved."}
