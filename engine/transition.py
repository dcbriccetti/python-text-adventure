# from engine.place import Place  todo resolve circular import
from engine.inventory_item import InventoryItem


class Transition:
    def __init__(self, place, *must_have: InventoryItem):
        self.place = place
        self.must_have = must_have

    def __str__(self) -> str:
        must_have = ', Must have: ' + ', '.join((mh.name for mh in self.must_have)) if self.must_have else ''
        return self.place.title + must_have
