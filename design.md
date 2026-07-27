# Design: Zoo-Verwaltung (Mermaid-Diagramme)

Dieses Dokument enthält Diagramme in Mermaid-Syntax zur Dokumentation des OOP-Designs für den Teilbereich "Zoo-Verwaltung".

## Klassendiagramm (Mermaid)

```mermaid
classDiagram
    class Zoo {
        -Gehege[] gehege
        -Mitarbeiter[] mitarbeiter
        -Finanzen finanzen
        -Inventar inventar
        +tick()
        +addGehege(Gehege)
        +hire(Mitarbeiter)
    }

    class Gehege {
        -int kapazitaet
        -float sauberkeit
        -Tier[] tiere
        +addTier(Tier)
        +removeTier(Tier)
    }

    class Finanzen {
        -float budget
        -float einnahmen
        -float ausgaben
        +addEinnahme(float)
        +addAusgabe(float)
        +paySalary(Mitarbeiter)
    }

    class Inventar {
        -map<string,int> items
        +addItem(string,int)
        +consumeItem(string,int)
    }

    class Mitarbeiter {
        <<abstract>>
        -int id
        -string name
        -float gehalt
        +performDuty()
    }

    class Caretaker
    class Vet
    class Cashier

    class Tier {
        <<abstract>>
        -string species
        -int alter
        -float gesundheit
        -float hunger
        +fressen()
        +bewegen()
        +altern()
    }

    class Birdy
    class Liz
    class Mal
    class Pinky
    class Rizzy
    class Sami

    Zoo "1" o-- "0..*" Gehege : enthält
    Zoo "1" o-- "0..*" Mitarbeiter : beschäftigt
    Zoo "1" o-- "1" Finanzen : besitzt
    Zoo "1" o-- "1" Inventar : besitzt
    Gehege "1" o-- "0..*" Tier : beherbergt
    Mitarbeiter <|-- Caretaker
    Mitarbeiter <|-- Vet
    Mitarbeiter <|-- Cashier
    Tier <|-- Birdy
    Tier <|-- Liz
    Tier <|-- Mal
    Tier <|-- Pinky
    Tier <|-- Rizzy
    Tier <|-- Sami
```

## Sequenzdiagramm (Mermaid): "Besucher kauft Ticket am Eingang"

Dieses Diagramm beschreibt die Interaktion, wenn ein Besucher ankommt, in der Schlange bezahlt (15s) und den Zoo betritt (Besuchszeit 40s).

```mermaid
sequenceDiagram
    participant Visitor
    participant Cashier
    participant Finanzen
    participant SimulationEngine

    Visitor->>Cashier: Ankunft, Anfrage Ticket
    Cashier->>Visitor: Zeigt Preis (z.B. 1$)
    Visitor->>Cashier: Bezahlen (-> 15s)
    activate Cashier
    Cashier->>Finanzen: addEinnahme(1.0)
    Finanzen-->>Cashier: Bestätigung
    Cashier-->>Visitor: Übergibt Ticket; Visitor.status = "InZoo"
    deactivate Cashier
    SimulationEngine->>Visitor: startBesuchsTimer(40s)
    Note over Visitor,SimulationEngine: Visitor erkundet Karte; nach 40s verlässt Visitor Zoo
```

---

Hinweis: Die Diagramme sind als Mermaid-Code gehalten und können z.B. in VS Code (Markdown Preview Mermaid) oder auf mermaid.live gerendert werden.
