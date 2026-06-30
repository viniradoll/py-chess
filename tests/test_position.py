# import pytest
import chess.core.board as board
import chess.core.datatypes as datatypes
import chess.core.pieces as pieces


def test_starting_position():
    b = board.MatrixBoard()
    b.setup_starting_position()
    b.get_piece_at(datatypes.Square(0, 0)) is pieces.Rook


def test_fen_parsing():
    board.FenParser.parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
