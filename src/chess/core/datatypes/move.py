from socket import fromfd
from chess.core.datatypes.square import Square


class Move:
    from_sq: Square
    to_sq: Square

    def __init__(self, from_sq: Square, to_sq: Square):
        self.from_sq = from_sq
        self.to_sq = to_sq

    def __repr__(self):
        return str({"from_sq": self.from_sq, "to_sq": self.to_sq})
    
    def __eq__(self, other: object):
        if not isinstance(other, Move):
            return False
        return self.from_sq == other.from_sq and self.to_sq == other.to_sq
