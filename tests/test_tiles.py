from typing import Type
import pytest

import hive.board
import hive.tiles


def test_spider_moves_with_4_specific_neighbours():
    board = hive.board.Board[hive.tiles.Tile]()
    spider = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    spider_index = (2, 2)
    board[spider_index] = spider
    board[(3, 1)] = hive.tiles.Ant(hive.tiles.Colour.WHITE)
    board[(2, 1)] = hive.tiles.Ant(hive.tiles.Colour.WHITE)
    board[(1, 2)] = hive.tiles.Ant(hive.tiles.Colour.WHITE)
    board[(1, 3)] = hive.tiles.Ant(hive.tiles.Colour.WHITE)

    valid_moves = spider.valid_moves(spider_index, board)
    assert valid_moves == {
        (4, 0),
        (0, 4),
    }



def test_bee_moves_with_4_specific_neighbours():
    board = hive.board.Board[hive.tiles.Tile]()
    bee = hive.tiles.Bee(hive.tiles.Colour.WHITE)
    bee_index = (2, 2)
    board[bee_index] = bee
    board[(3, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(2, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 3)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = bee.valid_moves(bee_index, board)
    assert valid_moves == {
        (3, 2),
        (2, 3),
    }


@pytest.mark.parametrize("tile_type", [
    hive.tiles.Bee,
    hive.tiles.Spider,
])
def test_stuck_with_4_specific_neighbours(tile_type: Type[hive.tiles.Tile]):
    board = hive.board.Board[hive.tiles.Tile]()
    tile = tile_type(hive.tiles.Colour.WHITE)
    tile_index = (2, 2)
    board[tile_index] = tile
    board[(3, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(3, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 3)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = tile.valid_moves(tile_index, board)
    assert len(valid_moves) == 0


@pytest.mark.parametrize("tile_type", [
    hive.tiles.Bee,
    hive.tiles.Spider,
])
def test_stuck_with_5_neighbours(tile_type: Type[hive.tiles.Tile]):
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
    assert len(valid_moves) == 0


@pytest.mark.parametrize("tile_type", [
    hive.tiles.Bee,
    hive.tiles.Spider,
])
def test_stuck_with_6_neighbours(tile_type: Type[hive.tiles.Tile]):
    board = hive.board.Board[hive.tiles.Tile]()
    tile = tile_type(hive.tiles.Colour.WHITE)
    tile_index = (2, 2)
    board[tile_index] = tile
    board[(3, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(3, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(2, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 2)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, 3)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(2, 3)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = tile.valid_moves(tile_index, board)
    assert len(valid_moves) == 0
