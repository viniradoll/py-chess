from __future__ import annotations



class Position:
    __defaultFenPosition: str = (
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    )

    def __init__(self, fen: str = __defaultFenPosition):
        self.fen = fen
        self.pieces = []
        self.setup()

    def setup(self):
        from chess.io.fen import FenParser

        self.pieces = FenParser.parse_fen(self.fen)
