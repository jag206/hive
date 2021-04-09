from typing import Dict, Set, Tuple, Optional
import logging

import numpy as np

import hive.tiles

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s: %(message)s')
ch.setFormatter(formatter)
# uncomment the below to register the stream handler
# logger.addHandler(ch)


class Board:
    """
    Class encapsulating the underlying structure representing the board.
    Indexed by integers relative to the root, where x points along the
    north-east direction in the hexagonal structure, y points in the north
    direction in the hexagonal structure.
    """
    def __init__(self):
        self.grid = np.full((3, 3), None)
        self.root = (1, 1)

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

    def add_tile(self, tile: hive.tiles.Tile, index: Tuple[int, int]):
        inner_index = self._add(self.root, index)
        self.grid[inner_index] = tile
        self._maybe_resize_board(index)


class Player:
    def __init__(self, colour: hive.tiles.Colour):
        self.colour = colour
        self.unused_tiles: Dict[hive.tiles.Tile] = {
            hive.tiles.Bee(colour),
            hive.tiles.Ant(colour),
            hive.tiles.Ant(colour),
            hive.tiles.Ant(colour),
            hive.tiles.Spider(colour),
            hive.tiles.Spider(colour),
            hive.tiles.Spider(colour),
        }
        self.turn = 0
        self.bee_played = False

    def pretty(self) -> str:
        return ', '.join([str(tile) for tile in self.unused_tiles])


class Game:
    def __init__(self):
        self.active_player = Player(hive.tiles.Colour.WHITE)
        self.inactive_player = Player(hive.tiles.Colour.BLACK)
        self.board = Board()
        self.first_move = True

    def pretty(self) -> str:
        return (
            f"\nBoard:\n{self.root.pretty()}\n\n"
            f"Active Player: {self.active_player.pretty()}\n\n"
            f"Inactive Player: {self.inactive_player.pretty()}"
        )

    def add_tile(self, tile: hive.tiles.Tile, index: Tuple[int, int]):
        logger.debug(f"{tile} @ {index}")

        if self.first_move and index != (0, 0):
            raise RuntimeError("First move must be at the root")

        # check that a valid tile is being played
        if tile not in self.active_player.unused_tiles:
            raise RuntimeError("Can't add tile not on unused rack of active player")

        if not self.active_player.bee_played and self.active_player.turn >= 2 and type(tile) is not hive.tiles.Bee:
            raise RuntimeError("Bee must be played now")

        if self.board[index] is not None:
            raise RuntimeError("Cell is already occupied!")

        # skip the neighbour count check on the very first move only
        if not self.first_move:
            neighbour_count = sum(
                tile is not None for tile in self.board.neighbours(index)
            )
            if neighbour_count == 0:
                raise RuntimeError("Tile would be disconnected")

        if self.active_player.turn > 0:
            # check for opposing colour violation
            for neighbour in self.board.neighbours(index):
                if neighbour.colour != self.active_player.colour:
                    raise RuntimeError("Tile would be touching opposite colour.")

        # now actually make the move on the board
        self.board.add_tile(tile, index)

        # that succeeded, so now drop the tile from the user's rack
        self.active_player.unused_tiles.remove(tile)
        self.active_player.turn += 1
        if type(tile) is hive.tiles.Bee:
            self.active_player.bee_played = True

        # and now switch the active and passive player
        self.active_player, self.inactive_player = self.inactive_player, self.active_player

        self.first_move = False
