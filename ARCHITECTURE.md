# SpaceZoo - Digitaler Zwilling (Zoo-Simulation)

## 1. Architektur-Regeln & OOP-Prinzipien (STRIKT EINHALTEN!)
Das Projekt verwendet eine strikte 4-Schichten-Architektur. 
* `backend/` (Domänenlogik, Simulation, Klassen)
* `database/` (Persistenzschicht mit Repository-Pattern)
* `interface/` (Die API-Fassade `SpaceZooAPI`)
* `frontend/` (Pygame Rendering, User Input, UI)

**Goldene OOP- & Clean-Code-Regeln:**
1. **Eine Klasse = Eine Datei.** Keine Sammeldateien.
2. **Kapselung:** Interne Zustände von Objekten MÜSSEN geschützt sein (`__` oder `_` Präfix) und dürfen nur über definierte Schnittstellen (Getter/Setter/Methoden) manipuliert werden.
3. **Fassaden-Muster:** Das Frontend darf NIEMALS direkt Klassen aus dem Backend/Database importieren. Alles läuft über die `SpaceZooAPI`, die nur native Datentypen (Dicts, Listen) zurückgibt.
4. **Dokumentation:** JEDE Klasse und Methode MUSS einen ausführlichen Docstring besitzen.
5. **Testing (ABZUGSRELEVANT):** Für JEDE Funktion/Methode im Code MÜSSEN im Docstring oder als Kommentar exakt zwei Testfälle *beschrieben* (nicht implementiert!) werden (z.B. "Testfall 1: Erwartet True bei X, Testfall 2: Erwirft ValueError bei Y").
6. **Python-Version:** Der Code muss für einen Python 3.14 Kernel kompatibel und lauffähig sein.

## 2. Teilbereich 1: Zoo-Verwaltung (Business)
* `Zoo`: Zentrale Kompositions-Klasse. Aggregiert `Gehege`, `Mitarbeiter`, `Finanzen`, `Inventar`.
* `Mitarbeiter` (Abstrakte Basisklasse): Definiert Name, ID und abstrakte Methoden.
  * Spezifische Unterklassen (Vererbung): `Caretaker` (Tierpfleger), `Vet` (Tierarzt), `Cashier` (Kassenpersonal). Nutzen Polymorphie für ihre spezifischen Aufgaben.
* `Gehege`: Verwaltet Kapazität, Sauberkeit und aggregiert `Tier`-Objekte.
* `Finanzen`: Kapselt das Budget, Einnahmen (Tickets) und Ausgaben (Gehälter, Futter).
* `Inventar`: Verwaltet Ressourcen (z.B. Futterbestand).

## 3. Teilbereich 2: Tiersimulation (Biologie)
* `Tier` (Abstrakte Basisklasse): Attribute (Spezies, Alter, Gesundheit, Hunger, Energie) und abstrakte Methoden (`fressen()`, `bewegen()`, `altern()`).
* Spezifische Arten (Vererbung): Die 6 Spezies (Birdy, Liz, Mal, Pinky, Rizzy, Sami) erben von `Tier`.
* `Verhalten` (Interface/Basisklasse): Ausgelagerte Logik für Fress- oder Sozialverhalten (Komposition innerhalb von `Tier`).
* `Umweltfaktor`: Beeinflusst Parameter (z.B. Tageszeit steuert Schlaf).

## 4. Teilbereich 3: Simulationskern
* `SimulationEngine`: Steuert den Simulationsablauf (`tick()`-Methode) und wendet das Single Responsibility Principle (SRP) an.
* `EventScheduler`: Verwaltet zeitgesteuerte Events (z.B. zufällige Krankheiten, Fütterungszyklen).

## 5. Frontend & Rendering (Pygame)
* Map: SpaceZooBase (1260x960), Grid: 21x16, Sprites: 60x60.
* Der `AssetLoader` lädt Grafiken aus `frontend/assets/`.
* Eingaben (WASD) werden vom Frontend erfasst und an die API gesendet.