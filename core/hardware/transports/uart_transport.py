"""UART command transport for the ATmega spectroscopy controller.

This module owns serial-port details only. MCU command semantics live in
``core.hardware.protocols.uart_protocol`` so another protocol or connection
type can be added without changing the analysis workflow.
"""

from __future__ import annotations

import time
import os
from typing import Optional

from import_data.constants import (
    CH340_PRODUCT_ID,
    CH340_VENDOR_ID,
    DEFAULT_UART_PORT,
    UART_BAUD_RATE,
)

try:
    import serial
    import serial.tools.list_ports
except ImportError:  # pragma: no cover - exercised only in incomplete installs
    serial = None


class UARTTransport:
    """Line-oriented transport backed by a USB-UART serial connection."""

    CH340_VID = CH340_VENDOR_ID
    CH340_PID = CH340_PRODUCT_ID
    DEFAULT_PORT = DEFAULT_UART_PORT

    def __init__(self, baud_rate: int = UART_BAUD_RATE, timeout: float = 2.0):
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.conn = None
        self.is_connected = False
        self._port_name: Optional[str] = None

    def connect(self, endpoint: Optional[str] = None) -> bool:
        """Open the selected serial endpoint and drain startup output."""
        if serial is None:
            raise RuntimeError(
                "pyserial is required for UART hardware access. "
                "Install the project dependencies first."
            )

        if self.is_connected and self.conn and self.conn.is_open:
            print(f"UARTTransport: Already connected to {self._port_name}, reusing.")
            return True

        self.close()
        port = (
            endpoint
            or os.getenv("SPECTRASOFT_UART_PORT")
            or self._find_ch340_port()
            or self.DEFAULT_PORT
        )

        print(f"  Opening {port} at {self.baud_rate} baud...")

        try:
            self.conn = serial.Serial(
                port=port,
                baudrate=self.baud_rate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout,
                dsrdtr=False,
                rtscts=False,
            )
            self.conn.dtr = False
            self.conn.rts = False
            time.sleep(0.5)
            self._drain_startup()
            self.is_connected = True
            self._port_name = port
            print(f"  Connected to {port}")
            return True
        except Exception as exc:
            print(f"  Connection failed: {exc}")
            self.is_connected = False
            self.conn = None
            return False

    def _find_ch340_port(self) -> Optional[str]:
        """Find a CH340 adapter by USB vendor/product identifiers."""
        if serial is None:
            return None

        for port in serial.tools.list_ports.comports():
            if port.vid == self.CH340_VID and port.pid == self.CH340_PID:
                return port.device
        return None

    def _drain_startup(self) -> None:
        """Discard boot messages emitted by the MCU after opening the port."""
        if self.conn is None:
            return

        deadline = time.time() + 1.0
        while time.time() < deadline:
            if self.conn.in_waiting > 0:
                line = self.conn.readline().decode("utf-8", errors="replace").strip()
                if line:
                    print(f"    uC: {line}")
            else:
                time.sleep(0.05)

        self.clear_buffers()

    def write_line(self, command: str) -> bool:
        """Write one newline-terminated command to the transport."""
        if self.conn is None or not self.conn.is_open:
            return False

        self.conn.write((command + "\r\n").encode("utf-8"))
        self.conn.flush()
        return True

    def read_line(self, timeout: float = 1.0) -> Optional[str]:
        """Read one response line, returning ``None`` on timeout."""
        if self.conn is None or not self.conn.is_open:
            return None

        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.conn.in_waiting > 0:
                return self.conn.readline().decode("utf-8", errors="replace").strip()
            time.sleep(0.001)
        return None

    def clear_buffers(self) -> None:
        """Clear pending serial input and output."""
        if self.conn is None:
            return
        self.conn.reset_input_buffer()
        self.conn.reset_output_buffer()

    def close(self) -> None:
        """Close the serial connection if it is open."""
        if self.conn and self.conn.is_open:
            self.conn.close()
        self.is_connected = False
        self.conn = None
        self._port_name = None
