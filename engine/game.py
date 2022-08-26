from random import random
from time import sleep
from typing import Sequence

from colorama import Fore, init as init_colorama

from engine.color import colored, bright
from engine.activity import Activity
from engine.event import Event
from engine.inventory_item import InventoryItem
from engine.player_attributes import PlayerAttributes
from engine.transition import Transition
from engine.place import Place
from engine.dumper import dump_place


class Game:
    '''
    The main code for running the game. Extend this class for your game.
    See simple_game.py or ship_game.py for examples.
    '''

    def __init__(self, default_attribute='Health'):
        self.condition = 100
        self.attributes = PlayerAttributes({})
        self.inventory = []
        self.introduction = ''
        self.location = None
        init_colorama()
        Event.default_attribute = default_attribute

    def play(self):
        'Play the game.'
        print(bright(self.introduction))
        sleep(0.5)
        last_location = None

        while True:
            print()
            print(bright(self.location.description))
            if self.location != last_location:
                self._acquire_items()
                self._process_events()

            print(self.attributes)
            print(f'Items:',
                ', '.join([i.name for i in self.inventory]) if self.inventory else 'None')
            last_location = self.location
            self._act_and_transition(self.location)

    def dump(self):
        'dump the contents of the game, without playing it.'
        print(self.introduction)
        dump_place(self.location, [])

    def _acquire_items(self):
        acquired_items = [i for i in self.location.inventory_items if random() < i.acquire_probability]
        for item in acquired_items:
            print('You find: ' + item.name)
            self.inventory.append(item)
            self.location.inventory_items.remove(item)
            sleep(0.5)

    def _process_events(self):
        for event in self.location.events:
            self.attributes += event.process(self.inventory)
            sleep(0.5)

    def _have_all(self, must_have_items: Sequence[InventoryItem]) -> bool:
        for item in must_have_items:
            if item not in self.inventory:
                return False
        return True

    def _available_transitions(self) -> list[Transition]:
        return [t for t in self.location.transitions if self._have_all(t.must_have)]

    def _available_activities(self, place: Place) -> list[Activity]:
        return [a for a in place.activities if self._have_all(a.must_have)]

    def _act_and_transition(self, place: Place) -> None:
        activities = self._available_activities(place)
        transitions = self._available_transitions()
        print('\nPlease choose: ')

        for index, activity in enumerate(activities):
            print(colored(Fore.GREEN, str(index + 1)), activity.description)

        for index, transition in enumerate(transitions):
            print(colored(Fore.GREEN, str(len(activities) + index + 1)), transition.place.title)

        choice_number = _get_numeric('Choose one, or enter 0 to exit: ', len(activities) + len(transitions))
        if choice_number == 0:
            exit(0)
        elif choice_number - 1 < len(activities):
            print()
            activity = activities[choice_number - 1]
            change = activity.run()
            if isinstance(change, int):
                print(f'({"+" if change > 0 else ""}{change})')
                self.attributes += {getattr(Event, 'default_attribute'): change}
        else:
            self.location = transitions[choice_number - len(activities) - 1].place


def _get_numeric(prompt: str, highest: int) -> int:
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
