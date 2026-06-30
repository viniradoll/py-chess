from chess.core.datatypes import Square, Color
import chess.core.pieces as pieces


class FenParser:
    @classmethod
    def parse_fen(cls, fen: str) -> list[tuple[Square, pieces.Piece]]:
        piece_list: list[tuple[Square, pieces.Piece]] = []
        parts: list[str] = fen.split(" ")
        placement, turn, castling, en_passant, halfmove, fullmove = parts

        row = 7
        col = 0
        for char in placement:
            if char.isalpha():
                piece = cls.resolve_piece(char)
                piece_list.append((Square(row, col), piece))
                col += 1
            if char.isdigit():
                col += int(char)
            if char == "/":
                col = 0
                row -= 1
        return piece_list

    @classmethod
    def resolve_piece(cls, piece: str) -> pieces.Piece:
        piece = piece[0]
        color = Color.BLACK if piece.islower() else Color.WHITE
        match piece.lower():
            case "p":
                return pieces.Pawn(color)
            case "r":
                return pieces.Rook(color)
            case "n":
                return pieces.Knight(color)
            case "b":
                return pieces.Bishop(color)
            case "q":
                return pieces.Queen(color)
            case "k":
                return pieces.King(color)
            case _:
                raise ValueError("Unkown piece type")
