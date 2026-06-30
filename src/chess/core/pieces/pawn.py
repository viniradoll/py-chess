from .base import Piece
import chess.core.datatypes as datatypes
import chess.core.board as board


class Pawn(Piece):
    can_promote = True

    def get_move_list(
        self, board: board.BoardView, from_sq: datatypes.Square
    ) -> list[datatypes.Move]:
        move_list: list[datatypes.Move] = []
        direction = 1 if self.color == datatypes.Color.WHITE else -1
        new_square = datatypes.Square(from_sq.row + (1 * direction), from_sq.col)
        if board.is_available(new_square):
            move_list.append(datatypes.Move(from_sq, to_sq=new_square))

            new_square = datatypes.Square(from_sq.row + (2 * direction), from_sq.col)
            if not self.has_moved and board.is_available(new_square):
                move_list.append(datatypes.Move(from_sq, to_sq=new_square))

        new_square = datatypes.Square(from_sq.row + (1 * direction), from_sq.col + 1)
        if board.is_capturable(new_square, self.color):
            move_list.append(datatypes.Move(from_sq, to_sq=new_square))

        new_square = datatypes.Square(from_sq.row + (1 * direction), from_sq.col - 1)
        if board.is_capturable(new_square, self.color):
            move_list.append(datatypes.Move(from_sq, to_sq=new_square))

        return move_list
