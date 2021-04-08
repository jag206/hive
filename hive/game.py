from dataclasses import dataclass
from enum import Enum
from typing import Sequence, Type, Optional

import hive.tiles


class Cell:
    def __init__(self):
        self.tile = None
        self.neighbours = None

    def pretty(self):
        return "Coming soon TM"

    def add_tile(self, tile: hive.tiles.Tile):
        if self.tile is not None:
            raise RuntimeError("Cell is already occupied!")

        self.tile = tile
        self.neighbours = [Cell()] * 6


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

class MoveType(Enum):
    ADD_TILE = 0
    MOVE_TILE = 1


@dataclass
class Move:
    """
    A class for encapsulating a move that a player wishes to play
    """
    move_type: MoveType
    tile_type: Type[hive.tiles.Tile]
    position: int


class Game:
    def __init__(self):
        self.active_player = Player(hive.tiles.Colour.WHITE)
        self.inactive_player = Player(hive.tiles.Colour.BLACK)
        self.board = Cell()

    def pretty(self) -> str:
        return (
            f"\nBoard:\n{self.board.pretty()}\n\n"
            f"Active Player: {self.active_player.pretty()}\n\n"
            f"Inactive Player: {self.inactive_player.pretty()}"
        )

    def add_tile(self, tile: hive.tiles.Tile, cell: Cell):
        # check that a valid move is being played
        if tile not in self.active_player.unused_tiles:
            raise RuntimeError("Can't add tile not on unused rack of active player")

        # now actually make the move on the board
        cell.add_tile(tile)

        # that succeeded, so now drop the tile from the user's rack
        self.active_player.unused_tiles.remove(tile)

        # and now switch the active and passive player
        self.active_player, self.inactive_player = self.inactive_player, self.active_player
