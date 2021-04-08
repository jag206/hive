from dataclasses import dataclass
from enum import Enum
from typing import Sequence, Tuple, Type, Optional

import numpy as np

import hive.tiles


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
        self.first_move = True

    @staticmethod
    def _add(left: Tuple[int, int], right: Tuple[int, int]):
        return (left[0] + right[0], left[1] + right[1])

    def pretty(self):
        return "Coming soon TM"

    def add_tile(self, tile: hive.tiles.Tile, index: Tuple[int, int]):
        if self.first_move and index != (0, 0):
            raise RuntimeError("First move must be at the root")

        inner_index = self._add(self.root, index)

        # TODO(james.gunn): Should this check really be here - maybe it should
        # be at the game level?
        if self.grid[inner_index] is not None:
            raise RuntimeError("Cell is already occupied!")

        # TODO(james.gunn): Check that by adding this tile we aren't violating
        # the cell colour rule (ie. that all cells that touch this one must be
        # the same colour as the tile we are adding)

        self.grid[inner_index] = tile
        self.first_move = False


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

    def pretty(self) -> str:
        return ', '.join([str(tile) for tile in self.unused_tiles])


class Game:
    def __init__(self):
        self.active_player = Player(hive.tiles.Colour.WHITE)
        self.inactive_player = Player(hive.tiles.Colour.BLACK)
        self.board = Board()

    def pretty(self) -> str:
        return (
            f"\nBoard:\n{self.root.pretty()}\n\n"
            f"Active Player: {self.active_player.pretty()}\n\n"
            f"Inactive Player: {self.inactive_player.pretty()}"
        )

    def add_tile(self, tile: hive.tiles.Tile, index: Tuple[int, int]):
        # check that a valid tile is being played
        if tile not in self.active_player.unused_tiles:
            raise RuntimeError("Can't add tile not on unused rack of active player")

        # TODO(james.gunn): Implement the check that the bee has been played
        # before a player's third (fourth?) turn here

        # now actually make the move on the board
        self.board.add_tile(tile, index)

        # that succeeded, so now drop the tile from the user's rack
        self.active_player.unused_tiles.remove(tile)

        # and now switch the active and passive player
        self.active_player, self.inactive_player = self.inactive_player, self.active_player
