from typing import Set, Tuple, Type
import pytest

import hive.board
import hive.tiles


def test_grasshopper_large_distance():
    board = hive.board.Board[hive.tiles.Tile]()
    grasshopper = hive.tiles.Grasshopper(hive.tiles.Colour.WHITE)
    grasshopper_index = (2, 2)
    board[grasshopper_index] = grasshopper
    board[(3, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(4, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(5, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = grasshopper.valid_moves(grasshopper_index, board)
    assert valid_moves == {
        (6, 2),
    }


@pytest.mark.parametrize("tile_type, valid_moves_expected", [
    (hive.tiles.Ant, {(1, 3), (2, 3), (3, 2), (3, 1), (2, 1)}),
    (hive.tiles.Bee, {(2, 1), (1, 3)}),
    (hive.tiles.Grasshopper, {(3, 2)}),
    (hive.tiles.Spider, {(3, 2)}),
])
def test_1_neighbour(
    tile_type: Type[hive.tiles.Tile],
    valid_moves_expected: Set[Tuple[int, int]]
):
    board = hive.board.Board[hive.tiles.Tile]()
    tile = tile_type(hive.tiles.Colour.WHITE)
    tile_index = (1, 2)
    board[tile_index] = tile
    board[(2, 2)] = hive.tiles.Ant(hive.tiles.Colour.WHITE)

    valid_moves = tile.valid_moves(tile_index, board)
    assert valid_moves == valid_moves_expected


@pytest.mark.parametrize("tile_type, valid_moves_expected", [
    (hive.tiles.Ant, {
        (2, 3), (3, 2), (4, 1), (4, 0), (3, 0), (2, 0), (1, 1), (0, 2), (0, 3),
        (0, 4), (1, 4)
    }),
    (hive.tiles.Bee, {(3, 2), (2, 3)}),
    (hive.tiles.Grasshopper, {(4, 0), (2, 0), (0, 2), (0, 4)}),
    (hive.tiles.Spider, {(4, 0), (0, 4)}),
])
def test_4_neighbours_a(
    tile_type: Type[hive.tiles.Tile],
    valid_moves_expected: Set[Tuple[int, int]]
):
    board = hive.board.Board[hive.tiles.Tile]()
    tile = tile_type(hive.tiles.Colour.WHITE)
    tile_index = (2, 2)
    board[tile_index] = tile
    board[(3, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(2, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 3)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = tile.valid_moves(tile_index, board)
    assert valid_moves == valid_moves_expected


@pytest.mark.parametrize("tile_type, valid_moves_expected", [
    (hive.tiles.Ant, set()),
    (hive.tiles.Bee, set()),
    (hive.tiles.Grasshopper, {(0, 2), (0, 4), (4, 2), (4, 0)}),
    (hive.tiles.Spider, set()),
])
def test_4_neighbours_b(
    tile_type: Type[hive.tiles.Tile],
    valid_moves_expected: Set[Tuple[int, int]]
):
    board = hive.board.Board[hive.tiles.Tile]()
    tile = tile_type(hive.tiles.Colour.WHITE)
    tile_index = (2, 2)
    board[tile_index] = tile
    board[(3, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(3, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 3)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = tile.valid_moves(tile_index, board)
    assert valid_moves == valid_moves_expected


@pytest.mark.parametrize("tile_type, valid_moves_expected", [
    (hive.tiles.Ant, set()),
    (hive.tiles.Bee, set()),
    (hive.tiles.Grasshopper, {(0, 2), (0, 4), (4, 2), (4, 0), (2, 0)}),
    (hive.tiles.Spider, set()),
])
def test_5_neighbours(
    tile_type: Type[hive.tiles.Tile],
    valid_moves_expected: Set[Tuple[int, int]]
):
    board = hive.board.Board[hive.tiles.Tile]()
    tile = tile_type(hive.tiles.Colour.WHITE)
    tile_index = (2, 2)
    board[tile_index] = tile
    board[(3, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(3, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(2, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 3)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = tile.valid_moves(tile_index, board)
    assert valid_moves == valid_moves_expected


@pytest.mark.parametrize("tile_type, valid_moves_expected", [
    (hive.tiles.Ant, set()),
    (hive.tiles.Bee, set()),
    (hive.tiles.Grasshopper, {(0, 2), (0, 4), (2, 4), (4, 2), (4, 0), (2, 0)}),
    (hive.tiles.Spider, set()),
])
def test_6_neighbours(
    tile_type: Type[hive.tiles.Tile],
    valid_moves_expected: Set[Tuple[int, int]]
):
    board = hive.board.Board[hive.tiles.Tile]()
    tile = tile_type(hive.tiles.Colour.WHITE)
    tile_index = (2, 2)
    board[tile_index] = tile
    board[(3, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(3, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(2, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 3)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(2, 3)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = tile.valid_moves(tile_index, board)
    assert valid_moves == valid_moves_expected
