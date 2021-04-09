import pytest
import hive.board


def test_create_board():
    hive.board.Board()


def test_set_and_get_friendly():
    board = hive.board.Board()
    board[(0, 0)] = "a"
    board[(0, 1)] = "b"
    board[(-1, 0)] = "c"

    assert board[(0, 0)] == "a"
    assert board[(0, 1)] == "b"
    assert board[(-1, 0)] == "c"


@pytest.mark.skip("Skipped whilst board resizes from root")
def test_set_and_get():
    board = hive.board.Board()
    board[(3, 2)] = "a"
    board[(1, -2)] = "b"
    board[(0, 0)] = "c"

    assert board[(3, 2)] == "a"
    assert board[(1, -2)] == "b"
    assert board[(0, 0)] == "c"


@pytest.mark.skip("Skipped whilst board resizes from root")
def test_neighbours():
    board = hive.board.Board()
    board[(3, 3)] = "a"
    board[(3, 4)] = "b"
    board[(4, 3)] = "c"
    board[(4, 2)] = "d"
    board[(2, 3)] = "e"
    board[(4, 4)] = "f"

    assert board.neighbours((3, 3)) == {"b", "c", "d", "e"}
    assert board.neighbours((4, 3)) == {"a", "b", "d", "f"}
    assert board.neighbours((1, 3)) == {"e"}
    assert board.neighbours((1, 5)) == set()
