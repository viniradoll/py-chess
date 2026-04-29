import chess.core.pieces as pieces
import chess.core.datatypes as datatypes

class Position:
    __defaultFenPosition: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen: str = __defaultFenPosition):
        self.fen = fen
        self.pieces: list[tuple[datatypes.Square, pieces.Piece]]  = []    
        self.setup()
    
    def setup(self):
        self.pieces = FenParser.parseFen(self.fen)

class FenParser:
    @classmethod
    def parseFen(cls,fen: str) -> list[tuple[datatypes.Square, pieces.Piece]]:
        pieceList: list[tuple[datatypes.Square, pieces.Piece]] = []
        parts: list[str] = fen.split(' ')
        placement, turn, castling, en_passant, halfmove, fullmove = parts

        row = 7
        col = 0
        for char in placement:
            if char.isalpha():
                piece = cls.resolvePiece(char)
                pieceList.append((datatypes.Square(row,col),piece))
                col += 1
            if char.isdigit():
                col += int(char)
            if char == '/':
                col = 0
                row -= 1
        return pieceList
    
    @classmethod
    def resolvePiece(cls,piece: str) -> pieces.Piece:
        piece = piece[0]
        color = datatypes.Color.BLACK if piece.islower() else datatypes.Color.WHITE
        match piece.lower():
            case 'p':
                return pieces.Pawn(color)
            case 'r':
                return pieces.Rook(color)
            case 'n':
                return pieces.Knight(color)
            case 'b':
                return pieces.Bishop(color)
            case 'q':
                return pieces.Queen(color)
            case 'k':
                return pieces.King(color)
            case _:
                raise ValueError("Unkown piece type")

        