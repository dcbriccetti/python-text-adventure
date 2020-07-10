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

        home = Place('Home', 'You are at home.')
        wag_event = Event(0.7, 'Your dog wags its tail.', 5)
        lamp_event = Event(0.8, 'Your dog\'s tail knocks over a lamp.', -10, max_occurrences=2)
        fire_event = Event(0.3, 'The lamp starts a fire.', -1000)
        lamp_event.chain(fire_event)
        wag_event.chain(lamp_event)
        home.add_events(wag_event)
        coding_party_invitation = InventoryItem('Coding party invitation', acquire_probability=0.8)
        home.add_items(coding_party_invitation)

        library = Place('Library', 'You are at the library.')
        library.add_events(Event(.1, 'Someone talks loudly.', -10, max_occurrences=1))
        programming_book = InventoryItem('Programming Book', acquire_probability=0.5)
        library.add_items(programming_book)

        coding_party = Place('Coding Party', 'A group of interesting people has gathered to write code.')
        prize_event = Event(0.7, 'You win a prize for most obfuscated code', 50)
        code_prize = InventoryItem('Most Obfuscated Code Prize')
        prize_event.add_items(code_prize)
        coding_party.add_events(
            Event(0.6, 'Someone teaches you some Python', 20),
            Event(0.1, 'A mean person laughs at your code', -20),
            prize_event
        )

        home.add_transitions(library)
        home.add_activities(Activity('You celebrate your code prize', code_prize))
        library.add_transitions(home, Transition(coding_party, programming_book, coding_party_invitation))
        coding_party.add_transitions(library, home)

        self.location = home


game = Simple()
game.play()
