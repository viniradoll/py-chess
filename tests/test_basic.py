from chess.core.board import MatrixBoard
from chess.core.datatypes import Color, Square
from chess.core.pieces import Pawn
import pytest


def test_opposite_colors():
    assert Color.WHITE is not Color.BLACK
    assert Color.WHITE == ~Color.BLACK


def test_initiate_board():
    b = MatrixBoard()
    assert b.grid == [[None] * 8] * 8


def test_instanciate_square():
    board = instanciate_board()
    with pytest.raises(ValueError):
        board.set_piece_at(Square(12, 5), Pawn(Color.BLACK))
    with pytest.raises(ValueError):
        board.set_piece_at(Square(-1, 5), Pawn(Color.BLACK))


def instanciate_board() -> MatrixBoard:
    b = MatrixBoard()
    for i in range(8):
        b.set_piece_at(Square(1, i), Pawn(Color.WHITE))
    return b


def test_square_from_algebraic_notation():
    sq = Square.from_algebraic("e4")
    assert sq.row == 3 and sq.col == 4


def test_square_to_algebraic_notation():
    sq = Square(3, 4)
    assert sq.to_algebraic() == "e4"


def test_squares_equal():
    sq1 = Square.from_algebraic("e4")
    sq2 = Square(3, 4)
    assert sq1 == sq2
