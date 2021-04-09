from typing import Optional, Set, Tuple
import logging
import numpy as np
import hive.tiles

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO(james.gunn): Remove mention of hive.tiles from this class, it should be
# a clean abstraction of a infinitely growable hexagonal board
class Board:
    """
    Class encapsulating the underlying structure representing the board.
    Indexed by integers relative to the root, where x points along the
    north-east direction in the hexagonal structure, y points in the north
    direction in the hexagonal structure.
    """
    def __init__(self):
        self.grid = np.full((1, 1), None)
        self.root = (0, 0)

    @staticmethod
    def _add(left: Tuple[int, int], right: Tuple[int, int]):
        return (left[0] + right[0], left[1] + right[1])

    def pretty(self):
        return "Coming soon TM"

    def __getitem__(self, index: Tuple[int, int]) -> Optional[hive.tiles.Tile]:
        inner_index = self._add(self.root, index)

        if inner_index[0] < 0 or inner_index[0] > self.grid.shape[0] - 1:
            return None

        if inner_index[1] < 0 or inner_index[1] > self.grid.shape[1] - 1:
            return None

        return self.grid[inner_index]

    def __setitem__(self, index: Tuple[int, int], tile: hive.tiles.Tile):
        inner_index = self._add(self.root, index)

        # trigger a resize if required
        padding = np.array([
            [max(-inner_index[0], 0), max(inner_index[0] - (self.grid.shape[0] - 1), 0)],
            [max(-inner_index[1], 0), max(inner_index[1] - (self.grid.shape[1] - 1), 0)],
        ], dtype=int)
        self.grid = np.pad(self.grid, padding, constant_values=None)
        self.root = self._add(self.root, (max(-inner_index[0], 0), max(-inner_index[1], 0)))

        new_inner_index = self._add(self.root, index)
        self.grid[new_inner_index] = tile

    def neighbours(self, index: Tuple[int, int]) -> Set[hive.tiles.Tile]:
        """
        Returns the neighbours of the specified cell., may be empty.

        Neighbours are not returned in any order.
        """
        neighbour_tiles: Set[hive.tiles.Tile] = set()
        neighbour_idxs = {
            self._add(index, (0, 1)),
            self._add(index, (1, 0)),
            self._add(index, (1, -1)),
            self._add(index, (0, -1)),
            self._add(index, (-1, 0)),
            self._add(index, (-1, 1)),
        }

        for neighbour_idx in neighbour_idxs:
            try:
                neighbour_tile = self[neighbour_idx]
            except IndexError:
                continue

            if neighbour_tile is not None:
                neighbour_tiles.add(neighbour_tile)

        return neighbour_tiles
