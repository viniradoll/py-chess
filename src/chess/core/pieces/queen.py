from chess.core.pieces import SlidingPiece


class Queen(SlidingPiece):
    def directions(self):
        return [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
