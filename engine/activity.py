from engine.inventory_item import InventoryItem


class Activity:
    '''
    An activity, offered in a place. Unlike events, which happen automatically,
    activities are offered to the player.

    :param description: a description of the activity
    :param action: a function that implements the activity
    :param must_have: zero or items that must be in the inventory in order for this activity to be offered
    '''
    def __init__(self, description: str, action, *must_have: InventoryItem):
        self.description = description
        self.action = action
        self.must_have = must_have

    def run(self) -> int:
        return self.action()

    def __repr__(self) -> str:
        return self.description
