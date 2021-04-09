from enum import Enum


class Colour(Enum):
    WHITE = 0
    BLACK = 1


class Tile:
    def __init__(self, colour: Colour):
        self.colour = colour

    def _emoji(self) -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self._emoji()


class Bee(Tile):
    def _emoji(self) -> str:
        return "🐝"


class Ant(Tile):
    def _emoji(self) -> str:
        return "🐜"


class Spider(Tile):
    def _emoji(self) -> str:
        return "🕷️"


class Beetle(Tile):
    def _emoji(self) -> str:
        return "Beetle"


class Grasshopper(Tile):
    def _emoji(self) -> str:
        return "🦗"
