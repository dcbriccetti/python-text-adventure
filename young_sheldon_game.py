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
        sparkses = Place('Billy Sparks’s', 'Billy Sparks’s House')
        chicken_event = Event(0.3, 'Billy’s chicken scares you', -10)
        chicken_event.add_else_events(Event(1, 'Billy says something kind', 5))
        sparkses.add_events(chicken_event)

        # Meemaw’s
        meemaws = Place('Meemaw’s', 'Meemaw’s house')
        meemaws.add_events(Event(0.4, 'Meemaw makes cookies', 20))
        meemaws.add_events(Event(0.3, 'We play video games', 20))

        # University
        university = Place('University', 'Your university')

        # Dr. Sturgis’s class
        sturgis_class = Place('Dr. Sturgis’s class', 'Your front row seat in Dr. Sturgis’s class')

        # Dr. Linkletter’s office
        linkletter_office = Place('Linkletter’s office', 'Dr. Linkletter’s office')
        linkletter_office.add_events(Event(1, 'Dr. Linkletter is not happy to see you', -10))

        # Transitions
        home.add_transitions(meemaws, university, sparkses)
        meemaws.add_transitions(home)
        university.add_transitions(home, sturgis_class, linkletter_office)
        sturgis_class.add_transitions(university)
        linkletter_office.add_transitions(university)
        sparkses.add_transitions(home)

        # Starting place
        self.location = home


if __name__ == '__main__':
    game = YoungSheldon()
    game.play()
