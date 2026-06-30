from __future__ import annotations


class Square:
    def __init__(self, row, col):
        self.row: int = row
        self.col: int = col

    @classmethod
    def from_algebraic(cls, algebraic: str) -> Square:
        if len(algebraic) != 2:
            raise ValueError(f"Invalid algebraic notation: '{algebraic}'")

        col_char, row_char = algebraic[0].lower(), algebraic[1]

        if col_char not in "abcdefgh" or row_char not in "12345678":
            raise ValueError(f"Invalid algebraic notation: '{algebraic}'")

        col = ord(col_char) - ord("a")  # a=0, b=1, ..., h=7
        row = int(row_char) - 1  # 1=0, 2=1, ..., 8=7

        return cls(row, col)

    def to_algebraic(self) -> str:
        col_char = chr(ord("a") + self.col)
        row_char = str(self.row + 1)
        return f"{col_char}{row_char}"

    def __repr__(self):
        return str({"row": self.row, "col": self.col})

    def __eq__(self, other: object):
        if not isinstance(other, Square):
            return False
        return self.row == other.row and self.col == other.col
