import pytest
import chess.core.board as board
import chess.core.datatypes as datatypes
import chess.core.pieces as pieces


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def empty_board() -> board.MatrixBoard:
    return board.MatrixBoard()


def board_with_pawn(
    row: int, col: int, color=datatypes.Color.WHITE
) -> tuple[board.MatrixBoard, datatypes.Square]:
    b = empty_board()
    sq = datatypes.Square(row, col)
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
        assert b.is_inbound(datatypes.Square(0, 0))
        assert b.is_inbound(datatypes.Square(7, 7))
        assert b.is_inbound(datatypes.Square(0, 7))
        assert b.is_inbound(datatypes.Square(7, 0))

    def test_out_of_bounds_positive(self):
        b = empty_board()
        assert not b.is_inbound(datatypes.Square(8, 0))
        assert not b.is_inbound(datatypes.Square(0, 8))
        assert not b.is_inbound(datatypes.Square(8, 8))

    def test_out_of_bounds_negative(self):
        b = empty_board()
        assert not b.is_inbound(datatypes.Square(-1, 0))
        assert not b.is_inbound(datatypes.Square(0, -1))
        assert not b.is_inbound(datatypes.Square(-1, -1))


# ---------------------------------------------------------------------------
# setPieceAt / getPieceAt
# ---------------------------------------------------------------------------


class TestSetAndGetPiece:
    def test_set_and_get(self):
        b = empty_board()
        sq = datatypes.Square(3, 4)
        pawn = pieces.Pawn(datatypes.Color.WHITE)
        b.set_piece_at(sq, pawn)
        assert b.get_piece_at(sq) is pawn

    def test_get_empty_square_returns_none(self):
        b = empty_board()
        assert b.get_piece_at(datatypes.Square(0, 0)) is None

    def test_set_out_of_bounds_raises(self):
        b = empty_board()
        with pytest.raises(ValueError):
            b.set_piece_at(datatypes.Square(8, 0), pieces.Pawn(datatypes.Color.WHITE))

    def test_set_negative_raises(self):
        b = empty_board()
        with pytest.raises(ValueError):
            b.set_piece_at(datatypes.Square(-1, 0), pieces.Pawn(datatypes.Color.WHITE))

    def test_get_out_of_bounds_raises(self):
        b = empty_board()
        with pytest.raises(ValueError):
            b.get_piece_at(datatypes.Square(8, 0))

    def test_overwrite_piece(self):
        b = empty_board()
        sq = datatypes.Square(0, 0)
        pawn = pieces.Pawn(datatypes.Color.WHITE)
        pawn2 = pieces.Pawn(datatypes.Color.BLACK)
        b.set_piece_at(sq, pawn)
        b.set_piece_at(sq, pawn2)
        assert b.get_piece_at(sq) is pawn2


# ---------------------------------------------------------------------------
# isEmpty / isEnemy / isAvailable / isCapturable / getColorAt
# ---------------------------------------------------------------------------


class TestBoardQueries:
    def test_is_empty_on_empty_square(self):
        b = empty_board()
        assert b.is_empty(datatypes.Square(0, 0))

    def test_is_empty_on_occupied_square(self):
        b, sq = board_with_pawn(3, 3)
        assert not b.is_empty(sq)

    def test_is_empty_out_of_bounds_raises(self):
        b = empty_board()
        with pytest.raises(ValueError):
            b.is_empty(datatypes.Square(8, 0))

    def test_get_color_at_empty_returns_none(self):
        b = empty_board()
        assert b.get_color_at(datatypes.Square(0, 0)) is None

    def test_get_color_at_returns_correct_color(self):
        b, sq = board_with_pawn(3, 3, datatypes.Color.BLACK)
        assert b.get_color_at(sq) == datatypes.Color.BLACK

    def test_is_enemy_against_opposite_color(self):
        b, sq = board_with_pawn(3, 3, datatypes.Color.BLACK)
        assert b.is_enemy(sq, datatypes.Color.WHITE)

    def test_is_enemy_against_same_color(self):
        b, sq = board_with_pawn(3, 3, datatypes.Color.WHITE)
        assert not b.is_enemy(sq, datatypes.Color.WHITE)

    def test_is_enemy_on_empty_square(self):
        b = empty_board()
        assert not b.is_enemy(datatypes.Square(0, 0), datatypes.Color.WHITE)

    def test_is_enemy_out_of_bounds_raises(self):
        b = empty_board()
        with pytest.raises(ValueError):
            b.is_enemy(datatypes.Square(-1, 0), datatypes.Color.WHITE)

    def test_is_available_empty_inbound(self):
        b = empty_board()
        assert b.is_available(datatypes.Square(0, 0))

    def test_is_available_occupied(self):
        b, sq = board_with_pawn(2, 2)
        assert not b.is_available(sq)

    def test_is_available_out_of_bounds(self):
        b = empty_board()
        assert not b.is_available(datatypes.Square(8, 8))

    def test_is_capturable_enemy(self):
        b, sq = board_with_pawn(4, 4, datatypes.Color.BLACK)
        assert b.is_capturable(sq, datatypes.Color.WHITE)

    def test_is_capturable_ally(self):
        b, sq = board_with_pawn(4, 4, datatypes.Color.WHITE)
        assert not b.is_capturable(sq, datatypes.Color.WHITE)

    def test_is_capturable_empty(self):
        b = empty_board()
        assert not b.is_capturable(datatypes.Square(4, 4), datatypes.Color.WHITE)

    def test_is_capturable_out_of_bounds(self):
        b = empty_board()
        assert not b.is_capturable(datatypes.Square(-1, 0), datatypes.Color.WHITE)


class TestBoardMoves:
    def test_piece_moves(self):
        b, sq = board_with_pawn(2, 2, datatypes.Color.WHITE)
        move = datatypes.Move(sq, datatypes.Square(3, 2))
        b.move_piece(move)
        assert b.get_piece_at(move.to_sq) == pieces.Pawn(datatypes.Color.WHITE)

    def test_piece_leaves_blank_square(self):
        b, sq = board_with_pawn(2, 2, datatypes.Color.WHITE)
        move = datatypes.Move(sq, datatypes.Square(3, 2))
        b.move_piece(move)
        assert b.get_piece_at(move.from_sq) is None
