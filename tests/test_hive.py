from typing import Type

import pytest

import hive.game
import hive.tiles


def get_tile(player: hive.game.Player, tile_type: Type[hive.tiles.Tile]):
    for unused_tile in player.unused_tiles:
        if type(unused_tile) is tile_type:
            return unused_tile

    pytest.fail("Player has no tile of that type to play")


def test_create_game():
    hive.game.Game()


def test_cant_add_external_tile():
    game = hive.game.Game()

    with pytest.raises(RuntimeError):
        game.add_tile(hive.tiles.Bee(hive.tiles.Colour.WHITE), (0, 0))


def test_can_play_at_root():
    game = hive.game.Game()
    game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, 0))


def test_first_play_must_be_root():
    game = hive.game.Game()

    with pytest.raises(RuntimeError):
        game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, 1))


def test_can_both_play():
    game = hive.game.Game()
    game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, 0))
    game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, 1))


@pytest.mark.skip("Refactor after API change")
def test_cannot_play_if_no_tile_of_type():
    # this test assumes that each player only has one bee
    game = hive.game.Game()
    game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, 0))
    game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, 1))

    with pytest.raises(RuntimeError):
        game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, -1))


def test_cannot_both_play_at_root():
    game = hive.game.Game()
    game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, 0))

    with pytest.raises(RuntimeError):
        game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, 0))


def test_must_play_bee_on_or_before_turn_three_a():
    game = hive.game.Game()
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 0))
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 1))
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, -1))
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 2))

    # try to play the third spider when the Bee should have been played
    with pytest.raises(RuntimeError):
        game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, -2))


def test_must_play_bee_on_or_before_turn_three_b():
    game = hive.game.Game()
    game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, 0))
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 1))
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, -1))
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 2))

    # the bee was played earlier, so player 1 can now play another spider...
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, -2))

    # ...but player 2 cannot
    with pytest.raises(RuntimeError):
        game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 3))


def test_must_play_bee_on_or_before_turn_three_c():
    game = hive.game.Game()
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 0))
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 1))
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, -1))
    game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, 2))

    # verify that player 1 can get away with playing the Bee on turn 3...
    game.add_tile(get_tile(game.active_player, hive.tiles.Bee), (0, -2))

    # and player 2 already played it (turn 2) so she's ok too
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 3))


@pytest.mark.skip
def test_cannot_add_tile_disconnected():
    game = hive.game.Game()
    game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 0))

    with pytest.raises(RuntimeError):
        game.add_tile(get_tile(game.active_player, hive.tiles.Spider), (0, 2))


# TODO(james.gunn): Be careful here to test some edge cases where playing the
# tile would violate a connection that hasn't been explicitly constructed
# eg. if the hive bends around to reconnect with itself further around
@pytest.mark.skip("Not implemented")
def test_cannot_add_tile_where_it_touches_opposite_color():
    # TODO(james.gunn): Implement me
    pass
