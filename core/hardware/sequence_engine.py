"""Orchestrate the spectroscopy burn sequence through a controller interface."""

import time
from typing import Callable, Dict, List, Optional

from import_data.constants import DEFAULT_SOURCE_CODE, SOURCE_CODE_MAX, SOURCE_CODE_MIN
from core.hardware.interfaces.spectrometer import SpectrometerController


class SequenceEngine:
    """Execute the workflow without depending on UART command details."""

    def __init__(self, controller: SpectrometerController):
        self.controller = controller
        self._progress_cb = None

    def set_progress_callback(self, callback: Callable[[str, int], None]):
        """Set callback for progress updates."""
        self._progress_cb = callback

    def _progress(self, step: str, percent: int):
        if self._progress_cb:
            self._progress_cb(step, percent)

    def execute_reset(self) -> bool:
        self._progress("Resetting hardware...", 5)
        return self.controller.reset()

    def execute_argon_purge(self, purge_sec: float) -> bool:
        self._progress(f"Argon purge ({purge_sec}s)...", 10)
        return self.controller.argon_purge(purge_sec)

    def execute_prespark(self, source_code: int, preburn_ms: int) -> bool:
        self._progress(f"Prespark (0x{source_code:X}, {preburn_ms}ms)...", 15)
        return self.controller.prespark(source_code, preburn_ms)

    @staticmethod
    def _source_code_from_selection(selection) -> int:
        """Read the hexadecimal entry number saved by the source dropdown."""
        token = str(selection).split(":", 1)[0].strip()
        try:
            source_code = int(token, 16)
        except ValueError:
            source_code = DEFAULT_SOURCE_CODE
        return max(SOURCE_CODE_MIN, min(SOURCE_CODE_MAX, source_code))

    def execute_integration(self, integ_ms: int, elements: List[Dict]) -> Dict[str, int]:
        """Measure elements and emit progress using the returned element names."""
        self._progress(f"Integration ({integ_ms}ms)...", 20)
        results = self.controller.integrate(integ_ms, elements)

        for idx, element in enumerate(elements):
            name = element.get("ele", f"ele{element.get('itg', 0)}")
            percent = 20 + int((idx + 1) / len(elements) * 60)
            self._progress(f"Reading {name}...", percent)

        return results

    def execute_clean(self, clean_ms: int) -> bool:
        self._progress(f"Cleaning ({clean_ms}ms)...", 85)
        return self.controller.clean(clean_ms)

    def execute_shutdown(self) -> bool:
        self._progress("Shutting down...", 95)
        return self.controller.shutdown()

    def execute_full_sequence(
        self,
        page1_data: Dict,
        page3_data: List[Dict],
        progress_cb: Optional[Callable[[str, int], None]] = None,
    ) -> Dict[str, int]:
        """Execute the complete burn sequence."""
        if progress_cb:
            self.set_progress_callback(progress_cb)

        self._progress("Starting sequence...", 0)
        all_results: Dict[str, int] = {}

        if not self.execute_reset():
            self._progress("Reset failed!", 0)
            return all_results
        time.sleep(0.3)

        seq_keys = {"1": "seq1", "2": "seq2", "3": "seq3"}
        purge_sec = float(page1_data.get("purge_seq1", 3))

        for seq_num, seq_key in seq_keys.items():
            self._progress(f"Sequence {seq_num}...", 10 + int(seq_num) * 20)

            source_selection = page1_data.get(
                f"source_{seq_key}", f"{DEFAULT_SOURCE_CODE:X}: Normal Spark"
            )
            source_code = self._source_code_from_selection(source_selection)
            preburn_ms = int(page1_data.get(f"preburn_{seq_key}", 200))
            integ_ms = int(page1_data.get(f"integ_{seq_key}", 300))

            if integ_ms == 0:
                self._progress(f"SEQ{seq_num} skipped (integ=0)", 10 + int(seq_num) * 20)
                continue

            if not self.execute_argon_purge(purge_sec):
                self._progress(f"Argon purge failed in SEQ{seq_num}", 0)
                return all_results
            time.sleep(0.2)

            if not self.execute_prespark(source_code, preburn_ms):
                self._progress(f"Prespark failed in SEQ{seq_num}", 0)
                return all_results
            time.sleep(0.2)

            seq_elements = [element for element in page3_data if str(element.get("seq", "")) == seq_num]
            if seq_elements:
                all_results.update(self.execute_integration(integ_ms, seq_elements))
            time.sleep(0.2)

        clean_ms = int(page1_data.get("clean_value", 0))
        self.execute_clean(clean_ms)
        time.sleep(0.2)
        self.execute_shutdown()

        self._progress("Sequence complete!", 100)
        return all_results
