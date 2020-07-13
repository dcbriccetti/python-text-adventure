import engine.inventory_item


class Activity:
    '''
    An activity that may be available in a place.
    '''
    def __init__(self, description: str, action, *must_have: engine.inventory_item.InventoryItem):
        self.description = description
        self.action = action
        self.must_have = must_have

    def run(self):
        self.action()
