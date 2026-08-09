# SpaceZoo - Digital Twin (Zoo Simulation)

## 1. Architecture Rules & OOP Principles (STRICT COMPLIANCE REQUIRED!)

The project employs a strict 4-layer architecture:

* `backend/` (Domain logic, simulation, core business classes)
* `database/` (Persistence layer using the Repository Pattern)
* `interface/` (The API Facade `SpaceZooAPI`)
* `frontend/` (Pygame rendering, user input, Dashboard UI)

**Golden OOP & Clean Code Rules:**

1. **One Class = One File.** No collection files or class dumping.
2. **Encapsulation:** Internal object states MUST be protected (`_` or `__` prefix) and manipulated strictly via defined interfaces (Getters, Setters, Methods).
3. **Facade Pattern:** The `frontend/` directory must NEVER import classes directly from `backend/` or `database/`. All communication goes strictly through `SpaceZooAPI`, which returns and receives only native Python data types (`dict`, `list[dict]`, primitives).
4. **Documentation & English Comments:** EVERY class, method, and inline comment MUST be written in English. All classes and methods require comprehensive Google-style docstrings.
5. **Testing Strategy (CRITICAL FOR GRADING):** For EVERY function and method in the codebase, exactly two test cases (Normal Case + Edge Case) MUST be explicitly *described* in text form inside the docstring (specifying Precondition, Action, Expected Result).
6. **Python Version:** All code must be fully compatible and executable with a Python 3.14 kernel.
7. **Individual Work Split:**
* **Frontend, UI, Rendering, Asset Management & API Facade Integration:** Mo (Individual Contribution)
* **Backend, Database, Simulation Logic:** Jasmin



---

## 2. Sub-Domain 1: Zoo Management (Business)

* `Zoo`: Central composition class aggregating `Enclosure`, `Staff`, `Finances`, and `Inventory`.
* `Staff` (Abstract Base Class): Defines name, ID, and abstract operational methods.
* Specific Subclasses (Inheritance): `Caretaker`, `Vet`, `Cashier`. Utilize polymorphism to execute role-specific responsibilities.


* `Enclosure`: Manages capacity, cleanliness level, and aggregates `Animal` objects.
* `Finances`: Encapsulates budget management, revenues (ticket sales), and expenses (staff salaries, food supplies).
* `Inventory`: Manages resource stocks (e.g., food supplies, medical stock).

---

## 3. Sub-Domain 2: Animal Simulation (Biology)

* `Animal` (Abstract Base Class): Contains attributes (species, age, health, hunger, energy) and abstract behavioral methods (`eat()`, `move()`, `age()`).
* Specific Species (Inheritance): The 6 species (`Birdy`, `Liz`, `Mal`, `Pinky`, `Rizzy`, `Sami`) inherit directly from `Animal`.
* `Behavior` (Interface / Strategy Base Class): Decoupled behavioral logic for feeding and social interactions (composed within `Animal`).
* `EnvironmentalFactor`: Modulates environmental parameters (e.g., day/night cycle controlling sleep states).

---

## 4. Sub-Domain 3: Simulation Core

* `SimulationEngine`: Controls simulation progression (`tick()` method) while adhering strictly to the Single Responsibility Principle (SRP).
* `EventScheduler`: Manages time-driven scheduled events (e.g., random illness outbreaks, feeding schedules).

---

## 5. Sub-Domain 4: Frontend & Rendering (Pygame & Dashboard Control Panel)

* **Canvas & Grid Specifications:**
* Fixed resolution: 1260 x 960 pixels (no camera scrolling).
* Tile Grid: 21 columns x 16 rows (60 x 60 pixel tiles).
* Sprites: Scaled to 60 x 60 pixels.
* Target Framerate: 30 FPS (`clock.tick(30)`).


* **Asset Loading (`frontend/asset_loader.py`):**
* Singleton class with in-memory caching.
* Loads and scales graphics from `frontend/assets/`.
* Returns fallback colored shapes (`pygame.Surface`) if image files are missing.


* **Dashboard Control Panel UI Structure:**
* **Sidebar (Left, 250px Width):** 10 interactive action buttons (Trigger tick, buy/sell animal, buy food/medicine, hire/fire staff, feed/heal animal, clean enclosure).
* **Topbar KPI Cards (Top):** Simulation time & day, budget & score, visitor count, attractiveness score.
* **Data Tables:** Structured data grids displaying Animals, Enclosures, Staff, Inventory, and Eggs.
* **Informational Cards:** Environmental status (Weather, Temperature, Wind) and System Info (Upcoming events).


* **User Input & Interaction:**
* Mouse click events (`pygame.MOUSEBUTTONDOWN`) mapped to UI button triggers and table selection.
* Keyboard WASD / Arrow key inputs captured by the frontend player controller and translated into API actions via `SpaceZooAPI`.



---

## 6. Docstring & Test Case Standard (Reference Pattern)

All Python code files in `frontend/` must adhere to the following docstring standard:

```python
# Author: Mo (Individual Contribution - Frontend, Rendering, UI, Asset Management & API Facade Integration)
# Module: SpaceZoo Frontend Theme & UI Components


def calculate_bar_width(current_val: float, max_val: float, total_pixels: int) -> int:
    """Calculates the pixel width of a progress bar based on a percentage value.

    Args:
        current_val (float): Current numeric value (e.g., Hunger at 60.0).
        max_val (float): Maximum possible value (e.g., 100.0).
        total_pixels (int): Total width of the progress bar graphic in pixels.

    Returns:
        int: Calculated width in pixels for the filled bar portion.

    Test Case 1 (Normal Case - 50% Fill):
        - Precondition: current_val = 50.0, max_val = 100.0, total_pixels = 200.
        - Action: calculate_bar_width(50.0, 100.0, 200) is called.
        - Expected Result: Returns exactly 100 (pixels).

    Test Case 2 (Edge Case - Value Exceeds Maximum):
        - Precondition: current_val = 120.0 (Overflow), max_val = 100.0, total_pixels = 200.
        - Action: calculate_bar_width(120.0, 100.0, 200) is called.
        - Expected Result: Clamps and returns maximum width of 200 (pixels).
    """
    if max_val <= 0:
        return 0
    ratio = min(max(current_val / max_val, 0.0), 1.0)
    return int(ratio * total_pixels)

```