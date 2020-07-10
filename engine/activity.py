import engine.inventory_item


class Activity:
    def __init__(self, description: str, *must_have: engine.inventory_item.InventoryItem):
        self.description = description
        self.must_have = must_have
        self.events = []

    def add_events(self, *events):
        for event in events:
            self.events.append(event)
