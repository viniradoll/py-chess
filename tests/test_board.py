from socket import fromfd
from chess.core.datatypes import Color, Square, Move
from chess.core.board.matrix import MatrixBoard
import pytest
import chess.core.board as board
import chess.core.pieces as pieces


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def empty_board() -> board.MatrixBoard:
    return board.MatrixBoard()


def board_with_pawn(
    row: int, col: int, color=Color.WHITE
) -> tuple[board.MatrixBoard, Square]:
    b = empty_board()
    sq = Square(row, col)
    b.set_piece_at(sq, pieces.Pawn(color))
    return b, sq


# ---------------------------------------------------------------------------
# MatrixBoard — inicialização
# ---------------------------------------------------------------------------


class TestMatrixBoardInit:
    def test_default_size(self):
        b = empty_board()
        assert b.size == 8

    def test_grid_starts_empty(self):
        b = empty_board()
        for row in b.grid:
            assert all(cell is None for cell in row)

    def test_custom_size(self):
        b = board.MatrixBoard(size=10)
        assert b.size == 10
        assert len(b.grid) == 10
        assert all(len(row) == 10 for row in b.grid)


# ---------------------------------------------------------------------------
# isInbound
# ---------------------------------------------------------------------------


class TestIsInbound:
    def test_valid_corners(self):
        b = empty_board()
        assert b.is_inbound(Square(0, 0))
        assert b.is_inbound(Square(7, 7))
        assert b.is_inbound(Square(0, 7))
        assert b.is_inbound(Square(7, 0))

    def test_out_of_bounds_positive(self):
        b = empty_board()
        assert not b.is_inbound(Square(8, 0))
        assert not b.is_inbound(Square(0, 8))
        assert not b.is_inbound(Square(8, 8))

    def test_out_of_bounds_negative(self):
        b = empty_board()
        assert not b.is_inbound(Square(-1, 0))
        assert not b.is_inbound(Square(0, -1))
        assert not b.is_inbound(Square(-1, -1))


# ---------------------------------------------------------------------------
# setPieceAt / getPieceAt
# ---------------------------------------------------------------------------


class TestSetAndGetPiece:
    def test_set_and_get(self):
        b = empty_board()
        sq = Square(3, 4)
        pawn = pieces.Pawn(Color.WHITE)
        b.set_piece_at(sq, pawn)
        assert b.get_piece_at(sq) is pawn

    def test_get_empty_square_returns_none(self):
        b = empty_board()
        assert b.get_piece_at(Square(0, 0)) is None

    def test_set_out_of_bounds_raises(self):
        b = empty_board()
        with pytest.raises(ValueError):
            b.set_piece_at(Square(8, 0), pieces.Pawn(Color.WHITE))

    def test_set_negative_raises(self):
        b = empty_board()
        with pytest.raises(ValueError):
            b.set_piece_at(Square(-1, 0), pieces.Pawn(Color.WHITE))

    def test_get_out_of_bounds_raises(self):
        b = empty_board()
        with pytest.raises(ValueError):
            b.get_piece_at(Square(8, 0))

    def test_overwrite_piece(self):
        b = empty_board()
        sq = Square(0, 0)
        pawn = pieces.Pawn(Color.WHITE)
        pawn2 = pieces.Pawn(Color.BLACK)
        b.set_piece_at(sq, pawn)
        b.set_piece_at(sq, pawn2)
        assert b.get_piece_at(sq) is pawn2


# ---------------------------------------------------------------------------
# isEmpty / isEnemy / isAvailable / isCapturable / getColorAt
# ---------------------------------------------------------------------------


class TestBoardQueries:
    def test_is_empty_on_empty_square(self):
        b = empty_board()
        assert b.is_empty(Square(0, 0))

    def test_is_empty_on_occupied_square(self):
        b, sq = board_with_pawn(3, 3)
        assert not b.is_empty(sq)

    def test_is_empty_out_of_bounds_raises(self):
        b = empty_board()
        with pytest.raises(ValueError):
            b.is_empty(Square(8, 0))

    def test_get_color_at_empty_returns_none(self):
        b = empty_board()
        assert b.get_color_at(Square(0, 0)) is None

    def test_get_color_at_returns_correct_color(self):
        b, sq = board_with_pawn(3, 3, Color.BLACK)
        assert b.get_color_at(sq) == Color.BLACK

    def test_is_enemy_against_opposite_color(self):
        b, sq = board_with_pawn(3, 3, Color.BLACK)
        assert b.is_enemy(sq, Color.WHITE)

    def test_is_enemy_against_same_color(self):
        b, sq = board_with_pawn(3, 3, Color.WHITE)
        assert not b.is_enemy(sq, Color.WHITE)

    def test_is_enemy_on_empty_square(self):
        b = empty_board()
        assert not b.is_enemy(Square(0, 0), Color.WHITE)

    def test_is_enemy_out_of_bounds_raises(self):
        b = empty_board()
        with pytest.raises(ValueError):
            b.is_enemy(Square(-1, 0), Color.WHITE)

    def test_is_available_empty_inbound(self):
        b = empty_board()
        assert b.is_available(Square(0, 0))

    def test_is_available_occupied(self):
        b, sq = board_with_pawn(2, 2)
        assert not b.is_available(sq)

    def test_is_available_out_of_bounds(self):
        b = empty_board()
        assert not b.is_available(Square(8, 8))

    def test_is_capturable_enemy(self):
        b, sq = board_with_pawn(4, 4, Color.BLACK)
        assert b.is_capturable(sq, Color.WHITE)

    def test_is_capturable_ally(self):
        b, sq = board_with_pawn(4, 4, Color.WHITE)
        assert not b.is_capturable(sq, Color.WHITE)

    def test_is_capturable_empty(self):
        b = empty_board()
        assert not b.is_capturable(Square(4, 4), Color.WHITE)

    def test_is_capturable_out_of_bounds(self):
        b = empty_board()
        assert not b.is_capturable(Square(-1, 0), Color.WHITE)


class TestBoardMoves:
    def test_piece_moves(self):
        b, sq = board_with_pawn(2, 2, Color.WHITE)
        move = Move(sq, Square(3, 2))
        b.move_piece(move)
        assert b.get_piece_at(move.to_sq) == pieces.Pawn(Color.WHITE)

    def test_piece_leaves_blank_square(self):
        b, sq = board_with_pawn(2, 2, Color.WHITE)
        move = Move(sq, Square(3, 2))
        b.move_piece(move)
        assert b.get_piece_at(move.from_sq) is None

@pytest.fixture
def seen_white():
    b = MatrixBoard()
    b.setup_starting_position()
    return b.get_seen_squares(Color.WHITE)

class TestSeenSquares:
    def test_unseen_squares_starting_pos(self,seen_white):
        unseen = ["a1","a4","a5","h1","h4","h5","e4","e8","g8"]
        assert all(Square.from_algebraic(pos) not in seen_white for pos in unseen)

    def test_seen_squares_starting_pos(self,seen_white):
        seen = ["b1","b3","c2","f1","e1","d1","d3","f3","c1"]
        assert all(Square.from_algebraic(pos) in seen_white for pos in seen)