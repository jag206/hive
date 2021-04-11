import hive.board
import hive.tiles


def test_bee_moves_with_4_specific_neighbours():
    board = hive.board.Board[hive.tiles.Tile]()
    bee = hive.tiles.Bee(hive.tiles.Colour.WHITE)
    bee_index = (0, 0)
    board[bee_index] = bee
    board[(1, -1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(0, -1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(-1, 0)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(-1, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = bee.valid_moves(bee_index, board)
    assert valid_moves == {
        (1, 0),
        (0, 1),
    }


def test_bee_stuck_with_4_specific_neighbours():
    board = hive.board.Board[hive.tiles.Tile]()
    bee = hive.tiles.Bee(hive.tiles.Colour.WHITE)
    bee_index = (0, 0)
    board[bee_index] = bee
    board[(1, 0)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, -1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(-1, 0)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(-1, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = bee.valid_moves(bee_index, board)
    assert len(valid_moves) == 0


def test_bee_stuck_with_5_neighbours():
    board = hive.board.Board[hive.tiles.Tile]()
    bee = hive.tiles.Bee(hive.tiles.Colour.WHITE)
    bee_index = (0, 0)
    board[bee_index] = bee
    board[(1, 0)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, -1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(0, -1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(-1, 0)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(-1, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = bee.valid_moves(bee_index, board)
    assert len(valid_moves) == 0


def test_bee_stuck_with_6_neighbours():
    board = hive.board.Board[hive.tiles.Tile]()
    bee = hive.tiles.Bee(hive.tiles.Colour.WHITE)
    bee_index = (0, 0)
    board[bee_index] = bee
    board[(1, 0)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(1, -1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(0, -1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(-1, 0)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(-1, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)
    board[(0, 1)] = hive.tiles.Spider(hive.tiles.Colour.WHITE)

    valid_moves = bee.valid_moves(bee_index, board)
    assert len(valid_moves) == 0
