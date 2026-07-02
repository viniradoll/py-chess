from .base import Piece
from chess.core.datatypes import Square, Move, Color
from chess.core.board import BoardView


class Pawn(Piece):
    can_promote = True
    
    def get_seen_squares(self, board: BoardView, from_sq: Square) -> list[Square]:
        direction = 1 if self.color == Color.WHITE else -1
        seen_squares = []

        new_square = Square(from_sq.row + (1 * direction), from_sq.col + 1)
        if board.is_capturable(new_square, self.color):
            seen_squares.append(new_square)

        new_square = Square(from_sq.row + (1 * direction), from_sq.col - 1)
        if board.is_capturable(new_square, self.color):
            seen_squares.append(new_square)
        return seen_squares

    def get_move_list(self, board: BoardView, from_sq: Square) -> list[Move]:
        move_list: list[Move] = []
        direction = 1 if self.color == Color.WHITE else -1
        new_square = Square(from_sq.row + (1 * direction), from_sq.col)
        if board.is_available(new_square):
            move_list.append(Move(from_sq, to_sq=new_square))

            new_square = Square(from_sq.row + (2 * direction), from_sq.col)
            if not self.has_moved and board.is_available(new_square):
                move_list.append(Move(from_sq, to_sq=new_square))

        new_square = Square(from_sq.row + (1 * direction), from_sq.col + 1)
        if board.is_capturable(new_square, self.color):
            move_list.append(Move(from_sq, to_sq=new_square))

        new_square = Square(from_sq.row + (1 * direction), from_sq.col - 1)
        if board.is_capturable(new_square, self.color):
            move_list.append(Move(from_sq, to_sq=new_square))

        return move_list
