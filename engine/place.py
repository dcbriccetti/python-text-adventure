from typing import Sequence
from engine.event import Event
from engine.inventory_item import InventoryItem


class Place:
    'A place in the game, with a title, description, and events that can occur there.'

    def __init__(self, title: str, description: str, events: Sequence[Event] = (),
                 inventory_items: Sequence[InventoryItem] = ()):
        self.title = title
        self.description = description
        self.events = events
        self.inventory_items = list(inventory_items)
        self.transitions = []

    def __str__(self) -> str:
        return f'{self.title}: {self.description}'
