'A very simple example game using the text adventure engine.'
from engine.game import Game
from engine.place import Place


class VerySimple(Game):
    def __init__(self):
        super().__init__()
        self.introduction = 'Welcome to a Very Simple Game'

        # Home
        home = Place('Home', 'You are at home.')

        # School
        school = Place('School', 'You are at school.')

        # Transitions
        home.add_transitions(school, reverse=True)

        # Starting place
        self.location = home


if __name__ == '__main__':
    game = VerySimple()
    game.play()
