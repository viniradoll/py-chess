from enum import Enum


class Color(Enum):
    WHITE = "white"
    BLACK = "black"

    def __invert__(self):
        return Color.WHITE if self is Color.BLACK else Color.BLACK
