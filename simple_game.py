'A simple example game using the text adventure engine.'

from engine.activity import Activity
from engine.game import Game
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.event import Event
from engine.transition import Transition


class Simple(Game):
    def __init__(self):
        super(Simple, self).__init__()
        self.condition_description = 'Happiness'
        self.introduction = 'Welcome to Coding Party'

        # Home
        home = Place('Home', 'You are at home.')
        relaxation_event = Event(0.75, 'Being at home relaxes you.', 5)
        relaxation_event.add_else_events(Event(1, 'A neighbor\'s leaf blower bothers you.', -20))
        wag_event = Event(0.7, 'Your dog wags its tail.', 5)
        lamp_event = Event(0.5, 'Your dog\'s tail knocks over a lamp.', -10, max_occurrences=2)
        fire_event = Event(0.3, 'The lamp starts a fire.', -1000)
        home.add_events(relaxation_event)
        # The following events are chained together
        home.add_events(wag_event)    # The dog might wag its tail
        wag_event.chain(lamp_event)   # which could cause the lamp event
        lamp_event.chain(fire_event)  # which could cause a fire
        coding_party_invitation = InventoryItem('Coding party invitation', acquire_probability=0.8)
        home.add_items(coding_party_invitation)

        # Math Circle
        math_circle = Place('Math Circle', 'A fun place to do math')
        math_circle.add_activities(Activity('Solve a math problem', self.solve_math_problem))

        # Library
        library = Place('Library', 'You are at the library.')
        library.add_events(Event(.1, 'Someone talks loudly.', -10, max_occurrences=1))
        programming_book = InventoryItem('Programming Book', acquire_probability=0.8)
        library.add_items(programming_book)

        # Coding Party
        coding_party = Place('Coding Party', 'A group of interesting people has gathered to write code.')
        prize_event = Event(0.7, 'You win a prize for most obfuscated code', 50)
        code_prize = InventoryItem('Most Obfuscated Code Prize')
        prize_event.add_items(code_prize)
        coding_party.add_events(
            Event(0.6, 'Someone teaches you some Python', 20),
            Event(0.1, 'A mean person laughs at your code', -20),
            prize_event
        )

        # Transitions
        home.add_transitions(math_circle, library)
        math_circle.add_transitions(home)
        library.add_transitions(home, Transition(coding_party, programming_book, coding_party_invitation))
        coding_party.add_transitions(library, home)

        # Starting place
        self.location = home

    def solve_math_problem(self):
        from random import randint
        m1 = randint(2,5)
        m2 = randint(11,19)
        product = m1 * m2
        answer = int(input(f'{m1} * {m2} = ? '))
        change = 10
        if answer == product:
            print('Right!')
        else:
            print('Oops!')
            change = -2
        return change

if __name__ == '__main__':
    game = Simple()
    game.play()
