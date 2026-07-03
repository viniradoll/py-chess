import chess.core.board as board
import chess.core.datatypes as datatypes
import chess.core.pieces as pieces
from chess.core.pieces.bishop import Bishop
from chess.core.pieces.rook import Rook
from chess.core.pieces.queen import Queen
from chess.core.pieces.king import King
from chess.core.pieces.knight import Knight


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def empty_board() -> board.MatrixBoard:
    return board.MatrixBoard()


def place(
    b: board.MatrixBoard, row: int, col: int, piece: pieces.Piece
) -> datatypes.Square:
    sq = datatypes.Square(row, col)
    b.set_piece_at(sq, piece)
    return sq


def moves_to(b: board.MatrixBoard, sq: datatypes.Square) -> set[tuple[int, int]]:
    return {(m.to_sq.row, m.to_sq.col) for m in b.get_moves_at(sq)}


# ---------------------------------------------------------------------------
# Pawn
# ---------------------------------------------------------------------------


class TestPawn:
    def test_returns_list(self):
        b = empty_board()
        sq = place(b, 1, 4, pieces.Pawn(datatypes.Color.WHITE))
        assert isinstance(b.get_moves_at(sq), list)

    def test_first_move_two_squares(self):
        b = empty_board()
        sq = place(b, 1, 4, pieces.Pawn(datatypes.Color.WHITE))
        destinations = moves_to(b, sq)
        assert (2, 4) in destinations
        assert (3, 4) in destinations
        assert len(destinations) == 2

    def test_after_moved_only_one_square(self):
        b = empty_board()
        pawn = pieces.Pawn(datatypes.Color.WHITE)
        pawn.has_moved = True
        sq = place(b, 3, 4, pawn)
        destinations = moves_to(b, sq)
        assert (4, 4) in destinations
        assert (5, 4) not in destinations
        assert len(destinations) == 1

    def test_blocked_by_own_piece(self):
        b = empty_board()
        sq = place(b, 1, 4, pieces.Pawn(datatypes.Color.WHITE))
        place(b, 2, 4, pieces.Pawn(datatypes.Color.WHITE))
        assert len(moves_to(b, sq)) == 0

    def test_capture_diagonal(self):
        b = empty_board()
        sq = place(b, 3, 3, pieces.Pawn(datatypes.Color.WHITE))
        place(b, 4, 4, pieces.Pawn(datatypes.Color.BLACK))
        destinations = moves_to(b, sq)
        assert (4, 4) in destinations

    def test_no_capture_same_color(self):
        b = empty_board()
        sq = place(b, 3, 3, pieces.Pawn(datatypes.Color.WHITE))
        place(b, 4, 4, pieces.Pawn(datatypes.Color.WHITE))
        destinations = moves_to(b, sq)
        assert (4, 4) not in destinations

    def test_at_edge_no_out_of_bounds_error(self):
        b = empty_board()
        sq = place(b, 0, 0, pieces.Pawn(datatypes.Color.WHITE))
        # deve funcionar sem levantar exceção
        result = b.get_moves_at(sq)
        assert isinstance(result, list)

    def test_can_promote_flag(self):
        assert pieces.Pawn(datatypes.Color.WHITE).can_promote is True


# ---------------------------------------------------------------------------
# SlidingPiece genérica
# ---------------------------------------------------------------------------


class TestSlidingPiece:
    def _make_sliding(self, directions):
        class Generic(pieces.SlidingPiece):
            def directions(self):
                return directions

        return Generic

    def test_single_direction_full_range(self):
        cls = self._make_sliding([(1, 0)])
        b = empty_board()
        sq = place(b, 1, 0, cls(datatypes.Color.WHITE))
        result = b.get_moves_at(sq)
        assert len(result) == 6  # linhas 2..7

    def test_stops_at_ally(self):
        cls = self._make_sliding([(1, 0)])
        b = empty_board()
        sq = place(b, 1, 0, cls(datatypes.Color.WHITE))
        place(b, 4, 0, pieces.Pawn(datatypes.Color.WHITE))
        destinations = moves_to(b, sq)
        # pode ir até linha 3, mas não 4 nem além
        assert (3, 0) in destinations
        assert (4, 0) not in destinations
        assert (5, 0) not in destinations

    def test_captures_enemy_and_stops(self):
        cls = self._make_sliding([(1, 0)])
        b = empty_board()
        sq = place(b, 1, 0, cls(datatypes.Color.WHITE))
        place(b, 4, 0, pieces.Pawn(datatypes.Color.BLACK))
        destinations = moves_to(b, sq)
        assert (4, 0) in destinations  # captura
        assert (5, 0) not in destinations  # não passa

    def test_diagonal_direction(self):
        cls = self._make_sliding([(1, 1), (-1, -1)])
        b = empty_board()
        sq = place(b, 3, 3, cls(datatypes.Color.WHITE))
        result = b.get_moves_at(sq)
        for move in result:
            # ambas as direções mantêm row == col
            assert move.to_sq.row == move.to_sq.col
            assert move.to_sq != sq

    def test_all_moves_reference_origin(self):
        cls = self._make_sliding([(0, 1)])
        b = empty_board()
        sq = place(b, 0, 0, cls(datatypes.Color.WHITE))
        for move in b.get_moves_at(sq):
            assert move.from_sq == sq


# ---------------------------------------------------------------------------
# Bishop
# ---------------------------------------------------------------------------


class TestBishop:
    def test_moves_only_diagonals(self):
        b = empty_board()
        sq = place(b, 3, 3, Bishop(datatypes.Color.WHITE))
        for move in b.get_moves_at(sq):
            dr = abs(move.to_sq.row - sq.row)
            dc = abs(move.to_sq.col - sq.col)
            assert dr == dc  # diagonal pura

    def test_center_has_13_moves(self):
        b = empty_board()
        sq = place(b, 3, 3, Bishop(datatypes.Color.WHITE))
        assert len(b.get_moves_at(sq)) == 13

    def test_corner_has_7_moves(self):
        b = empty_board()
        sq = place(b, 0, 0, Bishop(datatypes.Color.WHITE))
        assert len(b.get_moves_at(sq)) == 7


# ---------------------------------------------------------------------------
# Rook
# ---------------------------------------------------------------------------


class TestRook:
    def test_moves_only_straight(self):
        b = empty_board()
        sq = place(b, 3, 3, Rook(datatypes.Color.WHITE))
        for move in b.get_moves_at(sq):
            dr = move.to_sq.row - sq.row
            dc = move.to_sq.col - sq.col
            assert dr == 0 or dc == 0  # linha ou coluna

    def test_center_has_14_moves(self):
        b = empty_board()
        sq = place(b, 3, 3, Rook(datatypes.Color.WHITE))
        assert len(b.get_moves_at(sq)) == 14

    def test_secundary_castle_flag(self):
        assert Rook(datatypes.Color.WHITE).secundary_castle_piece is True


# ---------------------------------------------------------------------------
# Queen
# ---------------------------------------------------------------------------


class TestQueen:
    def test_center_has_27_moves(self):
        b = empty_board()
        sq = place(b, 3, 3, Queen(datatypes.Color.WHITE))
        assert len(b.get_moves_at(sq)) == 27

    def test_moves_include_all_directions(self):
        b = empty_board()
        sq = place(b, 3, 3, Queen(datatypes.Color.WHITE))
        destinations = moves_to(b, sq)
        assert (3, 7) in destinations  # horizontal direita
        assert (3, 0) in destinations  # horizontal esquerda
        assert (7, 3) in destinations  # vertical acima
        assert (0, 3) in destinations  # vertical abaixo
        assert (7, 7) in destinations  # diagonal NE
        assert (0, 0) in destinations  # diagonal SW


# ---------------------------------------------------------------------------
# King
# ---------------------------------------------------------------------------


class TestKing:
    def test_center_has_8_moves(self):
        b = empty_board()
        sq = place(b, 3, 3, King(datatypes.Color.WHITE))
        assert len(b.get_moves_at(sq)) == 8

    def test_corner_has_3_moves(self):
        b = empty_board()
        sq = place(b, 0, 0, King(datatypes.Color.WHITE))
        assert len(b.get_moves_at(sq)) == 3

    def test_cannot_move_to_ally(self):
        b = empty_board()
        sq = place(b, 3, 3, King(datatypes.Color.WHITE))
        place(b, 4, 4, pieces.Pawn(datatypes.Color.WHITE))
        destinations = moves_to(b, sq)
        assert (4, 4) not in destinations

    def test_can_capture_enemy(self):
        b = empty_board()
        sq = place(b, 3, 3, King(datatypes.Color.WHITE))
        place(b, 4, 4, pieces.Pawn(datatypes.Color.BLACK))
        destinations = moves_to(b, sq)
        assert (4, 4) in destinations

    def test_all_moves_one_step(self):
        b = empty_board()
        sq = place(b, 3, 3, King(datatypes.Color.WHITE))
        for move in b.get_moves_at(sq):
            assert abs(move.to_sq.row - sq.row) <= 1
            assert abs(move.to_sq.col - sq.col) <= 1

    def test_primary_castle_flag(self):
        assert (
            King(datatypes.Color.WHITE).primary_castle_piece is True
        ) 


# ---------------------------------------------------------------------------
# Knight
# ---------------------------------------------------------------------------


class TestKnight:
    def test_center_has_8_moves(self):
        b = empty_board()
        sq = place(b, 3, 3, Knight(datatypes.Color.WHITE))
        assert len(b.get_moves_at(sq)) == 8

    def test_corner_has_3_moves(self):
        b = empty_board()
        sq = place(b, 0, 0, Knight(datatypes.Color.WHITE))
        assert len(b.get_moves_at(sq)) == 2


# ---------------------------------------------------------------------------
# Datatypes
# ---------------------------------------------------------------------------


class TestDatatypes:
    def test_colors_are_distinct(self):
        assert datatypes.Color.WHITE != datatypes.Color.BLACK

    def test_square_equality(self):
        assert datatypes.Square(3, 4) == datatypes.Square(3, 4)

    def test_square_inequality(self):
        assert datatypes.Square(3, 4) != datatypes.Square(4, 3)

    def test_square_not_equal_to_other_type(self):
        assert datatypes.Square(3, 4) != (3, 4)

    def test_move_stores_squares(self):
        a = datatypes.Square(0, 0)
        b = datatypes.Square(1, 1)
        move = datatypes.Move(a, b)
        assert move.from_sq == a
        assert move.to_sq == b
