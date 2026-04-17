from .base import Piece
import chess.core.datatypes as datatypes
import chess.core.board as board

class Pawn(Piece):
    canPromote = True

    def getMoveList(self, board: board.BoardView, from_sq: datatypes.Square) -> list[datatypes.Move]:
        moveList: list[datatypes.Move] = []
        direction = 1 if self.color == datatypes.Color.WHITE else -1
        newSquare = datatypes.Square(from_sq.row+(1*direction), from_sq.col)
        if board.isAvailable(newSquare):
            moveList.append(datatypes.Move(from_sq,to_sq=newSquare))
        
            newSquare = datatypes.Square(from_sq.row+(2*direction), from_sq.col)
            if not self.hasMoved and board.isAvailable(newSquare):
                moveList.append(datatypes.Move(from_sq,to_sq=newSquare))

        newSquare = datatypes.Square(from_sq.row+(1*direction), from_sq.col+1)
        if board.isCapturable(newSquare, self.color):
            moveList.append(datatypes.Move(from_sq,to_sq=newSquare))

        newSquare = datatypes.Square(from_sq.row+(1*direction), from_sq.col-1)
        if board.isCapturable(newSquare, self.color):
            moveList.append(datatypes.Move(from_sq,to_sq=newSquare))

        return moveList