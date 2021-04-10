import hive.board


def test_create_board():
    hive.board.Board()


def test_set_and_get():
    board = hive.board.Board()
    board[(3, 2)] = "a"
    board[(1, -2)] = "b"
    board[(0, 0)] = "c"
    board[(-5, -9)] = "d"
    board[(-7, 1)] = "e"

    assert board[(3, 2)] == "a"
    assert board[(1, -2)] == "b"
    assert board[(0, 0)] == "c"
    assert board[(-5, -9)] == "d"
    assert board[(-7, 1)] == "e"


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


def test_connected_components_a():
    board = hive.board.Board()

    assert board.connected_components() == 0


def test_connected_components_b():
    board = hive.board.Board()

    board[(0, 0)] = "a"

    assert board.connected_components() == 1


def test_connected_components_c():
    board = hive.board.Board()

    board[(0, 0)] = "a"
    board[(1, 1)] = "b"

    assert board.connected_components() == 2


def test_connected_components_d():
    board = hive.board.Board()

    board[(0, 0)] = "a"
    board[(1, 1)] = "b"
    board[(1, 0)] = "c"

    assert board.connected_components() == 1


def test_connected_components_e():
    board = hive.board.Board()

    # add a circle of tiles
    board[(0, 0)] = "a"
    board[(0, 1)] = "b"
    board[(1, 1)] = "c"
    board[(2, 0)] = "d"
    board[(2, -1)] = "e"
    board[(1, -1)] = "f"

    assert board.connected_components() == 1
