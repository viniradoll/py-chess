from chess.core.pieces import SlidingPiece


class Bishop(SlidingPiece):
    symbol = "B"
    def directions(self):
        return [(1, 1), (-1, -1), (-1, 1), (1, -1)]
