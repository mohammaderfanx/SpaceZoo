"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""

from enum import Enum
from typing import List


class SleepingHabit:
    """The hours at which an animal wakes and falls asleep."""

    def __init__(self, hourOfWaking: int, hourOfFallingAsleep: int):
        self.hourOfWaking = hourOfWaking
        self.hourOfFallingAsleep = hourOfFallingAsleep


class FoodPreference(Enum):
    """Dietary category of an animal."""

    CARNIVORE = "carnivore"
    HERBIVORE = "herbivore"
    OMNIVORE = "omnivore"

class EatingHabit:
    """An animal's diet type and the hours at which it needs feeding."""

    def __init__(self, foodPreference: FoodPreference, feedingTimes: List[int]):
        self.foodPreference = foodPreference
        self.feedingTimes = feedingTimes
        
#social habits?



class Habits:
    """Bundles an animal's sleeping and eating habits."""

    def __init__(self, sleepingHabit: SleepingHabit, eatingHabit: EatingHabit):
        self.sleepingHabit = sleepingHabit
        self.eatingHabit = eatingHabit

