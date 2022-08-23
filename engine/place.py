from typing import List, Sequence, Union
import engine.transition
from engine.event import Event
from engine.inventory_item import InventoryItem
from engine.activity import Activity


class Place:
    '''
    A place in the game, with a title, description, and events that can occur there.

    :param title: A short name for the place
    :param description: A longer description—very long if you like—of the place
    :param events: An optional sequence of events that may happen at the place.
        Instead of providing events here, you might call the add_events method.
    :param inventory_items: An optional sequence of inventory items.
        Instead of providing items here, you might call the add_items method.
    '''

    def __init__(self, title: str, description=None, events: Sequence[Event] = (),
                 inventory_items: Sequence[InventoryItem] = ()):
        self.title = title
        self.description = description if description else title
        self.events = list(events)
        self.inventory_items = list(inventory_items)
        self.transitions: List[engine.transition.Transition] = []
        self.activities: List[Activity] = []

    def add_events(self, *events: Event):
        'Add one or more events to this place.'
        for event in events:
            self.events.append(event)

    def add_items(self, *items: InventoryItem):
        'Add one or more inventory items to this place.'
        for item in items:
            self.inventory_items.append(item)

    def add_activities(self, *activities: Activity):
        for activity in activities:
            self.activities.append(activity)

    def add_transitions(self, *targets: Union['Place', 'engine.transition.Transition'], reverse=False):
        '''
        Add one or more transitions from this place to other places.

        :param targets: a sequence of either ``Place`` or ``Transition`` objects
        :param reverse: whether to add a transitions in the opposite direction from places specified
        '''
        for target in targets:
            if isinstance(target, engine.transition.Transition):
                self.transitions.append(target)
                if reverse:
                    target.place.add_transitions(self)
            elif isinstance(target, Place):
                self.transitions.append(engine.transition.Transition(target))
                if reverse:
                    target.add_transitions(self)

    def __str__(self) -> str:
        return f'{self.title}: {self.description}'
