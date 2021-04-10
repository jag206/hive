from enum import Enum
from typing import Sequence, Tuple

import hive.board


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

    def valid_moves(self, index: Tuple[int, int], board: hive.board.Board) -> Sequence[Tuple[int, int]]:
        """
        Takes in the board and the current position of this tile and returns the possible destination indices of this
        tile.
        """
        raise NotImplementedError()


class Bee(Tile):
    def _emoji(self) -> str:
        return "🐝"

    def valid_moves(self, index: Tuple[int, int], board: hive.board.Board) -> Sequence[Tuple[int, int]]:
        return []


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
