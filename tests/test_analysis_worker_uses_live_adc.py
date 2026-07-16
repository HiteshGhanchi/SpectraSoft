from PyQt6.QtWidgets import QApplication

from core.analysis_worker import AnalysisWorker


class FakeUART:
    is_connected = True


class FakeSequenceEngine:
    def __init__(self, uart):
        self.uart = uart
        self.calls = []

    def execute_full_sequence(self, page1_data, page3_data, progress_cb=None):
        self.calls.append((page1_data, page3_data))
        return {"Fe": 123}


def test_analysis_worker_prefers_live_adc_results(monkeypatch):
    app = QApplication.instance() or QApplication([])

    monkeypatch.setattr("core.analysis_worker.UARTManager", lambda: FakeUART())
    monkeypatch.setattr("core.analysis_worker.load_st_values", lambda st: {"Fe": 999})
    monkeypatch.setattr("core.analysis_worker.SequenceEngine", FakeSequenceEngine)

    worker = AnalysisWorker(group_id=1, params={"st_number": "ABCD"})
    worker._load_group_data = lambda: {
        "page_01_source": {"purge_seq1": "0"},
        "page_03_channel": [{"seq": "1", "itg": 1, "ele": "Fe"}],
    }

    results = []
    worker.result.connect(lambda payload: results.append(payload))
    worker.run()

    assert results
    assert results[0]["raw_adc"] == {"Fe": 123}
    assert results[0]["intensities"] == {"Fe": 123 / 4095}

    app.quit()


def test_analysis_worker_runs_sequence_once(monkeypatch):
    app = QApplication.instance() or QApplication([])

    class CountingSequenceEngine:
        def __init__(self, uart):
            self.uart = uart
            self.calls = 0

        def execute_full_sequence(self, page1_data, page3_data, progress_cb=None):
            self.calls += 1
            return {"Fe": 123}

    sequence_engine = CountingSequenceEngine(FakeUART())

    monkeypatch.setattr("core.analysis_worker.UARTManager", lambda: FakeUART())
    monkeypatch.setattr("core.analysis_worker.load_st_values", lambda st: {"Fe": 999})
    monkeypatch.setattr("core.analysis_worker.SequenceEngine", lambda uart: sequence_engine)

    worker = AnalysisWorker(group_id=1, params={"st_number": "ABCD"})
    worker._load_group_data = lambda: {
        "page_01_source": {"purge_seq1": "0"},
        "page_03_channel": [{"seq": "1", "itg": 1, "ele": "Fe"}],
    }

    worker.run()

    assert sequence_engine.calls == 1
    app.quit()
