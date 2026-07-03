from chess.core.pieces import Piece
from chess.core.datatypes import Square, Move
from chess.core.board import BoardView


class King(Piece):
    primary_castle_piece = True

    def get_seen_squares(self, board: BoardView, from_sq: Square) -> list[Square]:
        seen_squares = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                new_square = Square(from_sq.row + i, col=from_sq.col + j)
                if board.is_inbound(new_square):
                    seen_squares.append(new_square)
        return seen_squares
