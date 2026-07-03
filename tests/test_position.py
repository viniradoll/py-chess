# import pytest
import chess.core.board as board
import chess.core.datatypes as datatypes
import chess.core.pieces as pieces
from chess.io.fen import FenParser


def test_starting_position():
    b = board.MatrixBoard()
    b.setup_starting_position()
    assert isinstance(b.get_piece_at(datatypes.Square(0, 0)), pieces.Rook) 


def test_fen_parsing():
    FenParser.parse_fen(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    )
