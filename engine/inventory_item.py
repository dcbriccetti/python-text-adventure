class InventoryItem:
    'An object that can be acquired'

    def __init__(self, name: str, acquire_probability: float = 1):
        self.name = name
        self.acquire_probability = acquire_probability

    def __str__(self):
        return self.name
