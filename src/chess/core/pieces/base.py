from abc import ABC, abstractmethod
import chess.core.datatypes as datatypes
import chess.core.board as board


class Piece(ABC):
    # Piece has already moved in this game
    has_moved: bool = False
    # If piece can promote on the last rank (e.g. Pawn)
    can_promote: bool = False
    # If piece can Castle (e.g. King)
    primary_castle_piece: bool = False
    # If piece can help a piece Castle (e.g. Rook)
    secundary_castle_piece: bool = False

    def __init__(self, color: datatypes.Color):
        self.color = color

    @abstractmethod
    def get_move_list(
        self, board: board.BoardView, from_sq: datatypes.Square
    ) -> list[datatypes.Move]: ...

    def __eq__(self, other: object):
        if not isinstance(other, Piece):
            return False
        return self.__class__ == other.__class__ and self.color == other.color


class SlidingPiece(Piece):
    def __init__(self, color: datatypes.Color):
        super().__init__(color)

    @abstractmethod
    def directions(self) -> list[tuple[int, int]]: ...

    def get_move_list(
        self, board: board.BoardView, from_sq: datatypes.Square
    ) -> list[datatypes.Move]:
        move_list = []
        for direction in self.directions():
            distance = 1
            row, col = direction
            new_square = datatypes.Square(
                from_sq.row + (distance * row), from_sq.col + (distance * col)
            )
            while board.is_available(new_square):
                move_list.append(datatypes.Move(from_sq, to_sq=new_square))
                distance += 1
                new_square = datatypes.Square(
                    from_sq.row + (distance * row), from_sq.col + (distance * col)
                )
            if board.is_capturable(new_square, self.color):
                move_list.append(datatypes.Move(from_sq, to_sq=new_square))

            distance = 1

        return move_list
