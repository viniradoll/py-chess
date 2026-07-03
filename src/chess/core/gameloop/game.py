from chess.core.datatypes import Color, Move, Square
from chess.core.board import Board, MatrixBoard


class Game:
    def __init__(self, board: Board | None = None):
        self.board: Board = board if board is not None else MatrixBoard()
        self.board.setup_starting_position()
        self.turn: Color = Color.WHITE

    def make_move(self, from_sq: str, to_sq: str):
        move = Move(Square.from_algebraic(from_sq), Square.from_algebraic(to_sq))

        if not self.validate_move(move):
            return False
        
        self.board.move_piece(move)

        self.turn = ~self.turn

    def validate_move(self, move: Move) -> bool:
        if move not in self.get_all_moves(self.turn):
            raise ValueError("Invalid move")
            return False
        return True

    def get_all_moves(self, color: Color) -> set[Move]:
        moves = set()
        for piece, square in self.board:
            if piece.color != color: continue
            moves.update(self.board.get_moves_at(square))
        return moves

    def is_in_check(self, color: Color) -> bool:
        king_position = self.board.get_king_position(color)
        if king_position is None:
            raise ValueError("No king?")
        return king_position in self.board.get_seen_squares(~color)