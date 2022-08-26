'Young Sheldon Adventure.'
from random import randint
from time import sleep

from engine.activity import Activity
from engine.game import Game
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.event import Event
from engine.player_attributes import PlayerAttributes
from engine.transition import Transition


class YoungSheldon(Game):
    introduction: str
    attributes: PlayerAttributes

    def __init__(self):
        super().__init__('Happiness')
        self.introduction = 'Welcome to Young Sheldon Adventure'
        self.attributes = PlayerAttributes({
            'Health'      : 100,
            'Happiness'   : 100,
            'Gaming Skill':   0,
            'Confidence'  : 100,
        })

        home: Place = self._define_game()
        self.location = home

    def _define_game(self) -> Place:
        # Home
        home = Place('Home', 'You are at home.')
        relaxation_event = Event(0.75, 'You play with your trains.', 5)
        relaxation_event.add_else_events(Event(1, 'Missy plays loud sad music.', -20))
        feynman_poster_event = Event(0.3, 'You talk to your Richard Feynman poster', 10)
        home.add_events(relaxation_event, feynman_poster_event)

        # Billy Sparks’s house
        billys = Place('Billy Sparks’s House')
        chicken_event = Event(0.3, 'Billy’s chicken scares you', -10)
        chicken_event.add_else_events(Event(1, 'Billy says something kind', 5))
        billys.add_events(chicken_event)

        # Meemaw’s
        meemaws = Place('Meemaw’s house')
        meemaws.add_events(
            Event(0.4, 'Meemaw makes cookies', 20),
            Event(0.3, 'We play video games', {'Gaming Skill': 10}),
            Event(0.05, 'Meemaw is mad at you', -10),
        )

        # Sunday School
        sunday_school = Place('Sunday School')
        sunday_school.add_events(
            Event(0.2, 'Paige makes you mad', -20),
            Event(0.3, 'You win an argument with Pastor Jeff', {'Confidence': 20}),
            Event(0.2, 'Billy says something funny', 5),
        )

        # University
        university = Place('East Texas Tech')
        university.add_events(
            Event(0.1, 'Your mother embarrasses you', -5),
            Event(0.6, 'You are glad to be at your place of higher learning', 5),
        )

        # President Hagemeyer’s Office
        key = InventoryItem('Private dorm room key')
        hagemeyers = Place('President Hagemeyer’s Office', inventory_items=[key])

        # Dorm Room
        dorm_room = Place('Your Dorm Room', events=[Event(0.9, 'You have a nice rest', 15)])

        # Friends’ Dorm Room
        friends_dorm_room = Place('Oscar and Darren’s Dorm Room')
        friends_dorm_room.add_events(
            Event(0.3, 'Paige drops by and bums everybody out', -10, max_occurrences=1),
            Event(0.2, 'You eat too much junk food and barf', -20),
        )
        friends_dorm_room.add_activities(Activity('Play video games', self.play_video_games))

        # Dr. Sturgis’s class
        sturgis_class = Place('Dr. Sturgis’s class', 'Your front row seat in Dr. Sturgis’s class')

        # Dr. Linkletter’s office
        linkletters_office = Place('Dr. Linkletter’s office')
        linkletters_office.add_events(Event(1, 'Dr. Linkletter is not happy to see you', -10))

        # Transitions
        home.add_transitions(meemaws, university, billys, sunday_school, reverse=True)
        university.add_transitions(hagemeyers, sturgis_class, linkletters_office, reverse=True)
        university.add_transitions(Transition(dorm_room, key), Transition(friends_dorm_room, key), reverse=True)

        return home

    def play_video_games(self):
        happiness_change = randint(-10, 20)  # You’re more likely to win
        print('You sit down and take the controller.')
        sleep(1.5)
        print('You', 'won!' if happiness_change > 0 else 'lost.' if happiness_change < 0 else 'tied')
        return happiness_change


if __name__ == '__main__':
    game = YoungSheldon()
    game.play()
