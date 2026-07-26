# SpaceZoo - Architektur & Spezifikation

## 1. Architektur-Regeln (STRIKT EINHALTEN)
Wir verwenden eine strikte 4-Schichten-Architektur. Das Projekt ist in folgende Hauptordner unterteilt:
* `backend/` (Domänenlogik, Simulation, Klassen wie Tier, Besucher, EventScheduler)
* `database/` (Persistenzschicht mit Repository-Pattern)
* `interface/` (Die API-Fassade)
* `frontend/` (Pygame Rendering, User Input, UI)

**Goldene Regeln:**
1. Eine Klasse = Eine Datei.
2. Das Frontend (`frontend/`) darf NIEMALS direkt Klassen aus dem `backend/` oder `database/` importieren.
3. Die gesamte Kommunikation zwischen Frontend und Backend MUSS über die Klasse `SpaceZooAPI` in `interface/spacezoo_api.py` erfolgen (Fassaden-Muster). Die API liefert nur Basis-Datentypen (Dicts, Listen, Primitives) an das Frontend, keine Backend-Objekte.

## 2. Spielmechaniken
* 6 Tierarten (Birdy, Liz, Mal, Pinky, Rizzy, Sami). Lebenszyklus: 15 Minuten (Kind: 0-5, Erwachsen: 5-10, Alt: 10-15).
* Hunger: Steigt kontinuierlich. Bei 100% startet ein 10s-Timer bis zum Tod.
* Krankheit: Tritt zufällig auf. Startet 15s-Timer bis zum Tod.
* Personal (Kosten: 10$): Caretaker (füttert autonom), Vet (heilt autonom), Cashier (Kasse).
* Besucher: Spawnen alle 10s (45% Chance). Stellen sich in einer Linie an. Warten 15s am Ticketschalter, zahlen 1$, betreten Zoo (Max. 10 im Zoo). Despawnen nach 40s im Zoo.
* Simulation: 2-Minuten Tag/Nacht-Zyklus.

## 3. Frontend & Rendering
* Map: 1260 x 960 Pixel. Sprites: 60 x 60 Pixel. Grid: 21x16.
* Spieler bewegt sich mit WASD.
* Taskbar (unten, einklappbar): Zeigt Quick-Stats (eingeklappt) oder detailliertes Dashboard (aufgeklappt).