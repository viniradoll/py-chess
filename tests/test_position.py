#import pytest
import chess.core.board as board
import chess.core.datatypes as datatypes
import chess.core.pieces as pieces

def test_starting_position():
    Board = board.MatrixBoard()
    Board.setupStartingPosition()
    Board.getPieceAt(datatypes.Square(0,0)) is pieces.Rook

def test_fen_parsing():
    board.FenParser.parseFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")