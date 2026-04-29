from chess.core.pieces import Piece
from chess.core.board import BoardView
from chess.core.datatypes import Square, Move

class Knight(Piece):
    def getMoveList(self, board: BoardView, from_sq: Square) -> list[Move]:
        moveList: list[Move] = []
        for i in [(-2,(-1,1)),(-1,(-2,2)),(1,(-2,2)),(2,(-1,1))]:
            for j in i[1]:
                newSquare = Square(from_sq.row+i[0],from_sq.col+j)
                if not board.isAvailable(newSquare) and not board.isCapturable(newSquare, self.color):
                    continue
                moveList.append(Move(from_sq, newSquare))
                
        return moveList
