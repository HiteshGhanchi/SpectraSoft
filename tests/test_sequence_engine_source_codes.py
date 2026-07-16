from core.sequence_engine import SequenceEngine


class FakeSourceCode:
    def __init__(self, entry_no, name):
        self.entry_no = entry_no
        self.name = name


class FakeSession:
    def __init__(self, rows):
        self._rows = rows

    def query(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def all(self):
        return self._rows

    def close(self):
        pass


def test_sequence_engine_uses_database_source_codes(monkeypatch):
    rows = [FakeSourceCode(3, "Combined Spark")]
    fake_session = FakeSession(rows)

    monkeypatch.setattr("core.sequence_engine.get_session", lambda: fake_session)

    engine = SequenceEngine(uart=object())

    assert engine.get_source_nibble("3: Combined Spark") == 3
