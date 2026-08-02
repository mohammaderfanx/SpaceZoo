"""
EventScheduler für SpaceZoo.
Verwaltet zeitgesteuerte Ereignisse und Callback-Registrierungen.
"""

from typing import Any, Callable, Dict, List


class EventScheduler:
    """
    Planer für zeitgesteuerte Events innerhalb der Zoo-Simulation.
    """

    def __init__(self) -> None:
        self.scheduled_events: List[Dict[str, Any]] = []

    def schedule_event(self, delay: float, callback: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """
        Plant ein Event, das nach einer Verzögerung von `delay` Sekunden ausgeführt wird.

        :param delay: Verzögerung in Sekunden.
        :param callback: Die aufzurufende Funktion.
        """
        self.scheduled_events.append({
            "time_remaining": delay,
            "callback": callback,
            "args": args,
            "kwargs": kwargs
        })

    def tick(self, delta_time: float) -> None:
        """
        Aktualisiert alle geplanten Events und führt abgelaufene Events aus.

        :param delta_time: Vergangene Zeit in Sekunden.
        """
        events_to_run = []
        remaining_events = []

        for event in self.scheduled_events:
            event["time_remaining"] -= delta_time
            if event["time_remaining"] <= 0.0:
                events_to_run.append(event)
            else:
                remaining_events.append(event)

        self.scheduled_events = remaining_events

        for event in events_to_run:
            event["callback"](*event["args"], **event["kwargs"])
