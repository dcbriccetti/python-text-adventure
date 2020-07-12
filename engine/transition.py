import engine.place
import engine.inventory_item


class Transition:
    '''
    A transition to another place, which may require possession of one or more inventory items.

    :param place: the place to which to transition
    :param must_have: zero or more inventory items the player
        must possess in order to make the transition
    '''
    def __init__(self, place: engine.place.Place, *must_have: engine.inventory_item.InventoryItem):
        self.place = place
        self.must_have = must_have

    def __str__(self) -> str:
        must_have = ', Must have: ' + ', '.join((mh.name for mh in self.must_have)) if self.must_have else ''
        return self.place.title + must_have
