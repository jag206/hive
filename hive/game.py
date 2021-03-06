from typing import Set, Tuple, Type
import logging

import hive.board
import hive.tiles

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s: %(message)s')
ch.setFormatter(formatter)
# uncomment the below to register the stream handler
# logger.addHandler(ch)


class HiveError(RuntimeError):
    pass


class DisconnectedHiveError(HiveError):
    pass


class InvalidMoveError(HiveError):
    pass


class Player:
    def __init__(self, colour: hive.tiles.Colour):
        self.colour = colour
        self.unused_tiles: Set[hive.tiles.Tile] = {
            hive.tiles.Bee(colour),
            hive.tiles.Beetle(colour),
            hive.tiles.Ant(colour),
            hive.tiles.Ant(colour),
            hive.tiles.Ant(colour),
            hive.tiles.Spider(colour),
            hive.tiles.Spider(colour),
            hive.tiles.Spider(colour),
            hive.tiles.Grasshopper(colour),
            hive.tiles.Grasshopper(colour),
            hive.tiles.Grasshopper(colour),
        }
        self.turn = 0
        self.bee_played = False

    def pretty(self) -> str:
        return ', '.join([str(tile) for tile in self.unused_tiles])


class Game:
    def __init__(self):
        self.active_player = Player(hive.tiles.Colour.WHITE)
        self.inactive_player = Player(hive.tiles.Colour.BLACK)
        self.board = hive.board.Board[hive.tiles.Tile]()
        self.first_move = True

    def pretty(self) -> str:
        return (
            f"\nBoard:\n{self.board.pretty()}\n\n"
            f"Active Player: {self.active_player.pretty()}\n\n"
            f"Inactive Player: {self.inactive_player.pretty()}"
        )

    def move_tile(self, from_index: Tuple[int, int], to_index: Tuple[int, int]):
        if not self.active_player.bee_played:
            raise RuntimeError("Cannot move piece until bee played")

        if self.board[from_index] is None:
            raise RuntimeError("Cannot move piece from empty tile")

        if self.board[to_index] is not None:
            raise RuntimeError("Cannot move piece to non-empty tile")

        if self.board[from_index].colour != self.active_player.colour:
            raise RuntimeError("Cannot move opponent's piece")

        tile = self.board[from_index]

        # remove the specified piece from the board and check connected
        # components
        del self.board[from_index]
        is_disconnected = self.board.connected_components() > 1
        self.board[from_index] = tile

        if is_disconnected:
            raise DisconnectedHiveError("Moving tile would disconnect hive")

        # TODO(james.gunn): Once all tiles have their valid moves implemented
        # we can swap the order of this check with the above
        if to_index not in tile.valid_moves(from_index, self.board):
            raise InvalidMoveError()

        self.board[to_index] = self.board[from_index]
        del self.board[from_index]

        # that succeeded, so now switch turns
        self.active_player.turn += 1
        self.active_player, self.inactive_player = self.inactive_player, self.active_player

    def _disconnect_check(self, index: Tuple[int, int]):
        neighbour_count = sum(
            tile is not None for tile in self.board.neighbours(index)
        )
        if neighbour_count == 0:
            raise RuntimeError("Tile would be disconnected")

    def _opposing_color_violation_check(self, index: Tuple[int, int]):
        # check for opposing colour violation
        for _, neighbour in self.board.neighbours(index):
            if neighbour.colour != self.active_player.colour:
                raise RuntimeError("Tile would be touching opposite colour.")

    def _valid_move_checks(self, tile_type: Type[hive.tiles.Tile], index: Tuple[int, int]):
        if self.first_move and index != (0, 0):
            raise RuntimeError("First move must be at the root")

        if not self.active_player.bee_played and self.active_player.turn >= 2 and tile_type is not hive.tiles.Bee:
            raise RuntimeError("Bee must be played now")

        if self.board[index] is not None:
            raise RuntimeError("Cell is already occupied!")

        # skip the neighbour count check on the very first move only
        if not self.first_move:
            self._disconnect_check(index)

        if self.active_player.turn > 0:
            self._opposing_color_violation_check(index)

    def add_tile(self, tile_type: Type[hive.tiles.Tile], index: Tuple[int, int]):
        logger.debug(f"Playing {tile_type} @ {index}")
        self._valid_move_checks(tile_type, index)

        # try and get a tile of the requested type
        try:
            tile = next(filter(lambda tile: type(tile) is tile_type, self.active_player.unused_tiles))
        except StopIteration:
            raise RuntimeError("No tiles of requested type available.")

        self.board[index] = tile

        # that succeeded, so now drop the tile from the user's rack
        self.active_player.unused_tiles.remove(tile)
        self.active_player.turn += 1
        if tile_type is hive.tiles.Bee:
            self.active_player.bee_played = True

        # and now switch the active and passive player
        self.active_player, self.inactive_player = self.inactive_player, self.active_player

        self.first_move = False
