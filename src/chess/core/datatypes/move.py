from chess.core.datatypes.square import Square

class Move:
    from_sq: Square
    to_sq: Square
    def __init__(self, from_sq:Square, to_sq:Square):
        self.from_sq = from_sq  
        self.to_sq = to_sq

    def __repr__(self):
        return str({"from_sq": self.from_sq, "to_sq": self.to_sq})