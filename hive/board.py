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

    def _maybe_resize_board(self, latest_index: Tuple[int, int]):
        logger.debug("Considering board resize")
        neighbours = [
            self._add(latest_index, (0, 1)),
            self._add(latest_index, (1, 0)),
            self._add(latest_index, (1, -1)),
            self._add(latest_index, (0, -1)),
            self._add(latest_index, (-1, 0)),
            self._add(latest_index, (-1, 1)),
        ]
        logger.debug(f"Neighbours: {', '.join([str(neighbour) for neighbour in neighbours])}")

        grid_shape = self.grid.shape
        min_x, max_x = (-self.root[0], (grid_shape[0] - 1) - self.root[0])
        min_y, max_y = (-self.root[1], (grid_shape[1] - 1) - self.root[1])
        logger.debug(f"(min_x, max_x)=({min_x}, {max_x})")
        logger.debug(f"(min_y, max_y)=({min_y}, {max_y})")

        expansion_required = False
        for neighbour in neighbours:
            if neighbour[0] < min_x or neighbour[0] > max_x:
                logger.debug(f"{neighbour} requires an expansion")
                expansion_required = True

            if neighbour[1] < min_y or neighbour[1] > max_y:
                logger.debug(f"{neighbour} requires an expansion")
                expansion_required = True

        if not expansion_required:
            return

        # add 1 element to the start and end of the grid in each dimension
        # and fill it with None
        self.grid = np.pad(self.grid, (1, 1), constant_values=None)

        # modify the root accordingly
        self.root = self._add(self.root, (1, 1))

        logger.debug(f"New grid shape: {self.grid.shape}")
        logger.debug(f"New root: {self.root}")

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
        self.grid[inner_index] = tile
        self._maybe_resize_board(index)

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
