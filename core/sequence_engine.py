"""
SpectraSoft — Sequence Engine
Executes the full burn sequence using UARTManager.
"""

import time
from typing import Dict, List, Optional, Callable
from core.uart_manager import UARTManager

class SequenceEngine:
    """Executes the full spectroscopy sequence."""

    # Source name → 4-bit nibble map. These occupy bits A0-A3 (LSB) of the
    # Port B byte, sent as-is (no shifting) — see PORT B BYTE LAYOUT below.
    SOURCE_NIBBLE_MAP = {
        "3 Peak Spark":  0b1011,
        "Normal Spark":  0b1001,
        "Combined":      0b1000,
        "Reverse":       0b1111,
        "HighPower":     0b1010,
        "Cleaning":      0b1100,  # placeholder
        "Lamp":          0b0000,

    }

    # ─────────────────────────────────────────────────────────────────────
    # PORT B BYTE LAYOUT (7 bits used, sent over UART as "O,B,<hex>")
    #   Bit:   6      5       4      3   2   1   0
    #   Name:  D      C       B      A   A   A   A
    #          empty  START   STOP   ── source nibble (LSB) ──
    #
    #   A = source nibble (bits 0-3, LSB group) — NOT shifted
    #   B = STOP  bit (bit 4) = 0x10
    #   C = START bit (bit 5) = 0x20
    #   D = unused (bit 6)    = 0
    #
    #   Byte is sent exactly as composed — never OR'd with any other
    #   existing Port B state.
    # ─────────────────────────────────────────────────────────────────────
    STOP_BIT  = 0x10   # Port B bit 4 ("B" / stop condition)
    START_BIT = 0x20   # Port B bit 5 ("C" / start condition)

    # Timing constants (matched with MCU firmware)
    ELEM_SELECT_DELAY = 0.100   # 100ms after element select
    ADC_INTER_DELAY   = 0.010   # 10ms between ADC triggers
    ADC_SETTLE_DELAY  = 0.100   # 100ms after 3C trigger
    RESET_HOLD_TIME   = 0.5     # 500ms reset hold

    def __init__(self, uart: UARTManager):
        self.uart = uart
        self._progress_cb = None

    def set_progress_callback(self, callback: Callable[[str, int], None]):
        """Set callback for progress updates."""
        self._progress_cb = callback

    def _progress(self, step: str, percent: int):
        """Emit progress update."""
        if self._progress_cb:
            self._progress_cb(step, percent)

    # =========================================================================
    # PORT B — STOP BIT HELPERS
    # =========================================================================

    def pulse_stop_bit(self) -> bool:
        """
        Pulse the STOP bit (bit 4 / 0x10) on Port B: send it HIGH, then LOW.
        Sent as a bare byte — not OR'd with the source nibble or any other
        Port B state. Used:
          - once, before anything else runs (before Reset)
          - once, after each sequence's integration completes
        """
        # STOP bit HIGH
        if not self.uart.send_command(f"O,B,{self.STOP_BIT:02X}",
wait_ack=True):
            return False
        # STOP bit LOW
        if not self.uart.send_command("O,B,00", wait_ack=True):
            return False
        return True

    def set_stop_bit_on(self) -> bool:
        """
        Set the STOP bit (bit 4 / 0x10) HIGH and leave it there (no pulse-low).
        Used once, after Clean, before Shutdown.
        """
        return self.uart.send_command(f"O,B,{self.STOP_BIT:02X}", wait_ack=True)

    # =========================================================================
    # STEP 1: RESET
    # =========================================================================

    def execute_reset(self) -> bool:
        """Execute the reset sequence: 9E → wait → C3"""
        self._progress("Resetting hardware...", 5)
        if not self.uart.send_command("O,A,9E", wait_ack=True):
            return False
        time.sleep(self.RESET_HOLD_TIME)
        if not self.uart.send_command("O,A,C3", wait_ack=True):
            return False
        time.sleep(self.RESET_HOLD_TIME)
        return True

    # =========================================================================
    # STEP 2: ARGON FLUSH + PRESPARK
    # =========================================================================

    def execute_argon_purge(self, purge_sec: float) -> bool:
        """Open argon valve for purge_sec seconds."""
        self._progress(f"Argon purge ({purge_sec}s)...", 10)
        if not self.uart.send_command("O,A,CB", wait_ack=True):
            return False
        time.sleep(purge_sec)
        return True

    def execute_prespark(self, source_name: str, preburn_ms: int) -> bool:
        """Execute prespark with the given source."""
        self._progress(f"Prespark ({source_name}, {preburn_ms}ms)...", 15)

        # Enable prespark
        if not self.uart.send_command("O,A,C9", wait_ack=True):
            return False

        # Select source: Port B START-bit pulse combined with the source
        # nibble (nibble sits in bits A0-A3, unshifted — see PORT B BYTE
        # LAYOUT above). START bit (0x20) goes HIGH then LOW; nibble stays
        # present in both bytes.
        nibble = self.SOURCE_NIBBLE_MAP.get(source_name, 0b0000)
        ob_byte_start_high = nibble | self.START_BIT  # nibble + START bit HIGH
        ob_byte_start_low  = nibble                   # nibble, START bit LOW
        if not self.uart.send_command(f"O,B,{ob_byte_start_high:02X}",
wait_ack=True):
            return False
        if not self.uart.send_command(f"O,B,{ob_byte_start_low:02X}",
wait_ack=True):
            return False

        # Wait for preburn duration
        time.sleep(preburn_ms / 1000.0)
        return True

    # =========================================================================
    # STEP 3: INTEGRATION + ADC READS
    # =========================================================================

    def execute_integration(self, integ_ms: int, elements: List[Dict])->Dict[str, int]:
        """
        Execute integration and read ADC for each element.

        Args:
            integ_ms: Integration time in milliseconds
            elements: List of dicts with 'itg' and 'ele' keys

        Returns:
            Dict of {element_name: adc_value}
        """
        self._progress(f"Integration ({integ_ms}ms)...", 20)
        results = {}

        # Integration trigger
        if not self.uart.send_command("O,A,8C", wait_ack=True):
            return results
        time.sleep(integ_ms / 1000.0)

        # Port B integration condition
        if not self.uart.send_command("O,B,20", wait_ack=True):
            return results

        # Read each element
        for idx, elem in enumerate(elements):
            itg = elem.get("itg", 0)
            name = elem.get("ele", f"ele{itg}")
            elem_hex = f"{int(itg) - 1:02X}"  # ITG 1 → 0x00
            # Select element
            if not self.uart.send_command(f"O,A,{elem_hex}", wait_ack=True):
                continue
            time.sleep(self.ELEM_SELECT_DELAY)

            # ADC Trigger 1
            if not self.uart.send_command("O,A,C9", wait_ack=True):
                continue
            time.sleep(self.ADC_INTER_DELAY)

            # ADC Trigger 2
            if not self.uart.send_command("O,A,CD", wait_ack=True):
                continue
            time.sleep(self.ADC_INTER_DELAY)

            # ADC Trigger 3
            if not self.uart.send_command("O,A,C9", wait_ack=True):
                continue
            time.sleep(self.ADC_SETTLE_DELAY)

            # Read the value
            self.uart.send_command("I", wait_ack=False)
            value = self.uart.read_adc_value()
            if value is not None:
                results[name] = value

            # Update progress
            pct = 20 + int((idx + 1) / len(elements) * 60)
            self._progress(f"Reading {name}...", pct)

        return results

    # =========================================================================
    # STEP 4: CLEAN
    # =========================================================================

    def execute_clean(self, clean_ms: int) -> bool:
        """Execute cleaning spark."""
        self._progress(f"Cleaning ({clean_ms}ms)...", 85)
        if not self.uart.send_command("O,A,9C", wait_ack=True):
            return False
        time.sleep(clean_ms / 1000.0)
        return True

    # =========================================================================
    # STEP 5: SHUTDOWN
    # =========================================================================

    def execute_shutdown(self) -> bool:
        """Send shutdown commands."""
        self._progress("Shutting down...", 95)
        if not self.uart.send_command("O,A,C2", wait_ack=True):
            return False
        if not self.uart.send_command("O,A,00", wait_ack=True):
            return False
        return True

    # =========================================================================
    # FULL SEQUENCE
    # =========================================================================

    def execute_full_sequence(
        self,
        page1_data: Dict,
        page3_data: List[Dict],
        progress_cb: Optional[Callable[[str, int], None]] = None
    ) -> Dict[str, int]:
        """
        Execute the complete burn sequence.

        Args:
            page1_data: Dictionary from page_01_condition
            page3_data: List of dicts from page_03_channel
            progress_cb: Optional progress callback

        Returns:
            Dict of {element_name: adc_value}
        """
        if progress_cb:
            self.set_progress_callback(progress_cb)

        self._progress("Starting sequence...", 0)
        all_results = {}

        # ── Step 0: Stop-bit pulse ───────────────────────────────────────
        # Before any other command is sent: pulse Port B STOP bit (0x10)
        # HIGH then LOW.
        self._progress("Stop-bit pulse (pre-run)...", 1)
        if not self.pulse_stop_bit():
            self._progress("Stop-bit pulse failed!", 0)
            return all_results

        # ── Step 1: Reset ──────────────────────────────────────────────────
        if not self.execute_reset():
            self._progress("Reset failed!", 0)
            return all_results
        time.sleep(0.3)

        # ── Step 2 & 3: For each sequence ──────────────────────────────
        seq_keys = {"1": "seq1", "2": "seq2", "3": "seq3"}

        # Get purge value (in seconds, from page1)
        purge_sec = float(page1_data.get("purge_seq1", 3))

        for seq_num, seq_key in seq_keys.items():
            self._progress(f"Sequence {seq_num}...", 10 + int(seq_num) * 20)

            source_name = page1_data.get(f"source_{seq_key}", "Normal Spark")
            # Values from UI are in seconds, convert to ms for the engine
            preburn_ms = int(page1_data.get(f"preburn_{seq_key}", 2)) * 1000
            integ_ms = int(page1_data.get(f"integ_{seq_key}", 3)) * 1000

            # Skip sequence if integration time is 0
            if integ_ms == 0:
                self._progress(f"SEQ{seq_num} skipped (integ=0)", 10 + int(seq_num) * 20)
                continue

            # ── Argon Flush ─────────────────────────────────────────────
            if not self.execute_argon_purge(purge_sec):
                self._progress(f"Argon purge failed in SEQ{seq_num}", 0)
                return all_results
            time.sleep(0.2)

            # ── Prespark ────────────────────────────────────────────────
            if not self.execute_prespark(source_name, preburn_ms):
                self._progress(f"Prespark failed in SEQ{seq_num}", 0)
                return all_results
            time.sleep(0.2)

            # ── Integration ─────────────────────────────────────────────
            # Get elements for this sequence
            seq_elements = [e for e in page3_data if str(e.get("seq", "")) == seq_num]
            if seq_elements:
                seq_results = self.execute_integration(integ_ms, seq_elements)
                all_results.update(seq_results)
            time.sleep(0.2)

            # ── Post-integration stop-bit pulse ──────────────────────────
            # After integration completes for this sequence: pulse Port B
            # STOP bit (0x10) HIGH then LOW. Repeated for every sequence.
            if not self.pulse_stop_bit():
                self._progress(f"Post-integration stop-bit pulse failed in SEQ{seq_num}", 0)
                return all_results
            time.sleep(0.2)

        # ── Step 4: Clean ──────────────────────────────────────────────────
        # Value from UI is in seconds, convert to ms
        clean_ms = int(page1_data.get("clean_value", 0)) * 1000
        self.execute_clean(clean_ms)
        time.sleep(0.2)

        # ── Stop bit ON (after Clean, before Shutdown) ──────────────────────
        # Set Port B STOP bit (0x10) HIGH and leave it high (no pulse-low).
        if not self.set_stop_bit_on():
            self._progress("Stop-bit ON failed!", 0)
            return all_results
        time.sleep(0.2)

        # ── Step 5: Shutdown ──────────────────────────────────────────────
        self.execute_shutdown()

        self._progress("Sequence complete!", 100)
        return all_results