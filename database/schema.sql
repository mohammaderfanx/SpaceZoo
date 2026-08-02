-- SpaceZoo Datenbank-Schema (SQLite-kompatibel)

-- 1. Tabelle für den generellen Zoo-Status (Geld, Zeit, Tag/Nacht-Zyklus, Spielerposition)
CREATE TABLE IF NOT EXISTS zoo_status (
    id INTEGER PRIMARY KEY CHECK (id = 1), -- Erzwingt eine Singleton-Zeile für den aktuellen Spielstand
    money INTEGER NOT NULL DEFAULT 100,
    simulation_time REAL NOT NULL DEFAULT 0.0, -- Gesamtzeit in Sekunden
    is_night BOOLEAN NOT NULL DEFAULT 0,
    player_x INTEGER NOT NULL DEFAULT 10,
    player_y INTEGER NOT NULL DEFAULT 8,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabelle für das Inventar / Futter- und Item-Bestand
CREATE TABLE IF NOT EXISTS inventory (
    item_id TEXT PRIMARY KEY, -- z.B. 'futter_birdy', 'futter_liz', 'medizin'
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabelle für gekaufte Tiere (inkl. Lebenszyklus, Hunger und Gesundheitsstatus)
CREATE TABLE IF NOT EXISTS creatures (
    id TEXT PRIMARY KEY,
    species TEXT NOT NULL, -- 'Birdy', 'Liz', 'Mal', 'Pinky', 'Rizzy', 'Sami'
    name TEXT NOT NULL,
    age_seconds REAL NOT NULL DEFAULT 0.0, -- Lebenszyklus: 0-300s Kind, 300-600s Erwachsen, 600-900s Alt
    hunger REAL NOT NULL DEFAULT 0.0 CHECK (hunger >= 0.0 AND hunger <= 100.0),
    hunger_timer REAL NOT NULL DEFAULT 10.0, -- 10s Countdown bei 100% Hunger bis zum Tod
    is_sick BOOLEAN NOT NULL DEFAULT 0,
    sick_timer REAL NOT NULL DEFAULT 15.0, -- 15s Countdown bei Krankheit bis zum Tod
    pos_x INTEGER NOT NULL,
    pos_y INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabelle für das aktive Personal (Caretaker, Vet, Cashier)
CREATE TABLE IF NOT EXISTS staff (
    id TEXT PRIMARY KEY,
    staff_type TEXT NOT NULL, -- 'Caretaker', 'Vet', 'Cashier'
    name TEXT NOT NULL,
    salary INTEGER NOT NULL DEFAULT 10, -- 10$ Personalkosten
    status TEXT NOT NULL DEFAULT 'Idle', -- 'Idle', 'Working'
    pos_x INTEGER NOT NULL,
    pos_y INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Initialer Zoo-Status-Eintrag (Standardwerte)
INSERT OR IGNORE INTO zoo_status (id, money, simulation_time, is_night, player_x, player_y)
VALUES (1, 100, 0.0, 0, 10, 8);
