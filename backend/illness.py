class Illness:
    def __init__(self, name: str, lethality: float, riskOfOccurrence: float):
        self.name = name
        self.lethality = lethality
        self.riskOfOccurrence = riskOfOccurrence

class ExampleIllness(Illness):
    def __init__(self):
        super().__init__("exampleIllness", 0.2, 0.07)

    
