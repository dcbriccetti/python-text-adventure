'An example game using the text adventure engine.'

from random import randint
from engine.game import Game
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.activity import Activity
from engine.event import Event
from engine.player_attributes import PlayerAttributes
from engine.transition import Transition


class ShipGame(Game):
    def __init__(self):
        super().__init__()
        self.friend_visits = 0
        self.introduction = 'Welcome to Ship Adventure. You are the captain of a star ship.'
        self.attributes = PlayerAttributes({
            'Health'     : 100,
        })

        bridge = Place('Bridge',
            "You are on the bridge of a spaceship, sitting in the captain's chair.", [
                Event(0.01, 'Oh, no! An intruder beams onto the bridge and shoots you.', -50, max_occurrences=1),
                Event(0.1, "The ship's doctor gives you a health boost.", 30),
            ])

        ready_room = Place('Ready Room', "You are in the captain's ready room.", [
            Event(.5, 'The fish in the aquarium turn to watch you', 0, max_occurrences=1),
        ])

        lift = Place('Lift', 'You have entered the turbolift.', [
            Event(.1, "The ship's android says hello to you.", 1),
        ])

        lounge = Place('Lounge', 'Welcome to the lounge.', [
            Event(1, 'Relaxing in the lounge improves your health.', 10),
        ])
        lounge.add_activities(Activity('Visit with some friends', self.visit_friends))

        space_suit = InventoryItem('Spacesuit')

        storage_room = Place('Storage Room', 'You enter the storage room',
            inventory_items=[space_suit])

        transporter_room = Place('Transporter Room',
            'The transporter room looks cool with all its blinking lights and sliders.')

        planet = Place('Planet', 'You have beamed down to the planet.', [
            Event(.3, 'You found the experience relaxing', +10),
        ])

        bridge          .add_transitions(ready_room, lift, reverse=True)
        lift            .add_transitions(lounge, storage_room, transporter_room, reverse=True)
        transporter_room.add_transitions(Transition(planet, space_suit), reverse=True)

        self.location = bridge

    def visit_friends(self):
        self.friend_visits += 1
        if self.friend_visits > randint(2, 3):
            print('Your friends are tired of you')
            change = -5
        else:
            print('You visit with friends and have a few laughs')
            change = 10
        return change


if __name__ == '__main__':
    game = ShipGame()
    game.play()
