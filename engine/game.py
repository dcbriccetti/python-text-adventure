from random import random, choice
from typing import Sequence, List
from engine.inventory_item import InventoryItem
from engine.transition import Transition
from engine.place import Place
from engine.event import Event


def _dump_event(event: Event, is_else, condition_description, level=1):
    else_msg = 'Else ' if is_else else ''
    print(('\t' * level) + else_msg + event.str(condition_description))
    for item in event.inventory_items:
        print(('\t' * (level + 1)) + f'Item: {item}')

    for event in event.else_events:
        _dump_event(event, True, condition_description, level + 1)

    for event in event.chained_events:
        _dump_event(event, False, condition_description, level + 1)


def _dump_place(condition_description, place: Place, explored: List[Place]):
    explored.append(place)
    print(place)

    for event in place.events:
        _dump_event(event, False, condition_description)

    for item in place.inventory_items:
        print(f'\tItem: {item}')

    for transition in place.transitions:
        print(f'\tTransition: {transition}')

    for activity in place.activities:
        print(f'\tActivity: {activity}')

    for transition in place.transitions:
        if transition.place not in explored:
            explored.append(transition.place)
            _dump_place(condition_description, transition.place, explored)


class Game:
    '''
    The main code for running the game. Extend this class for your game.
    See simple_game.py or ship_game.py for examples.
    '''

    def __init__(self):
        self.condition = 100
        self.condition_description = 'Health'
        self.inventory = []
        self.introduction = ''
        self.location = None

    def play(self):
        'Play the game.'
        print(self.introduction)
        last_location = None

        while True:
            if self.location != last_location:
                print()
                print(self.location.description)
                self._acquire_items()
                self._process_events()

                print(f'{self.condition_description}: {self.condition}, Items:',
                      ', '.join([i.name for i in self.inventory]) if self.inventory else 'None')
            last_location = self.location
            self._act_and_transition(self.location)

    def dump(self):
        'dump the contents of the game, without playing it.'
        print(self.introduction)
        _dump_place(self.condition_description, self.location, [])

    def _acquire_items(self):
        acquired_items = [i for i in self.location.inventory_items if random() < i.acquire_probability]
        for item in acquired_items:
            print('You found: ' + item.name)
            self.inventory.append(item)
            self.location.inventory_items.remove(item)

    def _process_events(self):
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

    def _available_activities(self, place: Place):
        return [a for a in place.activities if self._have_all(a.must_have)]

    def _act_and_transition(self, place: Place):
        activities = self._available_activities(place)
        transitions = self._available_transitions()
        print('Please choose: ')

        if activities:
            for (index, activity) in enumerate(activities):
                print(index + 1, activity.description)

        for (index, transition) in enumerate(transitions):
            print(len(activities) + index + 1, transition.place.title)

        choice_number = _get_numeric('Choose one, or enter 0 to exit: ', len(activities) + len(transitions))
        if choice_number == 0:
            exit(0)
        elif choice_number - 1 < len(activities):
            activity = activities[choice_number - 1]
            change = activity.run()
            print(f'({"+" if change > 0 else ""}{change})')
            self.condition += change
        else:
            self.location = transitions[choice_number - len(activities) - 1].place


def _get_numeric(prompt: str, highest: int):
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


def mt(*places: Place):
    'Make simple transitions to the specified places'
    return [Transition(place) for place in places]
