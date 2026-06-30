from chess.core.board import Board, MatrixBoard
from chess.core.datatypes import Color


class Game:
    def __init__(self):
        self.board: Board = MatrixBoard()
        self.board.setup_starting_position()
        self.turn: Color = Color.WHITE

    def make_move(self): ...
