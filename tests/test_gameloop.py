import pytest
from chess.core.pieces import Pawn, Knight
from chess.core.datatypes import Color, Square, Move
from chess.core.game import Game
from pytest import fixture
from chess.core.board import MatrixBoard

W = Color.WHITE
B = Color.BLACK

@fixture
def empty_board() -> MatrixBoard:
    return MatrixBoard()

@fixture
def board(empty_board: MatrixBoard) -> MatrixBoard:
    empty_board.setup_starting_position()
    return empty_board

@fixture
def game(board: MatrixBoard) -> Game:
    g = Game(board)
    return g

def test_make_move(game: Game):
    game.make_move(W, "e2", "e4")
    assert game.board.get_piece_at(Square.from_algebraic("e2")) is None
    assert game.board.get_piece_at(Square.from_algebraic("e4")) == Pawn(W)

class TestAllMoves:
    def test_get_all_moves_white_pawn(self,game):
        assert Move(Square.from_algebraic("e2"),Square.from_algebraic("e4")) in game.get_all_moves(W)

    def test_get_all_moves_white_knight(self,game):
        assert Move(Square.from_algebraic("b1"),Square.from_algebraic("c3")) in game.get_all_moves(W)

    def test_get_all_moves_white_enemy_pawn(self,game):
        assert Move(Square.from_algebraic("c7"),Square.from_algebraic("c5")) not in game.get_all_moves(W)
        
    def test_get_all_moves_black_pawn(self,game):
        assert Move(Square.from_algebraic("e7"),Square.from_algebraic("e5")) in game.get_all_moves(B)

    def test_get_all_moves_black_knight(self,game):
        assert Move(Square.from_algebraic("b8"),Square.from_algebraic("c6")) in game.get_all_moves(B)

    def test_get_all_moves_black_enemy_pawn(self,game):
        assert Move(Square.from_algebraic("c2"),Square.from_algebraic("c4")) not in game.get_all_moves(B)

class TestMoveValidation:
    def test_valid_pawn_move(self,game: Game):
        game.make_move(W, "e2", "e4")

    def test_valid_horse_move(self,game: Game):
        game.make_move(W, "b1", "c3")

    def test_valid_move_sequence(self,game: Game):
        game.make_move(W, "e2", "e4")
        game.make_move(B, "b8", "c6")
        game.make_move(W, "d2", "d4")
        assert game.board.get_piece_at(Square.from_algebraic("d4")) == Pawn(W)
        game.make_move(B, "c6", "d4")
        assert game.board.get_piece_at(Square.from_algebraic("d4")) == Knight(B)

    def test_invalid_pawn_move(self,game: Game):
        with pytest.raises(ValueError):
            game.make_move(W, "e2", "d4")

    def test_move_to_occupied_square(self,game: Game):
        game.make_move(W, "c2", "c4")
        game.make_move(B, "b8", "c6")
        game.make_move(W, "c4", "c5")
        game.make_move(B, "a7", "a6")
        with pytest.raises(ValueError):
            game.make_move(W, "c5", "c6")
    
    def test_two_moves_in_sequence(self,game: Game):
        game.make_move(W, "c2", "c4")
        with pytest.raises(ValueError):
            game.make_move(W, "d2", "d4")

class TestCheck():
    def test_not_in_check(self,game: Game):
        assert not game.is_in_check(Color.WHITE)
        assert not game.is_in_check(Color.BLACK)

    def test_is_in_check(self,game: Game):
        game.board.move_piece(Move(Square.from_algebraic("e1"), Square.from_algebraic("c6")))
        game.board.move_piece(Move(Square.from_algebraic("e8"), Square.from_algebraic("d3")))
        assert game.is_in_check(Color.WHITE)
        assert game.is_in_check(Color.BLACK)