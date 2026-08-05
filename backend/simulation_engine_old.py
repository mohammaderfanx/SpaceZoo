"""
SimulationEngine für SpaceZoo.
Verwaltet den globalen Zustand des Zoos, aktualisiert alle Entitäten (Spieler, Tiere, Besucher, Personal)
und implementiert die zentralen Spielmechaniken.
"""

import random
import uuid
from typing import Any, Dict, List, Optional

from backend.animal_old import Animal
from backend.event_scheduler import EventScheduler
from backend.player import Player
from backend.staff import Caretaker, Cashier, Staff, Vet
from backend.visitor import Visitor


class SimulationEngine:
    """
    Zentrale Simulations-Engine des SpaceZoo-Spiels.
    """

    def __init__(self) -> None:
        self.money: int = 100
        self.simulation_time: float = 0.0  # In Sekunden

        # Tag/Nacht-Zyklus: 2 Minuten gesamt = 120 Sekunden.
        # 60s Tag, 60s Nacht.
        self.day_duration: float = 120.0
        self.is_night: bool = False

        # Entitäten-Listen
        self.player: Player = Player(10, 8)
        self.creatures: List[Animal] = []
        self.visitors: List[Visitor] = []
        self.staff: List[Staff] = []

        # Scheduler für Events
        self.scheduler: EventScheduler = EventScheduler()

        # Timer für Besucher-Spawns (alle 10s)
        self.visitor_spawn_timer: float = 10.0

        # Max. Besucher gleichzeitig im Zoo
        self.max_visitors_in_zoo: int = 10

        # Kassen-Position / Ticket-Counter auf der Grid-Map
        self.ticket_counter_pos = (5, 2)
        # Zoo-Eingang
        self.zoo_entrance_pos = (6, 3)
        # Zoo-Ausgang / Despawn-Punkt
        self.zoo_exit_pos = (0, 8)

    def tick(self, delta_time: float) -> Dict[str, Any]:
        """
        Aktualisiert den gesamten Zustand der Simulation um die vergangen Zeit delta_time.

        :param delta_time: Zeitänderung in Sekunden.
        :return: Ein Dictionary mit aufgetretenen Ereignissen ('events').
        """
        events_occurred: List[str] = []

        # 1. Simulationszeit und Tag/Nacht-Zyklus aktualisieren
        self.simulation_time += delta_time
        cycle_progress = self.simulation_time % self.day_duration
        new_is_night = cycle_progress >= (self.day_duration / 2.0)
        if new_is_night != self.is_night:
            self.is_night = new_is_night
            phase = "Nacht" if self.is_night else "Tag"
            events_occurred.append(f"Tagesphase geändert zu: {phase}")

        # 2. Scheduler ticken
        self.scheduler.tick(delta_time)

        # 3. Besucher-Spawns steuern (Alle 10s besteht eine 45% Chance)
        self.visitor_spawn_timer -= delta_time
        if self.visitor_spawn_timer <= 0.0:
            self.visitor_spawn_timer = 10.0
            if random.random() < 0.45:
                # Prüfen, wie viele Besucher aktuell im Zoo sind (InZoo + BuyingTicket)
                current_active_visitors = sum(1 for v in self.visitors if v.status in ["InZoo", "BuyingTicket", "Queuing"])
                if current_active_visitors < self.max_visitors_in_zoo:
                    new_visitor = Visitor(
                        id_=str(uuid.uuid4())[:8],
                        pos_x=0,  # Spawnt am linken Rand
                        pos_y=2,  # Auf Schlangen-Höhe
                    )
                    self.visitors.append(new_visitor)
                    events_occurred.append(f"Besucher {new_visitor.id} ist am Ticketschalter erschienen.")

        # 4. Tiere aktualisieren (Altern, Hunger, Krankheit)
        dead_creatures = []
        for creature in self.creatures:
            was_sick = creature.is_sick
            was_dead = creature.is_dead

            creature.tick(delta_time)

            if creature.is_sick and not was_sick:
                events_occurred.append(f"WARNUNG: Tier {creature.name} ({creature.species}) ist krank geworden!")

            if creature.is_dead and not was_dead:
                events_occurred.append(f"TRAURIG: Tier {creature.name} ({creature.species}) ist gestorben.")
                dead_creatures.append(creature)

        # Gestorbene Tiere entfernen
        for dead in dead_creatures:
            if dead in self.creatures:
                self.creatures.remove(dead)

        # 5. Besucher aktualisieren (Warteschlange, Ticketkauf, Erkunden, Verlassen)
        cashier_present = any(isinstance(s, Cashier) for s in self.staff)
        
        # Sortiere Besucher in Queuing-Status, um Schlangen-Verhalten zu simulieren
        queuing_visitors = [v for v in self.visitors if v.status in ["Queuing", "BuyingTicket"]]
        
        for i, visitor in enumerate(queuing_visitors):
            # Der vorderste Besucher (Index 0) darf an die Kasse gehen
            if i == 0:
                visitor.status = "BuyingTicket"
                # Ticketschalter-Wartezeit läuft ab, falls ein Kassierer da ist
                if cashier_present:
                    ticket_finished = visitor.wait_in_line(delta_time)
                    if ticket_finished:
                        visitor.status = "InZoo"
                        visitor.x, visitor.y = self.zoo_entrance_pos
                        self.money += 1  # Zahlt 1$ Eintritt
                        events_occurred.append(f"Besucher {visitor.id} hat ein Ticket gekauft und zahlt 1$.")
            else:
                visitor.status = "Queuing"
                # Rückstau-Positionierung
                target_x = max(0, self.ticket_counter_pos[0] - i)
                visitor.move_to(target_x, self.ticket_counter_pos[1])

        # Besucher im Zoo und beim Verlassen
        leaving_visitors = []
        for visitor in self.visitors:
            if visitor.status == "InZoo":
                visitor.explore_zoo(delta_time)
                # Zufällige Bewegung im Zoo
                if random.random() < 0.2:
                    dx = random.choice([-1, 0, 1])
                    dy = random.choice([-1, 0, 1])
                    # Verbleibe in Zoomauern (Grid-Bereich grob einschränken)
                    visitor.move_to(max(1, min(20, visitor.x + dx)), max(1, min(15, visitor.y + dy)))
            
            elif visitor.status == "Leaving":
                # Zum Ausgang laufen
                visitor.move_to(self.zoo_exit_pos[0], self.zoo_exit_pos[1])
                if (visitor.x, visitor.y) == self.zoo_exit_pos:
                    leaving_visitors.append(visitor)
                    events_occurred.append(f"Besucher {visitor.id} hat den Zoo verlassen.")

        for lv in leaving_visitors:
            if lv in self.visitors:
                self.visitors.remove(lv)

        # 6. Personal autonom agieren lassen
        for staff_member in self.staff:
            if isinstance(staff_member, Caretaker):
                # Finde das hungrigste Tier (< 100%)
                hungry_creatures = [c for c in self.creatures if c.hunger > 30.0]
                if hungry_creatures:
                    # Sortiere nach Hunger absteigend
                    hungry_creatures.sort(key=lambda x: x.hunger, reverse=True)
                    target = hungry_creatures[0]
                    staff_member.status = "Working"
                    staff_member.target_id = target.id
                    staff_member.move_to(target.x, target.y)
                    # Versuche zu füttern
                    staff_member.feed_animal(target)
                else:
                    staff_member.status = "Idle"
                    staff_member.target_id = None

            elif isinstance(staff_member, Vet):
                # Finde krankes Tier
                sick_creatures = [c for c in self.creatures if c.is_sick]
                if sick_creatures:
                    target = sick_creatures[0]
                    staff_member.status = "Working"
                    staff_member.target_id = target.id
                    staff_member.move_to(target.x, target.y)
                    # Versuche zu heilen
                    staff_member.heal_animal(target)
                else:
                    staff_member.status = "Idle"
                    staff_member.target_id = None

            elif isinstance(staff_member, Cashier):
                # Kassierer bleibt am Ticketschalter stehen
                staff_member.move_to(self.ticket_counter_pos[0], self.ticket_counter_pos[1])
                if queuing_visitors and queuing_visitors[0].status == "BuyingTicket":
                    staff_member.status = "Working"
                    staff_member.target_id = queuing_visitors[0].id
                else:
                    staff_member.status = "Idle"
                    staff_member.target_id = None

        return {"events": events_occurred}

    def buy_animal(self, species: str, name: str) -> Optional[Animal]:
        """
        Kauft ein neues Tier, falls genügend Geld vorhanden ist.

        :param species: Die Tierart.
        :param name: Der Name des Tieres.
        :return: Das neue Animal-Objekt oder None.
        """
        cost = 20  # Standard-Kosten für ein Tier
        if self.money >= cost:
            self.money -= cost
            new_animal = Animal(
                id_=str(uuid.uuid4())[:8],
                species=species,
                name=name,
                pos_x=random.randint(2, 18),
                pos_y=random.randint(2, 14)
            )
            self.creatures.append(new_animal)
            return new_animal
        return None

    def hire_staff(self, staff_type: str, name: str) -> Optional[Staff]:
        """
        Stellt Personal für 10$ ein.
        """
        cost = 10
        if self.money >= cost:
            self.money -= cost
            id_ = str(uuid.uuid4())[:8]
            pos_x, pos_y = 10, 8  # Spawn in der Mitte

            if staff_type == "Caretaker":
                new_member = Caretaker(id_, name, pos_x, pos_y)
            elif staff_type == "Vet":
                new_member = Vet(id_, name, pos_x, pos_y)
            elif staff_type == "Cashier":
                new_member = Cashier(id_, name, pos_x, pos_y)
            else:
                self.money += cost  # Rückerstattung bei falschem Typ
                return None

            self.staff.append(new_member)
            return new_member
        return None
