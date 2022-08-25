from random import random
from dataclasses import dataclass
from engine.inventory_item import InventoryItem


@dataclass
class Event:
    probability: float
    message: str
    condition_change: int | dict[str, float | int]
    max_occurrences: int = 100_000

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

    def process(self, inventory: list[InventoryItem]) -> int:
        '''
        Process the event.

        :param inventory: the player’s inventory, which may be changed by the event
        :return: the change in condition, or 0
        '''
        condition_change_sum = 0
        if self.remaining_occurrences and random() < self.probability:
            self.remaining_occurrences -= 1
            change_sign = '+' if self.condition_change > 0 else ''
            print(f'{self.message} ({change_sign}{self.condition_change})')
            condition_change_sum += self.condition_change
            for item in self.inventory_items:
                inventory.append(item)
            for event in self.chained_events:
                condition_change_sum += event.process(inventory)
        else:
            for event in self.else_events:
                condition_change_sum += event.process(inventory)

        return condition_change_sum

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
