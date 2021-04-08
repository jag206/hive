import pytest

import hive.game
import hive.tiles

def test_create_game():
    game = hive.game.Game()


def test_cant_add_external_tile():
    game = hive.game.Game()

    with pytest.raises(RuntimeError) as e:
        game.add_tile(hive.tiles.Bee(hive.tiles.Colour.WHITE), 0)


def test_can_play_at_root():
    game = hive.game.Game()
    game.add_tile(next(iter(game.active_player.unused_tiles)), game.board)


def test_cannot_both_play_at_root():
    game = hive.game.Game()
    game.add_tile(next(iter(game.active_player.unused_tiles)), game.board)

    with pytest.raises(RuntimeError):
        game.add_tile(next(iter(game.active_player.unused_tiles)), game.board)
