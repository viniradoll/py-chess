from chess.core.pieces import Piece
from chess.core.board import BoardView
from chess.core.datatypes import Square, Move


class Knight(Piece):
    def get_move_list(self, board: BoardView, from_sq: Square) -> list[Move]:
        move_list: list[Move] = []
        for i in [(-2, (-1, 1)), (-1, (-2, 2)), (1, (-2, 2)), (2, (-1, 1))]:
            for j in i[1]:
                new_square = Square(from_sq.row + i[0], from_sq.col + j)
                if not board.is_available(new_square) and not board.is_capturable(
                    new_square, self.color
                ):
                    continue
                move_list.append(Move(from_sq, new_square))

        return move_list
