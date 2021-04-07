from typing import Sequence, Optional

import hive.tiles

class Cell:
    pass


class Board:
    def __init__(self):
        self.root: Optional[Cell] = None

    def pretty(self):
        return "Coming soon TM"


class Player:
    def __init__(self):
        self.unused_tiles: Sequence[Tile] = {
            hive.tiles.Bee(),
            hive.tiles.Ant(),
            hive.tiles.Ant(),
            hive.tiles.Ant(),
            hive.tiles.Spider(),
            hive.tiles.Spider(),
            hive.tiles.Spider(),
        }

    def pretty(self) -> str:
        return ', '.join([str(tile) for tile in self.unused_tiles])


class Game:
    def __init__(self):
        self.active_player = Player()
        self.inactive_player = Player()
        self.board = Board()

    def pretty(self) -> str:
        return (
            f"\nBoard:\n{self.board.pretty()}\n\n"
            f"Active Player: {self.active_player.pretty()}\n\n"
            f"Inactive Player: {self.inactive_player.pretty()}"
        )
