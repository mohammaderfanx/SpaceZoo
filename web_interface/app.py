"""Web-based interface for the DinoZoo backend simulation.

Run with: python web_interface/app.py
Then open http://127.0.0.1:5000/ in a browser. Time advances automatically
in the background (driven by SimulationEngine.start()); the page polls
/api/status to stay in sync.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, jsonify, render_template, request

from backend.core.simulationEngine import SimulationEngine
from backend.animalSimulation.animal import Eagle, Wolf, Rabbit, Gender
from backend.animalSimulation.habits import FoodPreference
from backend.zooManagement.employee import Caretaker, Vet, Cashier, WorkingHours
from backend.zooManagement.food import Meat, Hay, Fish
from backend.zooManagement.medicine import Antibiotic
from backend.zooManagement.enclosure import Enclosure

app = Flask(__name__)
engine = SimulationEngine()

ANIMALS = {"eagle": Eagle, "wolf": Wolf, "rabbit": Rabbit}
EMPLOYEES = {"caretaker": Caretaker, "vet": Vet, "cashier": Cashier}
FOODS = {"meat": Meat, "hay": Hay, "fish": Fish}
DIETS = {
    "carnivore": FoodPreference.CARNIVORE,
    "herbivore": FoodPreference.HERBIVORE,
    "omnivore": FoodPreference.OMNIVORE,
}


def zoo_state() -> dict:
    """Serializes the current engine/zoo state for the dashboard and API responses."""
    with engine.lock:
        zoo = engine.zoo
        return {
            "day": engine.elapsedDays,
            "hour": engine.elapsedHours,
            "budget": zoo.budget,
            "visitors": zoo.visitors,
            "score": round(zoo.score, 2),
            "animals": [animal.to_dict(engine.elapsedDays) for animal in zoo.animals],
            "staff": [employee.to_dict() for employee in zoo.staff],
            "enclosures": [
                {
                    "number": enclosure.number,
                    "diet": enclosure.typeOfAnimal.value,
                    "cleanliness": round(enclosure.cleanliness, 2),
                    "capacity": enclosure.capacity,
                    "occupied": len(enclosure.animals),
                }
                for enclosure in zoo.enclosures
            ],
            "food": [
                {"name": item.type.name, "weight": item.weight, "best_before": item.bestBefore}
                for item in zoo.inventory.food
            ],
            "medicine_count": len(zoo.inventory.medicine),
            "eggs": len(zoo.eggs),
        }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def api_status():
    return jsonify(zoo_state())


@app.route("/api/tick", methods=["POST"])
def api_tick():
    engine.tick_once()
    return jsonify(zoo_state())


@app.route("/api/animals", methods=["POST"])
def api_buy_animal():
    data = request.get_json(force=True) or {}
    animal_cls = ANIMALS.get(data.get("species"))
    if not animal_cls:
        return jsonify(error="Invalid species."), 400
    name = (data.get("name") or "").strip() or "Unnamed"
    gender = Gender.FEMALE if data.get("gender") == "f" else Gender.MALE

    with engine.lock:
        before = len(engine.zoo.animals)
        engine.zoo.buyNewAnimal(animal_cls, name, engine.elapsedDays, gender)
        bought = len(engine.zoo.animals) != before
    if not bought:
        return jsonify(error="Not enough budget."), 400
    return jsonify(zoo_state())


@app.route("/api/enclosures", methods=["POST"])
def api_add_enclosure():
    data = request.get_json(force=True) or {}
    diet = DIETS.get(data.get("diet"))
    if not diet:
        return jsonify(error="Invalid diet."), 400
    try:
        capacity = int(data.get("capacity") or 5)
    except (TypeError, ValueError):
        return jsonify(error="Invalid capacity."), 400

    with engine.lock:
        engine.zoo.enclosures.append(Enclosure(capacity, diet))
    return jsonify(zoo_state())


@app.route("/api/staff", methods=["POST"])
def api_hire_employee():
    data = request.get_json(force=True) or {}
    employee_cls = EMPLOYEES.get(data.get("role"))
    if not employee_cls:
        return jsonify(error="Invalid role."), 400
    name = (data.get("name") or "").strip() or "Unnamed"
    try:
        start = int(data.get("start") if data.get("start") is not None else 8)
        end = int(data.get("end") if data.get("end") is not None else 16)
    except (TypeError, ValueError):
        return jsonify(error="Invalid shift hours."), 400

    with engine.lock:
        before = len(engine.zoo.staff)
        engine.zoo.hireEmployee(employee_cls, name, WorkingHours(start, end))
        hired = len(engine.zoo.staff) != before
    if not hired:
        return jsonify(error="Could not hire (invalid data)."), 400
    return jsonify(zoo_state())


@app.route("/api/food", methods=["POST"])
def api_buy_food():
    data = request.get_json(force=True) or {}
    food_cls = FOODS.get(data.get("food"))
    if not food_cls:
        return jsonify(error="Invalid food."), 400
    try:
        weight = int(data.get("weight") or 10)
    except (TypeError, ValueError):
        return jsonify(error="Invalid weight."), 400

    with engine.lock:
        before = len(engine.zoo.inventory.food)
        engine.zoo.buyFood(food_cls, weight, engine.elapsedDays)
        bought = len(engine.zoo.inventory.food) != before
    if not bought:
        return jsonify(error="Not enough budget."), 400
    return jsonify(zoo_state())


@app.route("/api/medicine", methods=["POST"])
def api_buy_medicine():
    data = request.get_json(force=True) or {}
    try:
        quantity = int(data.get("quantity") or 1)
    except (TypeError, ValueError):
        return jsonify(error="Invalid quantity."), 400

    with engine.lock:
        before = len(engine.zoo.inventory.medicine)
        engine.zoo.buyMedicine(Antibiotic(), quantity)
        bought = len(engine.zoo.inventory.medicine) != before
    if not bought:
        return jsonify(error="Not enough budget."), 400
    return jsonify(zoo_state())


@app.route("/api/heal", methods=["POST"])
def api_heal_animal():
    data = request.get_json(force=True) or {}
    animal_id = data.get("animal_id")

    with engine.lock:
        animal = next((a for a in engine.zoo.animals if a.id == animal_id), None)
        if animal is None:
            return jsonify(error="Animal not found."), 404
        healed = engine.zoo.healAnimal(animal)
    if not healed:
        return jsonify(error="No matching medicine in stock."), 400
    return jsonify(zoo_state())


def main() -> None:
    engine.start()
    try:
        app.run(debug=False, threaded=True)
    finally:
        engine.stop()


if __name__ == "__main__":
    main()
