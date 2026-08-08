from animal import Animal

class Egg:
    def __init__(self, species: type[Animal], elapsedDays: int):
        self.species = species
        self.dayOfHatching = elapsedDays + 5