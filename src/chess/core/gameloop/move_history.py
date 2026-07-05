from chess.core.pieces import Piece
from chess.core.datatypes import Move
from dataclasses import dataclass

@dataclass(frozen=True)
class MoveRecord:
    move: Move
    captured_piece: Piece | None
    had_moved: bool

class MoveHistory:
    def __init__(self):
        self._records: list[MoveRecord] = []

    def push(self, record: MoveRecord) -> None:
        self._records.append(record)

    def pop(self) -> MoveRecord | None:
        return self._records.pop() if self._records else None