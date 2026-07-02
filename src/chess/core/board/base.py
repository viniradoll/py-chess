from chess.core.pieces import Piece
from typing import Iterator, Tuple, Set
from chess.core.datatypes import Move, Square, Color
from .view import BoardView
from .position import Position
from abc import ABC, abstractmethod
import chess.core.pieces as pieces


class Board(BoardView, ABC):
    def __init__(self, size: int):
        self.size: int = size

    @abstractmethod
    def initialize(self): ...

    def setup_starting_position(self, position: Position | None = None):
        if position is None:
            position = Position()
        for square, piece in position.pieces:
            self.set_piece_at(square, piece=piece)

    @abstractmethod
    def get_piece_at(self, sq: Square) -> pieces.Piece | None: ...

    @abstractmethod
    def set_piece_at(self, sq: Square, piece: pieces.Piece | None): ...

    def move_piece(self, move: Move):
        piece = self.get_piece_at(move.from_sq)
        if not piece:
            raise ValueError("No piece in this square")
        piece.has_moved = True
        self.set_piece_at(move.to_sq, piece)
        self.set_piece_at(move.from_sq, None)

    def get_moves_at(self, sq: Square) -> list[Move]:
        piece = self.get_piece_at(sq)
        if piece is None:
            return []
        return piece.get_move_list(board=self, from_sq=sq)

    def get_color_at(self, sq: Square) -> Color | None:
        piece = self.get_piece_at(sq)
        return None if piece is None else piece.color

    def get_seen_squares(self, color) -> Set[Square]:
        seen_squares: Set[Square] = set()
        for piece, sq in self:
            if piece.color == color:
                seen_squares.update(piece.get_seen_squares(self, sq))
        return seen_squares

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

    def __iter__(self) -> Iterator[Tuple[Piece, Square]]:
        for i in range(self.size):
            for j in range(self.size):
                piece = self.get_piece_at(Square(i, j))
                if piece is not None:
                    yield piece, Square(i,j)
