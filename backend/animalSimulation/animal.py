"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""

import random
from enum import Enum
from backend.animalSimulation.illness import Illness
from backend.animalSimulation.lifecycle import Lifecycle, LifecyclePhase
from backend.animalSimulation.habits import Habits, SleepingHabit, EatingHabit, FoodPreference

class Gender(Enum):
    """Biological sex of an animal."""

    FEMALE = "female"
    MALE = "male"

class Animal:
    """Base class for a zoo animal, tracking identity, lifecycle, health, and habits."""

    def __init__(self, name: str, birthdate: int, gender: Gender):
            self.id = name
            self.name = name
            self.species = self.__class__.__name__
            self.birthdate = birthdate
            self.gender = gender
            self.saturation = 1
            self.health = 1
            self.energy = 1
            self.illness: Illness = None
            self.lifecycle: Lifecycle
            self.habits: Habits
            self.awake: bool = True
            self.price: int
            self.x: int = 0
            self.y: int = 0

    def get_age_days(self, elapsedDays: int) -> int:
        """Returns the animal's age in days relative to the current simulation day."""
        return max(0, elapsedDays - self.birthdate)

    def get_hunger_percent(self) -> float:
        """Returns the animal's hunger percentage based on saturation."""
        return max(0.0, min(100.0, 100.0 * (1.0 - self.saturation)))

    def to_dict(self, elapsedDays: int) -> dict:
        """Serializes the animal state to a dictionary for UI and persistence."""
        return {
            "id": self.id,
            "species": self.species,
            "name": self.name,
            "age_days": self.get_age_days(elapsedDays),
            "health": float(self.health),
            "hunger": float(self.get_hunger_percent()),
            "energy": float(self.energy),
            "is_sick": self.illness is not None,
            "awake": self.awake,
            "position": (self.x, self.y),
            "gender": self.gender.value,
        }

    def getLifecyclePhase(self, elapsedDays):
        """Returns the animal's current lifecycle phase based on its age.

        Args:
            self
            elapsedDays: number of full days elapsed in the simulation

        Returns:
            LifecyclePhase: the phase (child, adult, or senior) matching the animal's current age

        Tests:
            age below childPhase.endOfPhaseAge -> returns childPhase
            age below adultPhase.endOfPhaseAge but at or beyond childPhase.endOfPhaseAge -> returns adultPhase
            age at or beyond adultPhase.endOfPhaseAge -> returns seniorPhase
        """
        age = elapsedDays - self.birthdate
        if age < self.lifecycle.childPhase.endOfPhaseAge:
            return self.lifecycle.childPhase
        elif age < self.lifecycle.adultPhase.endOfPhaseAge:
            return self.lifecycle.adultPhase
        else:
            return self.lifecycle.seniorPhase

         
    def feed(self, percentHungerQuelled: float):
        """Sets the animal's saturation to the percentage of hunger quelled.

        Args:
            self
            percentHungerQuelled: fraction of the animal's hunger that gets satisfied

        Tests:
            percentHungerQuelled is 1.0 -> saturation is set to 1.0
            percentHungerQuelled is 0.0 -> saturation is set to 0.0
        """
        self.saturation = percentHungerQuelled

    def sleep(self):
        """Puts the animal to sleep.

        Args:
            self

        Tests:
            called while awake -> animal's energy increases
            called while asleep -> no-op
        """
        if not self.awake:
            return
        self.awake = False
        self.energy = 1

    def wake(self):
        """Wakes the animal.

        Args:
            self

        Tests:
            called while asleep -> animal wakes, energy stops increasing
            called while awake -> no-op
        """
        if self.awake:
            return
        self.awake = True

    def age(self, elapsedDays: int):
         """Advances the animal to its next lifecycle phase.

         Args:
             self
             elapsedDays: number of full days elapsed in the simulation

         Tests:
             animal reaches the end of its current phase -> lifecycle phase advances
             called on a senior animal -> animal dies
         """
         if self.getLifecyclePhase(elapsedDays) == self.lifecycle.seniorPhase:
             self.health = 0

    def layEgg(self, elapsedDays: int) -> bool:
        """Lays an egg.

        Args:
            self
            elapsedDays: number of full days elapsed in the simulation

        Returns:
            bool: True if the animal laid an egg this call

        Tests:
            conditions for laying are met -> a new Egg is added to the zoo
            conditions not met -> no egg is created
        """
        if self.gender != Gender.FEMALE or self.getLifecyclePhase(elapsedDays) != self.lifecycle.adultPhase:
            return False
        return random.random() < 0.1

class Eagle(Animal):
    """Animal species preset: eagle, with its specific habits and lifecycle."""

    def __init__(self, name: str, birthdate: int, gender: Gender):
        super().__init__(name, birthdate, gender)
        self.price = 50
        self.habits = Habits(SleepingHabit(5, 18), EatingHabit(FoodPreference.OMNIVORE, [6, 16]))
        self.lifecycle = Lifecycle(LifecyclePhase(4, 1, 0.4),
                                   LifecyclePhase(8, 2, 1),
                                   LifecyclePhase(13, 2, 1.4))


class Wolf(Animal):
    """Animal species preset: wolf, with its specific habits and lifecycle."""

    

    def __init__(self, name: str, birthdate: int, gender: Gender):
        super().__init__(name, birthdate, gender)
        self.price = 100
        self.habits = Habits(SleepingHabit(19, 6), EatingHabit(FoodPreference.CARNIVORE, [20, 5]))
        self.lifecycle = Lifecycle(LifecyclePhase(6, 3, 0.4),
                                   LifecyclePhase(15, 8, 1),
                                   LifecyclePhase(20, 6, 1.4))

class Rabbit(Animal):
    """Animal species preset: rabbit, with its specific habits and lifecycle."""


    def __init__(self, name: str, birthdate: int, gender: Gender):
            super().__init__(name, birthdate, gender)
            self.price = 75
            self.habits = Habits(SleepingHabit(10, 20), EatingHabit(FoodPreference.HERBIVORE, [20, 5]))
            self.lifecycle = Lifecycle(LifecyclePhase(1, 1, 0.4),
                                       LifecyclePhase(10, 3, 1),
                                       LifecyclePhase(15, 3, 1.4))
