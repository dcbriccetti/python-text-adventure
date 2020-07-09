from random import random, choice
from typing import Sequence, List
from engine.inventory_item import InventoryItem
from engine.transition import Transition
from engine.place import Place
from engine.event import Event


def _dump_event(event: Event, level = 1):
    print(('\t' * level) + str(event))
    for item in event.inventory_items:
        print(('\t' * (level + 1)) + f'Item: {item}')

    for event in event.chained_events:
        _dump_event(event, level + 1)


def _dump_place(place: Place, explored: List[Place]):
    explored.append(place)
    print(place)

    for event in place.events:
        _dump_event(event)

    for item in place.inventory_items:
        print(f'\tItem: {item}')

    for transition in place.transitions:
        print(f'\tTransition: {transition}')

    for transition in place.transitions:
        if transition.place not in explored:
            explored.append(transition.place)
            _dump_place(transition.place, explored)


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

    def dump(self):
        print(self.introduction)
        _dump_place(self.location, [])

    def acquire_items(self):
        acquired_items = [i for i in self.location.inventory_items if random() < i.acquire_probability]
        for item in acquired_items:
            print('You found: ' + item.name)
            self.inventory.append(item)
            self.location.inventory_items.remove(item)

    def process_events(self):
        for event in self.location.events:
            self.condition += event.process(self.inventory)
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
