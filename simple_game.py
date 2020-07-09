from engine.game import Game
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.event import Event
from engine.transition import Transition


class Simple(Game):
    def __init__(self):
        super(Simple, self).__init__()
        self.condition_description = 'Happiness'
        self.introduction = 'Welcome to A Simple Game'

        home = Place('Home', "You are at home.")
        home.add_events(Event(0.5, "Your dog wags its tail.", 5))
        coding_party_invitation = InventoryItem('Coding party invitation', acquire_probability=0.8)
        home.add_items(coding_party_invitation)

        library = Place('Library', "You are at the library.")
        library.add_events(Event(.1, 'Someone talks loudly', -10, max_occurrences=1))
        programming_book = InventoryItem('Programming Book', acquire_probability=0.5)
        library.add_items(programming_book, coding_party_invitation)

        coding_party = Place('Coding Party', 'A group of interesting people has gathered to write code.')
        coding_party.add_events(
            Event(0.6, 'Someone teaches you some Python', 20),
            Event(0.1, 'A mean person laughs at your code', -20)
        )

        home.add_transitions(library)
        library.add_transitions(home, Transition(coding_party, programming_book, coding_party_invitation))
        coding_party.add_transitions(library, home)

        self.location = home


game = Simple()
game.play()
