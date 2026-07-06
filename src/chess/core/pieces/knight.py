from chess.core.pieces import Piece
from chess.core.datatypes import Square
from chess.core.view.board_view import BoardView


class Knight(Piece):
    symbol = "N"
    def get_seen_squares(self, board: BoardView, from_sq: Square) -> list[Square]:
        seen_squares: list[Square] = []
        for i in [(-2, (-1, 1)), (-1, (-2, 2)), (1, (-2, 2)), (2, (-1, 1))]:
            for j in i[1]:
                new_square = Square(from_sq.row + i[0], from_sq.col + j)
                if board.is_inbound(new_square):
                    seen_squares.append(new_square)

        return seen_squares
