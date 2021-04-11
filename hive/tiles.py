from enum import Enum
from typing import Set, Tuple
import logging

import hive.board

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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

    def valid_moves(self, index: Tuple[int, int], board: hive.board.Board) -> Set[Tuple[int, int]]:
        """
        Takes in the board and the current position of this tile and returns the possible destination indices of this
        tile.
        """
        raise NotImplementedError()


class Bee(Tile):
    @staticmethod
    def _add(left: Tuple[int, int], right: Tuple[int, int]):
        return (left[0] + right[0], left[1] + right[1])

    @staticmethod
    def _subtract(left: Tuple[int, int], right: Tuple[int, int]):
        return (left[0] - right[0], left[1] - right[1])

    @staticmethod
    def _relative_idx(position: int) -> Tuple[int, int]:
        if position == 0:
            return (0, 1)
        elif position == 1:
            return (1, 0)
        elif position == 2:
            return (1, -1)
        elif position == 3:
            return (0, -1)
        elif position == 4:
            return (-1, 0)
        elif position == 5:
            return (-1, 1)

        raise ValueError()

    @staticmethod
    def _position(index: Tuple[int, int]) -> int:
        if index == (0, 1):
            return 0
        elif index == (1, 0):
            return 1
        elif index == (1, -1):
            return 2
        elif index == (0, -1):
            return 3
        elif index == (-1, 0):
            return 4
        elif index == (-1, 1):
            return 5

        raise ValueError()

    def _emoji(self) -> str:
        return "🐝"

    def valid_moves(self, index: Tuple[int, int], board: hive.board.Board) -> Set[Tuple[int, int]]:
        valid_moves = set()
        neighbours = board.neighbours(index)
        relative_idxs = [self._subtract(neighbour_idx, index) for neighbour_idx, _ in neighbours]

        def check_single_move(relative_idx: Tuple[int, int]):
            position = self._position(relative_idx)
            if self._relative_idx((position + 1) % 6) not in relative_idxs and self._relative_idx((position + 2) % 6) not in relative_idxs:
                valid_moves.add(self._relative_idx((position + 1) % 6))
            if self._relative_idx((position - 1) % 6) not in relative_idxs and self._relative_idx((position - 2) % 6) not in relative_idxs:
                valid_moves.add(self._relative_idx((position - 1) % 6))

        for relative_idx in relative_idxs:
            check_single_move(relative_idx)

        return valid_moves


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
