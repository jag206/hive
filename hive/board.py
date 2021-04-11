from typing import Generic, List, Optional, Set, Tuple, TypeVar
import logging
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

T = TypeVar("T")


class Board(Generic[T]):
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

    def __getitem__(self, index: Tuple[int, int]) -> Optional[T]:
        inner_index = self._add(self.root, index)

        if inner_index[0] < 0 or inner_index[0] > self.grid.shape[0] - 1:
            return None

        if inner_index[1] < 0 or inner_index[1] > self.grid.shape[1] - 1:
            return None

        return self.grid[inner_index]

    def __setitem__(self, index: Tuple[int, int], tile: T):
        # TODO(james.gunn): Check for assignment of None?
        inner_index = self._add(self.root, index)

        # trigger a resize if required
        pad_x_before = max(-inner_index[0], 0)
        pad_x_after = max(inner_index[0] - (self.grid.shape[0] - 1), 0)
        pad_y_before = max(-inner_index[1], 0)
        pad_y_after = max(inner_index[1] - (self.grid.shape[1] - 1), 0)
        padding = np.array([
            [pad_x_before, pad_x_after],
            [pad_y_before, pad_y_after],
        ], dtype=int)
        # pad the array to permit the required index to be inserted, note that
        # all pad values may be 0 which will not trigger a resize
        self.grid = np.pad(self.grid, padding, constant_values=None)
        # any padding added at the start of the grid cause a shift to the root
        self.root = self._add(self.root, (pad_x_before, pad_y_before))

        new_inner_index = self._add(self.root, index)
        self.grid[new_inner_index] = tile

    def __delitem__(self, index: Tuple[int, int]):
        # TODO(james.gunn): Might we want to shrink the board back down?
        inner_index = self._add(self.root, index)
        self.grid[inner_index] = None

    def connected_components(self) -> int:
        non_null_tile_idxs: List[Tuple[int, int]] = []
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                non_null_tile_idx = (x, y)
                if self.grid[non_null_tile_idx] is not None:
                    non_null_tile_idxs.append(non_null_tile_idx)

        def _expand(index: Tuple[int, int]):
            # check if we've already visited this tile and ignore it (to avoid
            # getting stuck in a loop). This works equally well for avoiding
            # cells that are actually null.
            if index not in non_null_tile_idxs:
                return

            non_null_tile_idxs.remove(index)
            neighbour_idxs = {
                self._add(index, (0, 1)),
                self._add(index, (1, 0)),
                self._add(index, (1, -1)),
                self._add(index, (0, -1)),
                self._add(index, (-1, 0)),
                self._add(index, (-1, 1)),
            }

            for neighbour_idx in neighbour_idxs:
                _expand(neighbour_idx)

        num_components = 0
        while len(non_null_tile_idxs) > 0:
            num_components += 1
            _expand(non_null_tile_idxs[0])

        return num_components

    def neighbours(self, index: Tuple[int, int]) -> Set[Tuple[Tuple[int, int], T]]:
        """
        Returns the neighbours of the specified cell., may be empty.

        Neighbours are not returned in any order.
        """
        neighbour_tiles: Set[T] = set()
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
                neighbour_tiles.add((neighbour_idx, neighbour_tile))

        return neighbour_tiles
