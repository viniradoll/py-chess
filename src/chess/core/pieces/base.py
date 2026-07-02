from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from chess.core.datatypes import Square, Move, Color
if TYPE_CHECKING:
    from chess.core.board import BoardView


class Piece(ABC):
    # Piece has already moved in this game
    has_moved: bool = False
    # If piece can promote on the last rank (e.g. Pawn)
    can_promote: bool = False
    # If piece can Castle (e.g. King)
    primary_castle_piece: bool = False
    # If piece can help a piece Castle (e.g. Rook)
    secundary_castle_piece: bool = False

    def __init__(self, color: Color):
        self.color = color

    @abstractmethod
    def get_seen_squares(self, board: BoardView, from_sq: Square) -> list[Square]:
        ...

    def get_move_list(self, board: BoardView, from_sq: Square) -> list[Move]: 
        moves: list[Move] = []
        for square in self.get_seen_squares(board,from_sq):
            moves.append(Move(from_sq, square))
        return moves

    def __eq__(self, other: object):
        if not isinstance(other, Piece):
            return False
        return self.__class__ == other.__class__ and self.color == other.color


class SlidingPiece(Piece):
    def __init__(self, color: Color):
        super().__init__(color)

    @abstractmethod
    def directions(self) -> list[tuple[int, int]]: ...

    def get_seen_squares(self, board: BoardView, from_sq: Square) -> list[Square]:
        seen_squares = []
        for direction in self.directions():
            distance = 1
            row, col = direction
            new_square = Square(
                from_sq.row + (distance * row), from_sq.col + (distance * col)
            )
            while board.is_available(new_square):
                seen_squares.append(new_square)
                distance += 1
                new_square = Square(
                    from_sq.row + (distance * row), from_sq.col + (distance * col)
                )
            if board.is_capturable(new_square, self.color):
                seen_squares.append(new_square)

            distance = 1

        return seen_squares
