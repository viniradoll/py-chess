from chess.core.datatypes import Color, Move, Square
from chess.core.board import Board, MatrixBoard


class Game:
    def __init__(self, b):
        self.board: Board = b
        self.board.setup_starting_position()
        self.turn: Color = Color.WHITE

    def make_move(self, from_sq: str, to_sq: str):
        m = Move(Square.from_algebraic(from_sq), Square.from_algebraic(to_sq))
        self.board.move_piece(m)
