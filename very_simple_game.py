'A very simple example game using the text adventure engine.'

from engine.game import Game
from engine.place import Place


class VerySimple(Game):
    def __init__(self):
        super(VerySimple, self).__init__()
        self.condition_description = 'Health'
        self.introduction = 'Welcome to a Very Simple Game'

        # Home
        home = Place('Home', 'You are at home.')

        # School
        school = Place('School', 'You are at school.')

        # Transitions
        home.add_transitions(school)
        school.add_transitions(home)

        # Starting place
        self.location = home


if __name__ == '__main__':
    game = VerySimple()
    game.play()
