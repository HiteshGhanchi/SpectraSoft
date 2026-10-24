"""ATmega UART protocol implementation for the spectroscopy controller.

The command values in this module are derived from
``atmega2560pro_virtual_ports.ino``. Keeping them here means the rest of the
application depends on semantic instrument operations instead of raw UART
strings.
"""

from __future__ import annotations

import time
from typing import Dict, List, Optional

from import_data.constants import (
    ADC_INTER_DELAY_SECONDS,
    ADC_SETTLE_DELAY_SECONDS,
    ATTENUATOR_COMMAND_OFFSET,
    ATTENUATOR_ELEMENT_DELAY_SECONDS,
    ATTENUATOR_MAX_VALUE,
    ATTENUATOR_MIN_VALUE,
    ELEMENT_CHANNEL_COUNT,
    ELEMENT_SELECT_DELAY_SECONDS,
    RESET_HOLD_SECONDS,
    SOURCE_CODE_MAX,
    SOURCE_CODE_MIN,
    SOURCE_PORT_CONTROL_BITS,
)
from core.hardware.interfaces.spectrometer import SpectrometerController
from core.hardware.interfaces.transport import CommandTransport
from core.hardware.transports.uart_transport import UARTTransport


class UARTSpectrometerController(SpectrometerController):
    """Spectrometer controller that speaks the ATmega line protocol."""

    def __init__(self, transport: Optional[CommandTransport] = None):
        self.transport = transport or UARTTransport()

    def connect(self) -> bool:
        """Open the transport and place the controller in standby."""
        if not self.transport.connect():
            return False

        # Standby sequence from the existing application flow. These are
        # protocol commands, not transport concerns, so they live here.
        return all(
            self._send_command(command)
            for command in ("O,A,C2", "O,A,9E", "O,A,00", "O,B,16")
        )

    def reset(self) -> bool:
        if not self._send_command("O,A,9E"):
            return False
        if not self._delay_ms(RESET_HOLD_SECONDS * 1000):
            return False
        if not self._send_command("O,A,C3"):
            return False
        return self._delay_ms(RESET_HOLD_SECONDS * 1000)

    def argon_purge(self, purge_sec: float) -> bool:
        if not self._send_command("O,A,CB"):
            return False
        return self._delay_ms(purge_sec * 1000)

    def prespark(self, source_code: int, preburn_ms: int) -> bool:
        if not self._send_command("O,A,C9"):
            return False

        if not SOURCE_CODE_MIN <= int(source_code) <= SOURCE_CODE_MAX:
            return False

        port_b_value = (int(source_code) << 3) | SOURCE_PORT_CONTROL_BITS
        if not self._send_command(f"O,B,{port_b_value:02X}"):
            return False

        return self._delay_ms(preburn_ms)

    def integrate(self, integ_ms: int, elements: List[Dict]) -> Dict[str, int]:
        results: Dict[str, int] = {}

        if not self._send_command("O,A,8C"):
            return results
        if not self._delay_ms(integ_ms):
            return results

        if not self._send_command("O,B,16"):
            return results

        for element in elements:
            try:
                itg_no = int(element.get("itg", 0))
            except (TypeError, ValueError):
                continue

            name = element.get("ele", f"ele{itg_no}")
            element_hex = f"{itg_no - 1:02X}"

            if not self._send_command(f"O,A,{element_hex}"):
                continue
            if not self._delay_ms(ELEMENT_SELECT_DELAY_SECONDS * 1000):
                continue

            if not self._send_command("O,A,C9"):
                continue
            if not self._delay_ms(ADC_INTER_DELAY_SECONDS * 1000):
                continue

            if not self._send_command("O,A,CD"):
                continue
            if not self._delay_ms(ADC_INTER_DELAY_SECONDS * 1000):
                continue

            if not self._send_command("O,A,C9"):
                continue
            if not self._delay_ms(ADC_SETTLE_DELAY_SECONDS * 1000):
                continue

            if not self.transport.write_line("I"):
                continue

            value = self._read_adc_value()
            if value is not None:
                results[name] = value

        return results

    def clean(self, clean_ms: int) -> bool:
        if not self._send_command("O,A,9C"):
            return False
        return self._delay_ms(clean_ms)

    def shutdown(self) -> bool:
        return self._send_command("O,A,C2") and self._send_command("O,A,00")

    def set_attenuator(self, itg_no: int, att_value: int) -> bool:
        """Select one ITG channel and write its 0–63 attenuator value."""
        if not 1 <= int(itg_no) <= ELEMENT_CHANNEL_COUNT:
            return False
        if not ATTENUATOR_MIN_VALUE <= int(att_value) <= ATTENUATOR_MAX_VALUE:
            return False

        element_command = f"O,A,{int(itg_no) - 1:02X}"
        attenuator_command = f"O,A,{int(att_value) + ATTENUATOR_COMMAND_OFFSET:02X}"

        if not self._send_command(element_command):
            return False
        if not self._delay_ms(ATTENUATOR_ELEMENT_DELAY_SECONDS * 1000):
            return False

        # The controller has historically sent the ATT command twice for
        # reliability; preserve that behavior in the UART implementation.
        return self._send_command(attenuator_command) and self._send_command(
            attenuator_command
        )

    def close(self) -> None:
        self.transport.close()

    def _delay_ms(self, milliseconds: float) -> bool:
        """Use the MCU's non-blocking ``T,<ms>`` command for timing."""
        return self._send_command(f"T,{max(0, int(milliseconds))}")

    def _send_command(self, command: str, timeout: float = 1.0) -> bool:
        if not self.transport.write_line(command):
            return False

        deadline = time.time() + timeout
        while time.time() < deadline:
            remaining = max(0.001, deadline - time.time())
            line = self.transport.read_line(timeout=remaining)
            if line is None:
                return False
            if line.startswith("#"):
                continue
            return line == "K"
        return False

    def _read_adc_value(self, timeout: float = 5.0) -> Optional[int]:
        deadline = time.time() + timeout
        while time.time() < deadline:
            remaining = max(0.001, deadline - time.time())
            line = self.transport.read_line(timeout=remaining)
            if line is None:
                return None
            if line.startswith("#") or line == "K":
                continue
            if not line.startswith("D,"):
                return None
            try:
                return int(line.split(",", 1)[1].strip())
            except (IndexError, ValueError):
                return None
        return None
