from chess.core.pieces import SlidingPiece


class Rook(SlidingPiece):
    symbol = "R"
    secundary_castle_piece = True

    def directions(self):
        return [(1, 0), (0, 1), (-1, 0), (0, -1)]
