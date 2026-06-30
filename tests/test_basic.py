import chess.core.board as board
import chess.core.datatypes as datatypes
import chess.core.pieces as pieces
import pytest


def test_opposite_colors():
    assert datatypes.Color.WHITE is not datatypes.Color.BLACK


def test_initiate_board():
    b = board.MatrixBoard()
    assert b.grid == [[None] * 8] * 8


def test_instanciate_square():
    board = instanciate_board()
    with pytest.raises(ValueError):
        board.set_piece_at(datatypes.Square(12, 5), pieces.Pawn(datatypes.Color.BLACK))
    with pytest.raises(ValueError):
        board.set_piece_at(datatypes.Square(-1, 5), pieces.Pawn(datatypes.Color.BLACK))


def instanciate_board() -> board.MatrixBoard:
    b = board.MatrixBoard()
    for i in range(8):
        b.set_piece_at(datatypes.Square(1, i), pieces.Pawn(datatypes.Color.WHITE))
    return b


def test_square_from_algebraic_notation():
    sq = datatypes.Square.from_algebraic("e4")
    assert sq.row == 3 and sq.col == 4


def test_square_to_algebraic_notation():
    sq = datatypes.Square(3, 4)
    assert sq.to_algebraic() == "e4"


def test_squares_equal():
    sq1 = datatypes.Square.from_algebraic("e4")
    sq2 = datatypes.Square(3, 4)
    assert sq1 == sq2
