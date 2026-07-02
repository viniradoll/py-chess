from chess.core.datatypes import Color, Move, Square
from chess.core.board import Board, MatrixBoard


class Game:
    def __init__(self, board: Board | None = None):
        self.board: Board = board if board is not None else MatrixBoard()
        self.board.setup_starting_position()
        self.turn: Color = Color.WHITE

    def make_move(self, color: Color, from_sq: str, to_sq: str):
        move = Move(Square.from_algebraic(from_sq), Square.from_algebraic(to_sq))

        self._validate_move(move,color)
        
        self.board.move_piece(move)

        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK

    def _validate_move(self, move: Move, color: Color) -> bool:
        if color != self.turn:
            raise ValueError("Incorrect turn")
        if not self.board.get_piece_at(move.from_sq):
            raise ValueError(f"No piece at {move.from_sq.to_algebraic()}")
        if self.board.get_color_at(move.from_sq) != color:
            raise ValueError(f"This is not a {color} piece")
        
        if move not in self.board.get_moves_at(move.from_sq):
            raise ValueError(f"Invalid move {move}")

        return True

    def get_all_moves(self, color: Color) -> list[Move]:
        moves: list[Move] = []
        for piece, square in self.board:
            if piece.color != color: continue
            moves += piece.get_move_list(self.board, square)
        return moves