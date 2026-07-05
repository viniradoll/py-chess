import pytest
from unittest.mock import MagicMock
from chess.core.gameloop.move_history import MoveHistory, MoveRecord


@pytest.fixture
def history():
    return MoveHistory()


@pytest.fixture
def sample_record():
    return MoveRecord(move=MagicMock(), captured_piece=MagicMock(), had_moved=False)


class TestMoveHistoryPush:
    def test_push_then_pop_returns_same_record(self, history, sample_record):
        history.push(sample_record)
        assert history.pop() == sample_record

    def test_push_does_not_raise_on_multiple_calls(self, history):
        for _ in range(5):
            history.push(MoveRecord(move=MagicMock(), captured_piece=None, had_moved=False))
        # se push não fosse idempotente/aditivo corretamente, isso quebraria os pops abaixo
        for _ in range(5):
            assert history.pop() is not None


class TestMoveHistoryPop:
    def test_pop_on_empty_history_returns_none(self, history):
        assert history.pop() is None

    def test_pop_does_not_raise_when_called_repeatedly_on_empty(self, history):
        # list.pop() sem guard levantaria IndexError; aqui deve ser sempre None
        assert history.pop() is None
        assert history.pop() is None

    def test_pop_respects_lifo_order(self, history):
        record_a = MoveRecord(move=MagicMock(), captured_piece=None, had_moved=False)
        record_b = MoveRecord(move=MagicMock(), captured_piece=None, had_moved=True)
        record_c = MoveRecord(move=MagicMock(), captured_piece=MagicMock(), had_moved=False)

        history.push(record_a)
        history.push(record_b)
        history.push(record_c)

        assert history.pop() == record_c
        assert history.pop() == record_b
        assert history.pop() == record_a

    def test_pop_after_draining_all_records_returns_none(self, history, sample_record):
        history.push(sample_record)
        history.pop()
        assert history.pop() is None

    def test_pop_with_none_captured_piece_preserves_none(self, history):
        record = MoveRecord(move=MagicMock(), captured_piece=None, had_moved=False)
        history.push(record)
        popped = history.pop()
        assert popped.captured_piece is None


class TestMoveRecordInvariants:
    def test_records_with_equal_fields_compare_equal(self):
        move = MagicMock()
        piece = MagicMock()
        record_1 = MoveRecord(move=move, captured_piece=piece, had_moved=True)
        record_2 = MoveRecord(move=move, captured_piece=piece, had_moved=True)
        assert record_1 == record_2

    def test_record_is_immutable(self, sample_record):
        with pytest.raises(AttributeError):
            sample_record.had_moved = True