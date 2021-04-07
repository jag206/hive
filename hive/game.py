from typing import Sequence, Optional

import hive.tiles

class Cell:
    pass


class Board:
    def __init__(self):
        self.root: Optional[Cell] = None


class Player:
    def __init__(self):
        self.unused_tiles: Sequence[Tile] = set(

        )


class Game:
    def __init__(self):
        pass
