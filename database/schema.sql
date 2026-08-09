--author: Mohammad Rezaei
--date: 08.08.2026
--version: 1

-- DinoZoo / SimZoo savegame schema.
-- Persists the state of backend.core.simulationEngine.SimulationEngine /
-- backend.core.zoo.Zoo so a session can be restored on the next launch.

-- 1. Singleton row for zoo-wide state (budget, simulation clock, environment, score).
CREATE TABLE IF NOT EXISTS zoo_status (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    has_save BOOLEAN NOT NULL DEFAULT 0,
    budget INTEGER NOT NULL DEFAULT 100,
    elapsed_days INTEGER NOT NULL DEFAULT 0,
    elapsed_hours INTEGER NOT NULL DEFAULT 0,
    visitors INTEGER NOT NULL DEFAULT 0,
    score REAL NOT NULL DEFAULT 0.0,
    weather TEXT NOT NULL DEFAULT 'SUNNY',
    temperature INTEGER NOT NULL DEFAULT 25,
    wind_speed INTEGER NOT NULL DEFAULT 40,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Enclosures (number matches backend.zooManagement.enclosure.Enclosure.number).
CREATE TABLE IF NOT EXISTS enclosures (
    number INTEGER PRIMARY KEY,
    capacity INTEGER NOT NULL,
    diet TEXT NOT NULL,                 -- 'carnivore' | 'herbivore' | 'omnivore'
    cleanliness REAL NOT NULL DEFAULT 1.0
);

-- 3. Animals (one row per backend.animalSimulation.animal.Animal instance).
CREATE TABLE IF NOT EXISTS animals (
    id TEXT PRIMARY KEY,
    species TEXT NOT NULL,              -- 'Eagle' | 'Wolf' | 'Rabbit'
    name TEXT NOT NULL,
    birthdate INTEGER NOT NULL,
    gender TEXT NOT NULL,               -- 'male' | 'female'
    health REAL NOT NULL DEFAULT 1.0,
    saturation REAL NOT NULL DEFAULT 1.0,
    energy REAL NOT NULL DEFAULT 1.0,
    awake BOOLEAN NOT NULL DEFAULT 1,
    illness_name TEXT,
    enclosure_number INTEGER REFERENCES enclosures(number)
);

-- 4. Staff (Caretaker, Vet, Cashier).
CREATE TABLE IF NOT EXISTS staff (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,                 -- 'Caretaker' | 'Vet' | 'Cashier'
    name TEXT NOT NULL,
    shift_start INTEGER NOT NULL,
    shift_end INTEGER NOT NULL,
    salary INTEGER NOT NULL DEFAULT 10,
    busy_for INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'Idle'
);

-- 5. Food stock (backend.zooManagement.food.FoodItem instances).
CREATE TABLE IF NOT EXISTS food_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_type TEXT NOT NULL,            -- 'Meat' | 'Hay' | 'Fish'
    weight INTEGER NOT NULL,
    best_before INTEGER NOT NULL
);

-- 6. Medicine stock, grouped by type since individual units are interchangeable.
CREATE TABLE IF NOT EXISTS medicine_items (
    medicine_type TEXT PRIMARY KEY,     -- 'Antibiotic'
    quantity INTEGER NOT NULL DEFAULT 0
);

-- 7. Unhatched eggs.
CREATE TABLE IF NOT EXISTS eggs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    species TEXT NOT NULL,
    day_of_hatching INTEGER NOT NULL
);

INSERT OR IGNORE INTO zoo_status (id) VALUES (1);
