from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @property
    def coordinates(self):
        return [self.x, self.y]

    @property
    def is_odd(self):
        return (self.x + self.y) % 2
