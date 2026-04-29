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
    def initialize(self):
        pass

    def setupStartingPosition(self, position: Position = Position()):
        for square, piece in position.pieces:
            self.setPieceAt(square, piece=piece)

    @abstractmethod
    def getPieceAt(self,sq:datatypes.Square) -> pieces.Piece | None:
        return None

    @abstractmethod
    def setPieceAt(self,sq:datatypes.Square, piece: pieces.Piece):
        pass

    def getMovesAt(self,sq:datatypes.Square) -> list[datatypes.Move]:
        piece = self.getPieceAt(sq)
        if piece is None: 
            return []
        return piece.getMoveList(board=self, from_sq=sq)

    def getColorAt(self, sq: datatypes.Square) -> datatypes.Color | None:
        piece = self.getPieceAt(sq)
        return None if piece is None else piece.color
    
    def isEmpty(self, sq: datatypes.Square) -> bool:
        if not self.isInbound(sq):
            raise ValueError(f"Square is not inbound row: '{sq.row}' col: '{sq.col}'")
        return True if self.getPieceAt(sq) is None else False

    def isEnemy(self, sq:datatypes.Square, color: datatypes.Color) -> bool:
        if not self.isInbound(sq):
            raise ValueError(f"Square is not inbound row: '{sq.row}' col: '{sq.col}'")
        piece = self.getPieceAt(sq)
        return piece is not None and piece.color != color
    
    def __repr__(self):
        rows: list[str] = []
        for i in range(self.size-1,-1,-1):
            row: list[str] = []
            for j in range(self.size):
                piece = self.getPieceAt(Square(i, j))
                
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