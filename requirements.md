**Digital Twin of a Zoo Simulation**

Develop a digital twin of a zoo simulation by consistently applying the principles of Object-Oriented Programming (OOP) in Python. The project shall model both the administrative and economic aspects of a zoo as well as the biological processes of the animal world.

This project provides the opportunity to practically apply and deepen the OOP concepts learned in the module. You will model a complex system that simulates the interactions between various entities of a zoo. The digital twin should help develop a better understanding of the interconnections between zoo management and animal welfare.

**Important note:** The project is not intended to be implemented fully and comprehensively as a customer product. It is essential that the planning matches the implementation. The planning part is the individual contribution.

### Task
Design and implement a software model of a zoo. The focus is on a clean, modular, and extensible implementation using Python and the core principles of OOP.

Before starting the implementation, a careful planning phase is crucial. Visualize your object-oriented design using **Mermaid diagrams**. This helps you think through the structure of your system, identify potential problems early, and clearly communicate your design.

If working in a group, choose a focus area (e.g., Frontend, Backend, Database, Interface Design, …) and keep the planning for your self-chosen focus individual. Who does what must be clearly visible in the README and in the code (**deduction-relevant**).

Create at least one comprehensive focus-specific class diagram that shows the most important classes of your system, their attributes, methods, and the relationships between them (inheritance, aggregation, composition, association).

You may additionally create sequence diagrams to illustrate important interactions (e.g., “Zookeeper feeds animal”, “Visitor buys ticket”).

### System Structure
The simulation is divided into three main areas that must be connected through a common architecture:

#### Part 1: Zoo Management (Business Perspective)
This part models the organizational and economic aspects of zoo operations.

Example (adaptable):

- `Zoo`: A central class that represents the entire zoo and aggregates other management objects such as `Enclosure`, `Employee`, `Finances`, and `Inventory`.
- `Employee` (Abstract base class): Defines common properties (e.g., `Name`, `ID`) and basic behaviors.
- At least three specific employee types, e.g., `Zookeeper`, `Veterinarian`, `AdministrativeStaff`. Each subclass inherits from `Employee` and implements specific methods that reflect their tasks (e.g., `feed()`, `treat()`, `manageBudget()`).
- `Enclosure`: Represents individual enclosures with attributes such as `Size`, `Capacity`, `Condition` (e.g., cleanliness) and a list of the `Animal` objects contained in it.
- `Finances`: Manages income (e.g., ticket sales) and expenses (e.g., feed costs, salaries). Methods for updating and querying the budget.
- `Inventory`: Manages available resources such as `Feed` (different types) or `Medicines`.

**Application of OOP principles:**
- **Encapsulation:** Ensure that internal states of objects are protected and can only be manipulated via defined interfaces (methods).
- **Inheritance & Polymorphism:** Use the inheritance hierarchy for `Employee`. Polymorphic methods should be able to perform different actions depending on the employee type.
- **Composition & Aggregation:** The `Zoo` should act as a composition object that contains other objects such as `Enclosure` and `Employee`. `Enclosure` should aggregate `Animal` objects.

#### Part 2: Animal Simulation (Biological Perspective)
This part models the life, behavior, and interactions of the animals in the zoo.

Example (adaptable):

- `Animal` (Abstract base class): Defines basic attributes (`Name`, `Species`, `Age`, `Health`, `Hunger`, `Energy`) and abstract methods (`eat()`, `sleep()`, `move()`, `age()`).
- At least three specific animal species, e.g., `Lion`, `Giraffe`, `Penguin`. These inherit from `Animal` and implement species-specific details (e.g., `foodPreferences`, `typicalBehavior()`).
- `Behavior` (Abstract base class or interface): Defines general behavior patterns. Examples could be `FeedingBehavior`, `SocialBehavior`, or `RestingBehavior`. These can be implemented as separate classes used by animals.
- `EnvironmentalFactor`: A class for modeling simple environmental influences such as `Weather` (e.g., temperature) or `TimeOfDay`, which can influence animal behavior.

**Application of OOP principles:**
- **Inheritance & Polymorphism:** A clear inheritance hierarchy for `Animal` objects to define general animal logic and model specific species. Polymorphic methods (e.g., `eat()`) should adapt to the respective animal species.
- **Abstraction:** Use of abstract classes (`Animal`, `Behavior`) and methods to create a clear interface for implementing specific animal species and behaviors.
- **Composition:** An `Animal` object can be composed of various `Behavior` objects to model complex behavior patterns.

#### Part 3: Simulation Core & Interaction
This module coordinates the interaction between the management and animal simulation modules and controls the passage of time.

Example (adaptable):

- `SimulationEngine`: The main class that controls the simulation flow. It contains a reference to the `Zoo` object and is responsible for updating all objects per simulation step (e.g., `tick` method).
- `EventScheduler`: A simple class that can manage time-controlled events (e.g., feeding times, enclosure cleaning).

**Application of OOP principles:**
- **Single Responsibility Principle (SRP):** Each class should have a clearly defined task. The `SimulationEngine` controls the flow, the `Finances` manage money, the `Animal` classes simulate animals.
- Consistent application of OOP principles: Inheritance, polymorphism, encapsulation, and abstraction must be recognizable and correctly applied in the code.
- **Modular architecture:** The system should be designed so that it can easily be extended with new animal species, enclosure types, or management functions.

### Technical & Quality Requirements
- **Python implementation:** The entire code must be written in Python. (Exceptions in frontend presentation can be adapted → PyQt, HTML, JavaScript, … → focus remains on Python.)
- **Code quality:** The code should be well-structured, readable, and commented (docstrings for classes and methods are desired).
- **Simple interaction:** A basic possibility to interact with the simulation (e.g., via the console to query the state of the zoo or trigger actions) is required.
- Full documentation as known from the course must be included comprehensively (docstrings, inline comments).
- For every function, at least 2 tests must be described (but not implemented).
- The architecture must fulfill Frontend, Backend, Interface, and Database and be visibly separated (via file/folder structure → **do not write everything in one Python file**).
- Clear class separation → one responsibility per file.
- AI may be used but must always be verified using “human-in-the-loop” principles and aligned with the planning.

### Evaluation Criteria
This project is assessed according to the following criteria. The use of AI tools is allowed and is evaluated under the criterion “Reflection & AI Usage”. What matters is not the extent of AI usage, but the ability to understand the generated code, critically question it, adapt it, and reflect on one’s own learning process.

**Assessment criteria:**

- **Object-Oriented Programming (OOP) – Design & Implementation (40 points)**
  - Class structure & modeling (12 points)
  - Inheritance & Polymorphism (10 points)
  - Encapsulation & data integrity (8 points)
  - Modularity & extensibility (10 points)

- **Functionality & Correctness (15 points)**
  - Implementation of core functions (8 points)
  - Simulation logic & realism (7 points)

- **Test Description & Test Strategy (15 points)**
  - Test plan & test cases (10 points)
  - Test coverage & edge cases (5 points)

- **Documentation (15 points)**
  - Code documentation (Docstrings & comments) (15 points)

- **Design Visualization (Mermaid) (10 points)**

- **Reflection & AI Usage (5 points)**

**Pay special attention to the deduction-relevant points that are also reflected in the criteria!**

Even in group work, a submission is expected from all participants.  
In individual work, also reduce to one focus area in the individual contribution.

### Submission Requirements
- Upload all necessary files exclusively as a **zipped file**.
- Make sure the virtual environment is **not** included in the submission.
- Provide instructions for testing the application (it must be guaranteed that the application can be executed with a Python 3.14 kernel).
- Create corresponding `requirements.txt` files for your modules and README files.
- It must be clearly visible in the README who has chosen which area.  
  (**Deduction-relevant if missing!!**)