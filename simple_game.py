from engine.game import Game, mt
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.event import Event
from engine.transition import Transition


class Simple(Game):
    def __init__(self):
        super(Simple, self).__init__()
        self.condition_description = 'Happiness'
        self.introduction = 'Welcome to A Simple Game'

        programming_book = InventoryItem('Programming Book', acquire_probability=0.5)

        home_events = (Event(0.5, "Your dog wags its tail.", 5),)
        home = Place('Home', "You are at home.", home_events)

        library_events = (Event(.1, 'Someone talks loudly', -10, max_occurrences=1),)
        library_items = (programming_book,)
        library = Place('Library', "You are at the library.", library_events, library_items)

        coding_party_events = (
            Event(0.6, 'Someone teaches you some Python', 20),
            Event(0.1, 'A mean person laughs at your code', -20),
        )
        coding_party = Place('Coding Party', 'A group of interesting people has gathered to write code.',
            coding_party_events)

        home.transitions = mt(library)
        library.transitions = (Transition(home), Transition(coding_party, (programming_book,)),)
        coding_party.transitions = mt(library, home)

        self.location = home


game = Simple()
game.play()
