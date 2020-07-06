from typing import Sequence
from engine.place import Place
from engine.inventory_item import InventoryItem


class Transition:
    def __init__(self, place: Place, must_have: Sequence[InventoryItem] = ()):
        self.place = place
        self.must_have = must_have
