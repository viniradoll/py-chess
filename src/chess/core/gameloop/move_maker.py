from chess.core.datatypes import Move
from chess.core.pieces import Piece
from chess.core.board import Board
from chess.core.gameloop.move_history import MoveHistory, MoveRecord
class MoveMaker:
    def __init__(self, board: Board, history: MoveHistory | None = None):
        self.history = history if history is not None else MoveHistory()
        self.board: Board = board
    
    def make_move(self, move: Move) -> None:
        piece: Piece | None = self.board.get_piece_at(move.from_sq)
        if piece is None:
            raise ValueError("No piece in this square")

        captured: Piece | None = self.board.get_piece_at(move.to_sq)
        self.history.push(MoveRecord(move=move, captured_piece=captured, had_moved=piece.has_moved))

        piece.has_moved = True
        self.board.set_piece_at(move.to_sq, piece)
        self.board.set_piece_at(move.from_sq, None)

    def undo_move(self) -> None:
        record = self.history.pop()
        if record is None:
            return

        piece: Piece | None = self.board.get_piece_at(record.move.to_sq)
        piece.has_moved: bool = record.had_moved
        self.board.set_piece_at(record.move.from_sq, piece)
        self.board.set_piece_at(record.move.to_sq, record.captured_piece)