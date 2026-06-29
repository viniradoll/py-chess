from __future__ import annotations

class Square:
    def __init__(self, row, col):
        self.row: int = row
        self.col: int = col
    def __repr__(self):
        return str({"row": self.row, "col": self.col})
    def __eq__(self, other:object):
        if not isinstance(other, Square):
            return False
        return (self.row == other.row and self.col == other.col)