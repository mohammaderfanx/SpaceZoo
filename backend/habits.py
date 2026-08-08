from enum import Enum
from typing import List


class SleepingHabit:

    def __init__(self, hourOfWaking: int, hourOfFallingAsleep: int):
        self.hourOfWaking = hourOfWaking
        self.hourOfFallingAsleep = hourOfFallingAsleep


class FoodPreference(Enum):
    CARNIVORE = "carnivore"
    HERBIVORE = "herbivore"
    OMNIVORE = "omnivore"

class EatingHabit:

    def __init__(self, foodPreference: FoodPreference, feedingTimes: List[int]):
        self.foodPreference = foodPreference
        self.feedingTimes = feedingTimes
        
#social habits?



class Habits:

    def __init__(self, sleepingHabit: SleepingHabit, eatingHabit: EatingHabit):
        self.sleepingHabit = sleepingHabit
        self.eatingHabit = eatingHabit

