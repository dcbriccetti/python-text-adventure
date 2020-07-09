from random import random


class Event:
    'A game event, including the probability of its happening.'

    def __init__(self, probability: float, message: str, condition_change: int, max_occurrences: int = 100000):
        self.probability = probability
        self.message = message
        self.condition_change = condition_change
        self.remaining_occurrences = max_occurrences
        self.chained_events = []
        self.inventory_items = []

    def process(self, inventory) -> int:
        'Process the event, and return the change in condition, or 0.'

        condition_change_sum = 0
        if self.remaining_occurrences and random() < self.probability:
            self.remaining_occurrences -= 1
            print(self.message)
            condition_change_sum += self.condition_change
            for item in self.inventory_items:
                inventory.append(item)
            for event in self.chained_events:
                condition_change_sum += event.process(inventory)

        return condition_change_sum

    def add_items(self, *items):
        for item in items:
            self.inventory_items.append(item)

    def chain(self, *events):
        for event in events:
            self.chained_events.append(event)

    def __str__(self) -> str:
        return f'Event: {self.message}, Chance: {self.probability}, Condition: {self.condition_change}'

