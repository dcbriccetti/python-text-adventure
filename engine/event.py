from random import random
from dataclasses import dataclass, field

from engine.inventory_item import InventoryItem
from engine.player_attributes import PlayerAttributes, AttrsType


@dataclass
class Event:
    probability: float
    message: str
    flexible_condition_change: int | AttrsType
    max_occurrences: int = 100_000

    condition_change: PlayerAttributes = field(init=False)

    '''
    A game event, including the probability of its happening.

    :param probability: the probability the event will occur
    :param message: the text describing the event
    :param condition_change: how the event affects the player’s condition
    :param max_occurrences: a limit on the number of times the event may occur
    '''
    def __post_init__(self):
        self.remaining_occurrences = self.max_occurrences
        self.chained_events: list[Event] = []
        self.else_events: list[Event] = []
        self.inventory_items: list[InventoryItem] = []
        fcc: int | AttrsType = self.flexible_condition_change  # Shorter name
        attr = getattr(Event, 'default_attribute')
        chg = PlayerAttributes(fcc if isinstance(fcc, dict) else {attr: fcc})
        self.condition_change = chg

    def process(self, inventory: list[InventoryItem]) -> PlayerAttributes:
        '''
        Process the event.

        :param inventory: the player’s inventory, which may be changed by the event
        :return: the changes in condition
        '''
        attrs = PlayerAttributes()
        if self.remaining_occurrences and random() < self.probability:
            self.remaining_occurrences -= 1
            self._display_impact()
            attrs += self.condition_change
            for item in self.inventory_items:
                inventory.append(item)
            for event in self.chained_events:
                attrs += event.process(inventory)
        else:
            for event in self.else_events:
                attrs += event.process(inventory)

        return attrs

    def _display_impact(self):
        for condition, value in self.condition_change.items():
            change_sign = '+' if value > 0 else ''
            print(f'{self.message}   {condition}: {change_sign}{value}')

    def add_items(self, *items: InventoryItem):
        'Add one or more inventory items to this event.'
        for item in items:
            self.inventory_items.append(item)

    def chain(self, *events: 'Event'):
        'Chain one or more events to an event, so that if the event occurs, each of the chained events may also occur.'
        for event in events:
            self.chained_events.append(event)

    def add_else_events(self, *events: 'Event'):
        '''
        Add one or more “else” events to an event, so that if the event
        does not occur, each of the “else” events may occur.

        :param events: one or more “else” events
        '''
        for event in events:
            self.else_events.append(event)

    def __str__(self) -> str:
        return self.str("Condition")

    def str(self, condition_description: str) -> str:
        return f'Event: {self.message}, Chance: {self.probability}, {condition_description}: {self.condition_change}'
