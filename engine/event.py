from random import random


class Event:
    'A game event, including the probability of its happening.'

    def __init__(self, probability: float, message: str, health_change: int, max_occurrences: int = 100000):
        self.probability = probability
        self.message = message
        self.health_change = health_change
        self.remaining_occurrences = max_occurrences

    def process(self) -> int:
        'Process the event, and return the change in health, or 0.'

        if self.remaining_occurrences and random() < self.probability:
            self.remaining_occurrences -= 1
            print(self.message)
            return self.health_change

        return 0

    def __str__(self) -> str:
        return f'Event: {self.message}, Chance: {self.probability}, condition: {self.health_change}'

