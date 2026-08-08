```mermaid
classDiagram
    class Food {
        +String name
        +List~FoodPreference~ foodPreference
        +int shelfLife
        +int pricePerKg
    }
    class Meat
    class Hay
    class Fish
    class FoodItem {
        +Food type
        +int weight
        +int bestBefore
        +int price
    }
    class Inventory {
        +List~FoodItem~ food
        +List~Medicine~ medicine
        +__checkForMedicineForSpecificIllness(type~Illness~ illness) bool
        +__listOfFoodInCategory(type~Food~ category) List~FoodItem~
    }
    class Animal {
        +String id
        +String name
        +int birthdate
        +Gender gender
        +float saturation
        +Illness illness
        +Lifecycle lifecycle
        +Habits habits
        +getLifecyclePhase(int elapsedDays) LifecyclePhase
        +feed(float percentHungerQuelled) void
        +sleep() void
        +age() void
        +layEgg() void
    }
    class Eagle
    class Wolf
    class Rabbit
    Animal <|-- Rabbit
    class Zoo {
        +int budget
        +List~Animal~ animals
        +List~Employee~ staff
        +List~Enclosure~ enclosures
        +int visitors
        +Inventory inventory
        +List~Egg~ eggs
        +EnvironmentalFactors environment
        +float score
        +getCaretakers() List~Caretaker~
        +getVets() List~Vet~
        +getCashiers() List~Cashier~
        +animalDies(Animal animal) void
        +buyNewAnimal() void
        +sellAnimal() void
        +hireEmployee() void
        +buyFood() void
        +buyMedicine() void
        +healAnimal(Animal animal) void
    }
    class Employee {
        +String id
        +String name
        +WorkingHours workingHours
        +int salary
        +isOnShift(int elapsedHours) bool
    }
    class WorkingHours {
        +int startOfShift
        +int endOfShift
    }
    class Caretaker {
        +feedAnimal(Animal animal, float percentHungerQuelled) void
    }
    class Vet {
        +healAnimal(Animal animal) void
    }
    class Cashier {
        +sellTicket() void
    }
    class Enclosure {
        +int number
        +int capacity
        +FoodPreference typeOfAnimal
        +List~Animal~ animals
        +float cleanliness
    }
    class EnvironmentalFactors {
        +int temperature
        +int windSpeed
        +Weather weather
        +getVisitorAttractiveness() float
    }
    class Egg {
        +Animal species
        +int dayOfHatching
    }
    class Illness {
        +String name
        +float lethality
        +float riskOfOccurrence
    }
    class Medicine {
        +String name
        +int shelfLife
        +int price
        +Illness illness
    }
    class Lifecycle {
        +object childPhase
        +object adultPhase
        +object seniorPhase
    }
    class Habits {
        +object sleepingHabit
        +object eatingHabit
    }

    Food <|-- Meat
    Food <|-- Hay
    Food <|-- Fish
    Animal <|-- Eagle
    Animal <|-- Wolf
    Animal <|-- Rabbit
    Employee <|-- Caretaker
    Employee <|-- Vet
    Employee <|-- Cashier
    Employee "1" o-- "1" WorkingHours : has
    Zoo "1" --* "*" Animal : owns
    Zoo "1" --* "*" Employee : employs
    Zoo "1" --* "*" Enclosure : contains
    Zoo "1" --* "*" Egg : stores
    Zoo "1" --* "1" Inventory : manages
    Zoo "1" --* "1" EnvironmentalFactors : uses
    Enclosure "1" o-- "*" Animal : houses
    Animal "1" o-- "1" Lifecycle : has
    Animal "1" o-- "1" Habits : has
    Animal "1" o-- "0-1" Illness : has
    Inventory "1" o-- "*" FoodItem : stocks
    Inventory "1" o-- "*" Medicine : stocks
    FoodItem "1" o-- "1" Food : references
    Egg "1" --> "1" Animal : species

```