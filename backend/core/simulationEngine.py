"""
author: Jasmin Romeyke
date: 08.08.2026
version: 1
"""


import random
import threading
from core.eventScheduler import EventScheduler
from core.zoo import Zoo
from animalSimulation.egg import Egg
from animalSimulation.animal import Gender
import statistics

class SimulationEngine:
    """Drives the zoo's simulation loop, advancing time and applying periodic effects each tick."""

    def __init__(self):
        self.zoo = Zoo()
        self.eventScheduler: EventScheduler = EventScheduler(self.zoo)
        self.secondsPerTick = 10 #possibly change
        self.ticks = 0
        self.elapsedHours = 0
        self.elapsedDays = 0
        self.running = False


    def tick(self):
        """Advances the simulation by one time step and applies all periodic effects.

        Args:
            self

        Tests:
            called once -> elapsed time advances and all periodic effects apply, with the next tick scheduled via threading.Timer
        """
        self.increaseTime()
        self.eventScheduler.scheduleEvents(self.elapsedDays, self.elapsedHours)
        self.decreaseSaturation()
        self.decreaseHealth()
        self.decreaseEnergy()
        self.layEggs()
        self.eggsHatch()
        self.catchIllnesses()
        self.cleanEnclosures()
        self.calculateVisitorScore()
        threading.Timer(self.secondsPerTick, self.tick).start()


    def increaseTime(self):
        """Advances the elapsed hour/day counters.

        Args:
            self

        Tests:
            elapsedHours below 23 -> only elapsedHours increases
            elapsedHours reaches 24 -> elapsedHours resets to 0 and elapsedDays increases
        """
        self.elapsedHours += 1
        if self.elapsedHours == 24:
            self.elapsedHours = 0
            self.elapsedDays += 1


    def decreaseSaturation(self):
        """Reduces saturation for unfed animals, possibly killing them.

        Args:
            self

        Return:
            None

        Tests:
            animal not fed this tick -> saturation decreases
            animal already at minimum saturation -> animal dies
        """
        for animal in list(self.zoo.animals):
            if animal.saturation <= 0:
                self.zoo.animalDies(animal)
            else:
                animal.saturation = max(0, animal.saturation - 0.1)

    def decreaseHealth(self):
        """Reduces health for sick animals, possibly killing them.

        Args:
            self

        Return:
            None
        
                    
        Tests:
            animal is sick -> health decreases
            animal's health reaches 0 -> animal dies
        """
        for animal in list(self.zoo.animals):
            if animal.illness is not None:
                animal.health = max(0, animal.health - animal.illness.lethality * 0.1)
            if animal.health <= 0:
                self.zoo.animalDies(animal)

    def decreaseEnergy(self):
        """Reduces energy for animals that aren't sleeping.

        Args:
            self

        Return:
            None

                    
        Tests:
            animal is awake -> energy decreases
            animal is asleep -> energy stays the same
        """
        for animal in self.zoo.animals:
            if animal.awake:
                animal.energy = max(0, animal.energy - 0.05)

    def layEggs(self):
        """Lets one eligible animals per enclosure with space lay an egg by chance.

        Args:
            self

        Return:
            None

        Tests:
            eligible animal and a free spot -> egg may be created
            no eligible animals -> no eggs are created
        """
        possibleEnclosures = [enclosure for enclosure in self.zoo.enclosures if len(enclosure.animals) < enclosure.capacity]
        for enclosure in possibleEnclosures:
            possibleAnimals = [animal for animal in enclosure.animals if animal.gender.name == 'FEMALE']
            if len(possibleAnimals) > 0:
                if possibleAnimals[0].layEgg(self.elapsedDays):
                    self.zoo.eggs.append(Egg(type(possibleAnimals[0]), self.elapsedDays))

    def eggsHatch(self):
        """Hatches eggs that are due, creating new animals.

        Args:
            self

        Return:
            None

        Tests:
            egg's dayOfHatching has passed -> new animal is created and egg removed
            egg not yet due -> egg remains unchanged
        """
        hatchedEggs = [egg for egg in self.zoo.eggs if egg.dayOfHatching <= self.elapsedDays]
        for egg in hatchedEggs:
            gender = random.choice(list(Gender))
            newId = f"{egg.species.__name__}-{self.elapsedDays}-{len(self.zoo.animals)}"
            newAnimal = egg.species(newId, egg.species.__name__, self.elapsedDays, gender)
            self.zoo.animals.append(newAnimal)
            self.zoo.eggs.remove(egg)

    def catchIllnesses(self):
        """Randomly assigns illnesses to animals, more likely where a sick animal already shares the enclosure.

        Args:
            self

        Return:
            None

        Tests:
            enclosure has a sick animal -> higher chance of new illnesses there
            no sick animals present -> lower baseline chance applies
        """


    def decreaseCleanliness(self):
        """Reduces enclosure cleanliness over time as animals dirty them.

        Args:
            self

        Return:
            None

        Tests:
            enclosure cleanliness above 0 -> cleanliness decreases by 10%
            enclosure already at minimum cleanliness -> stays at 0
        """
        for enclosure in self.zoo.enclosures:
            enclosure.cleanliness = max(0, enclosure.cleanliness - 0.1)

    def cleanEnclosures(self):
        """Cleans enclosures below 50% cleanliness, dividing them among available caretakers.

        Args:
            self

        Return:
            None

        Tests:
            caretaker available and enclosure below 50% cleanliness -> caretaker cleans it
            no caretaker available -> enclosure stays dirty
            enclosure at or above 50% cleanliness -> not cleaned
        """
        enclosuresToClean = [enclosure for enclosure in self.zoo.enclosures if enclosure.cleanliness < 0.5]

        if len(enclosuresToClean) == 0:
            return 
        
        availableCaretakers = self.zoo.getCaretakers()
        if len(availableCaretakers) == 0:
            return 
        
        for indexEnclosure in range(len(enclosuresToClean)):
            currentEnclosure = enclosuresToClean[indexEnclosure]
            currentCaretaker = availableCaretakers[indexEnclosure % len(availableCaretakers)]
            currentCaretaker.cleanEnclosure(currentEnclosure)
        availableCaretakers = self.zoo.getCaretakers()
        
        


    def calculateVisitorScore(self):
        """Computes the visitor score from environment, animal count, and enclosure cleanliness.

        Args:
            self

        Return:
            None

        Returns:
            float: combined score used to attract visitors

        Tests:
            high environmental attractiveness and clean enclosures -> high score
            no enclosures -> cleanliness doesn't affect score
        """
        environmentalScore =  self.zoo.environment.getVisitorAttractiveness() # why :(?
        animalScore = len(self.zoo.animals)
        cleanlinessScore =1
        if len(self.zoo.enclosures) != 0:
            cleanlinessScore = statistics.mean(enclosure.cleanliness for enclosure in self.zoo.enclosures)
        return environmentalScore * animalScore * cleanlinessScore
        

    def start(self):
        """Starts the simulation loop.

        Args:
            self

        Return:
            None

        Tests:
            called once -> tick() begins the recurring simulation loop
            called again while already running -> is a no-op, no overlapping loop starts
        """
        if self.running:
            return
        self.running = True
        self.tick()
