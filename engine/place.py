from typing import Sequence
from engine.transition import Transition
from engine.event import Event
from engine.inventory_item import InventoryItem


class Place:
    'A place in the game, with a title, description, and events that can occur there.'

    def __init__(self, title: str, description: str, events: Sequence[Event] = (),
                 inventory_items: Sequence[InventoryItem] = ()):
        self.title = title
        self.description = description
        self.events = list(events)
        self.inventory_items = list(inventory_items)
        self.transitions = []

    def add_events(self, *events: Event):
        for event in events:
            self.events.append(event)

    def add_items(self, *items: InventoryItem):
        for item in items:
            self.inventory_items.append(item)

    def add_transitions(self, *transitions):
        for t in transitions:
            if isinstance(t, Transition):
                self.transitions.append(t)
            elif isinstance(t, Place):
                self.transitions.append(Transition(t))

    def __str__(self) -> str:
        return f'{self.title}: {self.description}'
