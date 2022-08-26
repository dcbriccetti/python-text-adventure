from dataclasses import dataclass, field

AttrsType = dict[str, int | float]


@dataclass
class PlayerAttributes:
    attribs: AttrsType = field(default_factory=dict)

    def __iadd__(self, other: 'PlayerAttributes'):
        if not other:
            return
        for k, v in other.items():
            if k in self.attribs:
                self.attribs[k] += v
            else:
                self.attribs[k] = v
        return self

    def items(self):
        return self.attribs.items()

    def __str__(self):
        return ', '.join(f'{name}: {value}' for name, value in self.attribs.items())
