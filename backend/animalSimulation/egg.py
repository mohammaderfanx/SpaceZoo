from animalSimulation.animal import Animal

class Egg:
    """An unhatched animal of a given species, due to hatch after a fixed number of days."""

    def __init__(self, species: type[Animal], elapsedDays: int):
        self.species = species
        self.dayOfHatching = elapsedDays + 5