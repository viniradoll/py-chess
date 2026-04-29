from abc import ABC, abstractmethod
import chess.core.datatypes as datatypes
import chess.core.board as board

class Piece(ABC):
    # Piece has already moved in this game
    hasMoved: bool = False
    # If piece can promote on the last rank (e.g. Pawn)
    canPromote: bool = False
    # If piece can Castle (e.g. King)
    primaryCastlePiece: bool = False
    # If piece can help a piece Castle (e.g. Rook)
    secundaryCastlePiece: bool = False

    def __init__(self, color: datatypes.Color):
        self.color = color

    @abstractmethod
    def getMoveList(self, board: board.BoardView, from_sq: datatypes.Square) -> list[datatypes.Move]:
        return []

    def __eq__(self, other: object):
        if not isinstance(other, Piece):
            return False
        return self.__class__ == other.__class__ and self.color == other.color

class SlidingPiece(Piece):
    def __init__(self, color: datatypes.Color):
        super().__init__(color)

    @abstractmethod
    def directions(self) -> list[tuple[int,int]]:
        return []

    def getMoveList(self, board: board.BoardView, from_sq: datatypes.Square) -> list[datatypes.Move]:
        moveList = []
        for direction in self.directions():
            distance = 1
            row, col = direction
            newSquare = datatypes.Square(from_sq.row+(distance*row), from_sq.col+(distance*col))
            while board.isAvailable(newSquare):
                moveList.append(datatypes.Move(from_sq,to_sq=newSquare))
                distance += 1
                newSquare = datatypes.Square(from_sq.row+(distance*row), from_sq.col+(distance*col))
            if board.isCapturable(newSquare, self.color):
                moveList.append(datatypes.Move(from_sq,to_sq=newSquare))
            
            distance = 1
        
        return moveList
            