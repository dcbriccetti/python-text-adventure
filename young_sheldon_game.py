'Young Sheldon Adventure.'

from engine.game import Game
from engine.place import Place
from engine.event import Event


class YoungSheldon(Game):
    def __init__(self):
        super(YoungSheldon, self).__init__()
        self.condition_description = 'Happiness'
        self.introduction = 'Welcome to Young Sheldon Adventure'

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
            Event(0.3, 'We play video games', 20),
            Event(0.05, 'Meemaw is mad at you', -10),
        )

        # Sunday School
        sunday_school = Place('Sunday School')
        sunday_school.add_events(
            Event(0.2, 'Paige makes you mad', -20),
            Event(0.3, 'You win an argument with Pastor Jeff about the existence of God', 20),
            Event(0.1, 'Billy says something funny', 5),
        )

        # University
        university = Place('Your university')
        university.add_events(
            Event(0.1, 'Your mother embarrasses you', -5),
            Event(0.6, 'You are glad to be at your place of higher learning', 5),
        )

        # Dorm Room
        dorm_room = Place('Your Dorm Room')

        # Dr. Sturgis’s class
        sturgis_class = Place('Dr. Sturgis’s class', 'Your front row seat in Dr. Sturgis’s class')

        # Dr. Linkletter’s office
        linkletters_office = Place('Dr. Linkletter’s office')
        linkletters_office.add_events(Event(1, 'Dr. Linkletter is not happy to see you', -10))

        # Transitions
        home.add_transitions(meemaws, university, billys, sunday_school, reverse=True)
        university.add_transitions(dorm_room, sturgis_class, linkletters_office, reverse=True)

        # Starting place
        self.location = home


if __name__ == '__main__':
    game = YoungSheldon()
    game.play()
