from dataclasses import dataclass


@dataclass(repr=False)
class InventoryItem:
    name: str
    acquire_probability: float = 1

    'An object that can be acquired'

    def __str__(self):
        return f'{self.name}, Acquire probability: {self.acquire_probability}'

    def __repr__(self) -> str:
        return self.__str__()
