from random import random, choice
from typing import Sequence
from engine.inventory_item import InventoryItem
from engine.transition import Transition


class Game:
    'The main code for running the game. Extend this class for your game. See simple_game.py or shipgame.py for examples.'

    def __init__(self):
        self.condition = 100
        self.condition_description = 'Health'
        self.inventory = []
        self.introduction = ''
        self.location = None

    def play(self):
        print(self.introduction)

        while True:
            print()
            print(self.location.description)
            self.acquire_items()
            self.process_events()

            print(f'{self.condition_description}: {self.condition}, Items:',
                  ', '.join([i.name for i in self.inventory]) if self.inventory else 'None')
            self._transition()

    def acquire_items(self):
        acquired_items = [i for i in self.location.inventory_items if random() < i.acquire_probability]
        for item in acquired_items:
            print('You found: ' + item.name)
            self.inventory.append(item)
            self.location.inventory_items.remove(item)

    def process_events(self):
        for event in self.location.events:
            self.condition += event.process()
            if self.condition <= 0:
                goodbyes = ("That's it for you!", 'You lose.', 'So long.')
                print(choice(goodbyes))
                exit(1)

    def _have_all(self, must_have: Sequence[InventoryItem]):
        missing = [mh for mh in must_have if mh not in self.inventory]
        return not missing

    def _available_transitions(self):
        return [t for t in self.location.transitions if self._have_all(t.must_have)]

    def _transition(self):
        transitions = self._available_transitions()
        print('You can go to these places:')
        for (index, transition) in enumerate(transitions):
            print(index + 1, transition.place.title)

        choice_number = get_numeric('Choose one, or enter 0 to exit: ', len(transitions))
        if choice_number:
            self.location = transitions[choice_number - 1].place
        else:
            exit(0)


def get_numeric(prompt: str, highest: int):
    while True:
        response = input(prompt)
        try:
            int_response = int(response)
            if int_response > highest or int_response < 0:
                print(f'Please enter a number between 0 and {highest}')
            else:
                return int_response
        except ValueError:
            print("Please enter a number.")


def mt(*places):
    'Make simple transitions to the specified places'
    return [Transition(place) for place in places]
