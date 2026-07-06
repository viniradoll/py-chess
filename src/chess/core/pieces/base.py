from __future__ import annotations
from abc import ABC, abstractmethod
from chess.core.datatypes import Square, Move, Color
from chess.core.view.board_view import BoardView


class Piece(ABC):
    # If piece can promote on the last rank (e.g. Pawn)
    can_promote: bool = False
    # If piece can Castle (e.g. King)
    primary_castle_piece: bool = False
    # If piece can help a piece Castle (e.g. Rook)
    secondary_castle_piece: bool = False
    # Algebric Notation symnol
    symbol: str

    def __init__(self, color: Color):
        self.color = color

        # Piece has already moved in this game
        self.has_moved: bool = False

    @abstractmethod
    def get_seen_squares(self, board: BoardView, from_sq: Square) -> list[Square]:
        ...

    def get_move_list(self, board: BoardView, from_sq: Square) -> list[Move]: 
        moves: list[Move] = []
        for square in self.get_seen_squares(board,from_sq):
            if not board.is_available(square) and not board.is_capturable(square, self.color):
                    continue
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
            if board.is_inbound(new_square):
                seen_squares.append(new_square)

            distance = 1

        return seen_squares
