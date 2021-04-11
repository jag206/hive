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


def test_can_play_at_root():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Bee, (0, 0))


def test_first_play_must_be_root():
    game = hive.game.Game()

    with pytest.raises(RuntimeError):
        game.add_tile(hive.tiles.Bee, (0, 1))


def test_can_both_play():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Bee, (0, 0))
    game.add_tile(hive.tiles.Bee, (0, 1))


def test_cannot_play_if_no_tile_of_type():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Bee, (0, 0))
    game.add_tile(hive.tiles.Bee, (0, 1))

    with pytest.raises(RuntimeError):
        game.add_tile(hive.tiles.Bee, (0, -1))


def test_cannot_both_play_at_root():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Bee, (0, 0))

    with pytest.raises(RuntimeError):
        game.add_tile(hive.tiles.Bee, (0, 0))


def test_must_play_bee_on_or_before_turn_three_a():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Spider, (0, 0))
    game.add_tile(hive.tiles.Spider, (0, 1))
    game.add_tile(hive.tiles.Spider, (0, -1))
    game.add_tile(hive.tiles.Spider, (0, 2))

    # try to play the third spider when the Bee should have been played
    with pytest.raises(RuntimeError):
        game.add_tile(hive.tiles.Spider, (0, -2))


def test_must_play_bee_on_or_before_turn_three_b():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Bee, (0, 0))
    game.add_tile(hive.tiles.Spider, (0, 1))
    game.add_tile(hive.tiles.Spider, (0, -1))
    game.add_tile(hive.tiles.Spider, (0, 2))

    # the bee was played earlier, so player 1 can now play another spider...
    game.add_tile(hive.tiles.Spider, (0, -2))

    # ...but player 2 cannot
    with pytest.raises(RuntimeError):
        game.add_tile(hive.tiles.Spider, (0, 3))


def test_must_play_bee_on_or_before_turn_three_c():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Spider, (0, 0))
    game.add_tile(hive.tiles.Spider, (0, 1))
    game.add_tile(hive.tiles.Spider, (0, -1))
    game.add_tile(hive.tiles.Bee, (0, 2))

    # verify that player 1 can get away with playing the Bee on turn 3...
    game.add_tile(hive.tiles.Bee, (0, -2))

    # and player 2 already played it (turn 2) so she's ok too
    game.add_tile(hive.tiles.Spider, (0, 3))


def test_cannot_add_tile_disconnected():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Spider, (0, 0))

    with pytest.raises(RuntimeError):
        game.add_tile(hive.tiles.Spider, (0, 2))


def test_cannot_add_tile_where_it_touches_opposite_color():
    game = hive.game.Game()

    # both players should be able to play their first tile...
    game.add_tile(hive.tiles.Bee, (0, 0))
    game.add_tile(hive.tiles.Bee, (1, 0))

    # ...but the first player should not be able to connect their second piece
    # to the first player's first piece

    with pytest.raises(RuntimeError):
        game.add_tile(hive.tiles.Spider, (2, 0))


@pytest.mark.skip("Requires beetle movement implementation")
def test_elevated_beetle_can_win():
    pass


@pytest.mark.skip("Requires beetle movement implementation")
def test_elevated_beetle_allows_new_tile():
    pass


def test_cannot_move_opponents_tile():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Bee, (0, 0))

    with pytest.raises(RuntimeError):
        game.move_tile((0, 0), (0, 1))


def test_cannot_request_move_to_occupied_tile():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Bee, (0, 0))
    game.add_tile(hive.tiles.Bee, (0, 1))

    with pytest.raises(RuntimeError):
        game.move_tile((0, 0), (0, 1))


@pytest.mark.skip("Requires beetle movement implementation")
def test_can_move_beetle_onto_occupied_tile():
    pass


def test_cannot_request_move_from_occupied_tile():
    game = hive.game.Game()

    with pytest.raises(RuntimeError):
        game.move_tile((0, 0), (0, 1))


# in this test we deliberately setup the situation so the hive is only disconnected whilst the piece is in transit,
# thus testing the harder case that also encompasses the easier case, those situations where the hive would remain
# disconnected after the piece is replaced
def test_move_must_not_disconnect_hive():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Spider, (0, 0))
    game.add_tile(hive.tiles.Bee, (1, 0))

    game.add_tile(hive.tiles.Bee, (0, -1))
    game.add_tile(hive.tiles.Spider, (2, 0))

    # this should be a valid move for the spider, but it disconnects the hive!
    with pytest.raises(hive.game.DisconnectedHiveError):
        game.move_tile((0, 0), (1, -1))


@pytest.mark.skip("Requires beetle movement implementation")
def test_cannot_move_tile_from_under_beetle():
    pass


def test_can_move_bee_to_valid_location_smoke():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Bee, (0, 0))
    game.add_tile(hive.tiles.Bee, (1, 0))
    original_bee = game.board[(0, 0)]

    game.move_tile((0, 0), (0, 1))

    assert game.board[(0, 0)] is None
    assert game.board[(0, 1)] == original_bee


def test_cannot_move_bee_to_invalid_location_smoke():
    game = hive.game.Game()
    game.add_tile(hive.tiles.Bee, (0, 0))
    game.add_tile(hive.tiles.Bee, (1, 0))

    with pytest.raises(RuntimeError):
        game.move_tile((0, 0), (1, 1))
