from chess.core.pieces import Piece
from chess.core.datatypes import Square, Move

from chess.core.board import BoardView


class King(Piece):
    def get_move_list(self, board: BoardView, from_sq: Square) -> list[Move]:
        move_list = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                new_square = Square(from_sq.row + i, col=from_sq.col + j)
                if not board.is_available(new_square) and not board.is_capturable(
                    new_square, self.color
                ):
                    continue
                move_list.append(Move(from_sq, to_sq=new_square))
        return move_list
