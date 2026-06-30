from chess.core.datatypes.move import Move
from chess.core.datatypes.square import Square
from .view import BoardView
from .position import Position
from abc import ABC, abstractmethod
import chess.core.datatypes as datatypes
import chess.core.pieces as pieces


class Board(BoardView, ABC):
    def __init__(self, size: int):
        self.size: int = size

    @abstractmethod
    def initialize(self): ...

    def setup_starting_position(self, position: Position = Position()):
        for square, piece in position.pieces:
            self.set_piece_at(square, piece=piece)

    @abstractmethod
    def get_piece_at(self, sq: datatypes.Square) -> pieces.Piece | None: ...

    @abstractmethod
    def set_piece_at(self, sq: datatypes.Square, piece: pieces.Piece | None): ...

    def move_piece(self, move: Move):
        piece = self.get_piece_at(move.from_sq)
        if not piece:
            raise ValueError("No piece in this square")
        self.set_piece_at(move.to_sq, piece)
        self.set_piece_at(move.from_sq, None)

    def get_moves_at(self, sq: datatypes.Square) -> list[datatypes.Move]:
        piece = self.get_piece_at(sq)
        if piece is None:
            return []
        return piece.get_move_list(board=self, from_sq=sq)

    def get_color_at(self, sq: datatypes.Square) -> datatypes.Color | None:
        piece = self.get_piece_at(sq)
        return None if piece is None else piece.color

    def is_empty(self, sq: datatypes.Square) -> bool:
        if not self.is_inbound(sq):
            raise ValueError(f"Square is not inbound row: '{sq.row}' col: '{sq.col}'")
        return True if self.get_piece_at(sq) is None else False

    def is_enemy(self, sq: datatypes.Square, color: datatypes.Color) -> bool:
        if not self.is_inbound(sq):
            raise ValueError(f"Square is not inbound row: '{sq.row}' col: '{sq.col}'")
        piece = self.get_piece_at(sq)
        return piece is not None and piece.color != color

    def __repr__(self):
        rows: list[str] = []
        for i in range(self.size - 1, -1, -1):
            row: list[str] = []
            for j in range(self.size):
                piece = self.get_piece_at(Square(i, j))

                if piece is None:
                    row.append(".")
                else:
                    symbol = piece.__class__.__name__[0]

                    if piece.color.name == "WHITE":
                        row.append(symbol.upper())
                    else:
                        row.append(symbol.lower())

            rows.append(" ".join(row))

        return "\n".join(rows)
