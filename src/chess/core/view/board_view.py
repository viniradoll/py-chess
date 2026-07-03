from abc import ABC,abstractmethod
import chess.core.datatypes as datatypes


class BoardView(ABC):
    def __init__(self, size: int = 8):
        self.size = size

    @abstractmethod
    def get_color_at(self, sq: datatypes.Square) -> datatypes.Color | None: ...

    def is_inbound(self, sq: datatypes.Square) -> bool:
        return 0 <= sq.row < self.size and 0 <= sq.col < self.size

    def is_empty(self, sq: datatypes.Square) -> bool:
        if not self.is_inbound(sq):
            raise ValueError(f"Square is not inbound row: '{sq.row}' col: '{sq.col}'")
        return self.get_color_at(sq) is None

    def is_enemy(self, sq: datatypes.Square, color: datatypes.Color) -> bool:
        if not self.is_inbound(sq):
            raise ValueError(f"Square is not inbound row: '{sq.row}' col: '{sq.col}'")
        square_color = self.get_color_at(sq)
        return square_color is not None and square_color != color

    def is_available(self, sq: datatypes.Square) -> bool:
        return self.is_inbound(sq) and self.is_empty(sq)

    def is_capturable(self, sq: datatypes.Square, color: datatypes.Color) -> bool:
        return self.is_inbound(sq) and self.is_enemy(sq, color)
