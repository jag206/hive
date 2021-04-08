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
    game.add_tile(next(iter(game.active_player.unused_tiles)), game.root)


def test_cannot_both_play_at_root():
    game = hive.game.Game()
    game.add_tile(next(iter(game.active_player.unused_tiles)), game.root)

    with pytest.raises(RuntimeError):
        game.add_tile(next(iter(game.active_player.unused_tiles)), game.root)

@pytest.mark.skip("Not implemented")
def test_must_play_bee_on_or_before_turn_three():
    game = hive.game.Game()
    # TODO(james.gunn): Implement me

# TODO(james.gunn): Be careful here to test some edge cases where playing the
# tile would violate a connection that hasn't been explicitly constructed
# eg. if the hive bends around to reconnect with itself further around
@pytest.mark.skip("Not implemented")
def test_cannot_add_tile_where_it_touches_opposite_color():
    game = hive.game.Game()
    # TODO(james.gunn): Implement me
