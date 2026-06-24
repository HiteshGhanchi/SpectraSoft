"""
SpectraSoft — Hardware Module
==============================
Bridges the database (technique data) with the hardware team's
command_generator.py and uart_handler.py.

Responsibilities:
  1. Auto-detect the spectrometer's COM port on startup
  2. Convert technique data from DB into the format the hardware team expects
  3. Run a full analysis sequence (or simulate one)
  4. Report progress back to the UI via a callback
  5. Return raw ADC readings keyed by element+wavelength

Usage:
    hw = HardwareManager()

    # Check connection
    hw.detect_port()          # returns True/False
    hw.is_connected           # property

    # Run analysis
    results = hw.run_analysis(
        group_data,           # dict from AnalyticalGroup columns
        progress_cb=my_fn     # called with (step_name, percent)
    )
    # results = {"FE|273.0": 2048, "C|193.0": 1024, ...}
"""

import sys
import os
import time
import threading
import random
from typing import Callable, Optional

# ── Try importing pyserial gracefully ─────────────────────────────────────
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False

# =============================================================================
# CONSTANTS (were previously in constants.py)
# =============================================================================

# Simulation mode (set to False to use real hardware)
SIMULATION_MODE = True

# UART settings
UART_BAUDRATE = 9600
UART_TIMEOUT = 1.0
UART_BYTESIZE = serial.EIGHTBITS
UART_PARITY = serial.PARITY_NONE
UART_STOPBITS = serial.STOPBITS_ONE

# ADC read timeout (seconds)
ADC_READ_TIMEOUT = 2.0

# Simulation ADC base value (will be randomized around this)
SIMULATION_ADC_VALUE = 2048

# ── Element channel map: (element, wavelength) → (channel_name, channel_id) ──
ELEMENT_CHANNEL_MAP = {
    ("FE", "273.0"):   ("Fe", 1),
    ("FE", "271.4"):   ("Fe", 1),
    ("C", "193.0"):    ("C", 2),
    ("SI", "212.4"):   ("Si", 3),
    ("MN", "293.3"):   ("Mn", 4),
    ("P", "178.3"):    ("P", 5),
    ("S", "180.7"):    ("S", 6),
    ("CR", "267.7"):   ("Cr", 7),
    ("CR", "298.9"):   ("Cr", 8),
    ("MO", "202.0"):   ("Mo", 9),
    ("MO", "277.5"):   ("Mo", 10),
    ("NI", "231.6"):   ("Ni", 11),
    ("NI", "227.7"):   ("Ni", 12),
    ("AL", "394.4"):   ("Al", 13),
    ("CU", "224.2"):   ("Cu", 14),
    ("TI", "337.2"):   ("Ti", 15),
    ("W", "220.4"):    ("W", 16),
    ("B", "182.6"):    ("B", 17),
    ("NB", "319.5"):   ("Nb", 18),
    ("CA", "396.8"):   ("Ca", 19),
    ("CO", "258.0"):   ("Co", 20),
    ("SN", "189.9"):   ("Sn", 21),
    ("N", "174.5*2"):  ("N", 22),
    ("PB", "405.7"):   ("Pb", 23),
    ("RH", "421.8"):   ("Rh", 24),
    ("CE", ""):        ("Ce", 25),
}

# ── Source mapping (Port B 7-bit values) ──
SOURCE_7BIT_MAP = {
    "1: Normal Spark":   0x0C,
    "2: High Power Spark": 0x14,
    "3: Combined Spark": 0x24,
    "4: Oscillation Spark": 0x44,
    "5: Cleaning Spark": 0x44,
    "0: Lamp":           0x00,
}

# ── Mode and code constants (2-bit mode + 6-bit data) ──
MODE_ELEMENT_SELECT = 0x00
MODE_ATTENUATOR_SET = 0x01
MODE_SENSOR_1       = 0x02
MODE_SENSOR_2       = 0x03

# Sensor 1 (6‑bit) codes
PURGE_CODE_SENSOR1_6BIT     = 0x0A
PREBURN_CODE_SENSOR1_6BIT   = 0x0B
INTEGRATION_CODE_SENSOR1_6BIT = 0x0C
OUTPUT_CODE_SENSOR1_6BIT    = 0x0D
CLEAN_CODE_SENSOR1_6BIT     = 0x0E

# Sensor 2 (6‑bit) codes
PURGE_CODE_SENSOR2_6BIT     = 0x1A
PREBURN_CODE_SENSOR2_6BIT   = 0x1B
INTEGRATION_CODE_SENSOR2_6BIT = 0x1C
OUTPUT_CODE_SENSOR2_6BIT    = 0x1D
CLEAN_CODE_SENSOR2_6BIT     = 0x1E

# Attenuator range
ATTENUATOR_MIN = 0
ATTENUATOR_MAX = 63

# =============================================================================
# Helper — build 8-bit command byte
# =============================================================================

def _make_byte(mode_2bit: int, data_6bit: int) -> int:
    """Pack 2-bit mode and 6-bit data into one byte."""
    return ((mode_2bit & 0b11) << 6) | (data_6bit & 0x3F)


# =============================================================================
# HardwareManager
# =============================================================================

class HardwareManager:
    """
    Single point of contact between the UI and the hardware.
    Thread-safe: run_analysis() spawns a worker thread and
    reports progress via callback so the UI stays responsive.
    """

    # USB description keywords that identify the spectrometer
    # Update these once you know the exact USB descriptor string
    _PORT_KEYWORDS = ["USB", "Serial", "CH340", "CP210", "FTDI", "Arduino"]

    def __init__(self):
        self._port: Optional[str] = None
        self._conn  = None          # serial.Serial instance when open
        self._lock  = threading.Lock()
        self.is_connected = False
        self._last_error  = ""

    # ------------------------------------------------------------------
    # Port detection
    # ------------------------------------------------------------------

    def detect_port(self) -> bool:
        """
        Scan available COM ports and connect to the first one that looks
        like a spectrometer.  Falls back to the first available port if
        no keyword match is found.

        Returns True if a port was found and opened, False otherwise.
        """
        if SIMULATION_MODE or not SERIAL_AVAILABLE:
            self.is_connected = False
            return False

        try:
            ports = list(serial.tools.list_ports.comports())
        except Exception as e:
            self._last_error = str(e)
            self.is_connected = False
            return False

        if not ports:
            self.is_connected = False
            return False

        # Prefer ports whose description matches known USB-serial chips
        chosen = None
        for p in ports:
            desc = (p.description or "") + (p.manufacturer or "")
            if any(kw.lower() in desc.lower() for kw in self._PORT_KEYWORDS):
                chosen = p.device
                break

        # Fall back to first available port
        if chosen is None:
            chosen = ports[0].device

        return self._open_port(chosen)

    def _open_port(self, port: str) -> bool:
        """Open a specific COM port."""
        self._close()
        try:
            self._conn = serial.Serial(
                port=port,
                baudrate=UART_BAUDRATE,
                timeout=UART_TIMEOUT,
                bytesize=UART_BYTESIZE,
                parity=UART_PARITY,
                stopbits=UART_STOPBITS,
            )
            time.sleep(0.1)
            self._port = port
            self.is_connected = True
            return True
        except Exception as e:
            self._last_error = str(e)
            self.is_connected = False
            return False

    def _close(self):
        if self._conn and self._conn.is_open:
            try:
                self._conn.close()
            except Exception:
                pass
        self._conn = None
        self.is_connected = False

    def disconnect(self):
        """Explicitly disconnect. Called on app exit."""
        self._close()

    @property
    def port_name(self) -> str:
        return self._port or "Not connected"

    @property
    def last_error(self) -> str:
        return self._last_error

    # ------------------------------------------------------------------
    # Run analysis
    # ------------------------------------------------------------------

    def run_analysis(
        self,
        group_data: dict,
        progress_cb: Optional[Callable[[str, int], None]] = None,
    ) -> dict:
        """
        Run a complete analysis sequence synchronously.

        group_data: dict with keys:
            page_01_condition  — from AnalyticalGroup.page_01_condition
            page_02_attenuator — from AnalyticalGroup.page_02_attenuator
            page_04_channel    — from AnalyticalGroup.page_04_channel

        progress_cb: callable(step_name: str, percent: int)
            Called at each step so the UI can update a progress bar.

        Returns:
            dict  { "ELEMENT|WAVELENGTH": adc_value, ... }
            e.g.  { "FE|273.0": 2048, "C|193.0": 1350, ... }

        Raises:
            HardwareError if not connected and not in simulation mode.
        """
        if not SIMULATION_MODE and not self.is_connected:
            raise HardwareError("Hardware not connected.")

        def _cb(msg, pct):
            if progress_cb:
                progress_cb(msg, pct)

        _cb("Building command sequence…", 5)
        commands, read_points = self._build_commands(group_data)

        _cb("Starting analysis…", 10)

        if SIMULATION_MODE:
            return self._simulate(commands, read_points, _cb)
        else:
            return self._execute(commands, read_points, _cb)

    # ------------------------------------------------------------------
    # Command building (converts DB data → command list)
    # ------------------------------------------------------------------

    def _build_commands(self, gd: dict):
        """
        Convert technique data from the database into the command list
        format used by uart_handler.

        gd keys: page_01_condition, page_02_attenuator, page_04_channel
        """
        commands    = []
        read_points = []

        p1  = gd.get("page_01_condition",  {})
        p2  = gd.get("page_02_attenuator", {})
        p4  = gd.get("page_04_channel",    {})

        att_rows  = (p2 or {}).get("rows",     [])
        chan_rows  = (p4 or {}).get("rows",     [])

        # ── Step 1: Select each element and set attenuator ─────────────
        for row in att_rows:
            ele = row.get("element", "").upper()
            wl  = row.get("wavelength", "")
            att = int(row.get("att_value", 0))

            if not ele:
                continue

            ch_info = ELEMENT_CHANNEL_MAP.get((ele, wl))
            if ch_info is None:
                # Unknown channel — skip silently (placeholder constants)
                commands.append(f"# SKIP (no channel): {ele} {wl}")
                continue

            _, ch_id = ch_info
            att_clamped = max(ATTENUATOR_MIN, min(ATTENUATOR_MAX, att))

            # Select element (mode 00)
            commands.append(
                f"O,A,{_make_byte(MODE_ELEMENT_SELECT, ch_id)}"
                f"  # Select {ele} {wl}"
            )
            # Set attenuator (mode 01)
            commands.append(
                f"O,A,{_make_byte(MODE_ATTENUATOR_SET, att_clamped)}"
                f"  # ATT={att_clamped}"
            )

        # ── Step 2: Purge ──────────────────────────────────────────────
        purge_sec = int(p1.get("purge_seq1", 3))
        commands.append(
            f"O,A,{_make_byte(MODE_SENSOR_1, PURGE_CODE_SENSOR1_6BIT)}"
            "  # Purge sensor1"
        )
        commands.append(
            f"O,A,{_make_byte(MODE_SENSOR_2, PURGE_CODE_SENSOR2_6BIT)}"
            "  # Purge sensor2"
        )
        commands.append(f"T,{purge_sec * 1000}  # Purge {purge_sec}s")

        # ── Step 3: Sequences 1, 2, 3 ─────────────────────────────────
        seq_keys = {"1": "seq1", "2": "seq2", "3": "seq3"}

        for seq_num, seq_key in seq_keys.items():
            source_name = p1.get(f"source_{seq_key}", "")
            preburn_ms  = int(p1.get(f"preburn_{seq_key}", 0) or 0)
            integ_ms    = int(p1.get(f"integ_{seq_key}",   0) or 0)

            if integ_ms == 0:
                continue  # Skip unused sequences

            # Source select (Port B)
            src_7bit = SOURCE_7BIT_MAP.get(source_name)
            if src_7bit is not None:
                commands.append(
                    f"O,B,{src_7bit & 0x7F}  # SEQ{seq_num} source={source_name}"
                )

            # Pre-burn
            if preburn_ms > 0:
                commands.append(
                    f"O,A,{_make_byte(MODE_SENSOR_1, PREBURN_CODE_SENSOR1_6BIT)}"
                    f"  # SEQ{seq_num} preburn s1"
                )
                commands.append(
                    f"O,A,{_make_byte(MODE_SENSOR_2, PREBURN_CODE_SENSOR2_6BIT)}"
                    f"  # SEQ{seq_num} preburn s2"
                )
                commands.append(f"T,{preburn_ms}  # Preburn {preburn_ms}ms")

            # Integration
            commands.append(
                f"O,A,{_make_byte(MODE_SENSOR_1, INTEGRATION_CODE_SENSOR1_6BIT)}"
                f"  # SEQ{seq_num} integ s1"
            )
            commands.append(
                f"O,A,{_make_byte(MODE_SENSOR_2, INTEGRATION_CODE_SENSOR2_6BIT)}"
                f"  # SEQ{seq_num} integ s2"
            )
            commands.append(f"T,{integ_ms}  # Integ {integ_ms}ms")

            # Output codes
            commands.append(
                f"O,A,{_make_byte(MODE_SENSOR_1, OUTPUT_CODE_SENSOR1_6BIT)}"
                "  # Output s1"
            )
            commands.append(
                f"O,A,{_make_byte(MODE_SENSOR_2, OUTPUT_CODE_SENSOR2_6BIT)}"
                "  # Output s2"
            )

            # Read elements belonging to this sequence
            for row in chan_rows:
                if str(row.get("seq", "")) != seq_num:
                    continue
                ele = row.get("ele_name", "").upper()
                wl  = row.get("w_length", "")
                if not ele:
                    continue

                ch_info = ELEMENT_CHANNEL_MAP.get((ele, wl))
                if ch_info is None:
                    commands.append(f"# SKIP read (no channel): {ele} {wl}")
                    continue

                _, ch_id = ch_info
                commands.append(
                    f"O,A,{_make_byte(MODE_ELEMENT_SELECT, ch_id)}"
                    f"  # Select {ele} {wl} for read"
                )
                read_points.append({
                    "command_index": len(commands),
                    "element":   ele,
                    "wavelength": wl,
                    "sequence":  seq_num,
                })
                commands.append(f"I  # Read {ele} {wl} SEQ{seq_num}")

        # ── Step 4: Cleaning ───────────────────────────────────────────
        clean_val = int(p1.get("clean_value", 0) or 0)
        commands.append(
            f"O,A,{_make_byte(MODE_SENSOR_1, CLEAN_CODE_SENSOR1_6BIT)}"
            "  # Clean s1"
        )
        commands.append(
            f"O,A,{_make_byte(MODE_SENSOR_2, CLEAN_CODE_SENSOR2_6BIT)}"
            "  # Clean s2"
        )
        if clean_val > 0:
            commands.append(f"T,{clean_val * 1000}  # Clean {clean_val}s")

        return commands, read_points

    # ------------------------------------------------------------------
    # Simulation mode
    # ------------------------------------------------------------------

    def _simulate(self, commands, read_points, cb) -> dict:
        """
        Walk through the command list, sleeping for real delays,
        and returning fake ADC values for each read point.
        """
        total = len(commands)
        results = {}

        read_map = {rp["command_index"]: rp for rp in read_points}

        for idx, cmd in enumerate(commands):
            pct = 10 + int((idx / max(total, 1)) * 85)
            clean = cmd.split("#")[0].strip()

            if clean.startswith("T,"):
                ms = int(clean.split(",")[1])
                cb(f"Waiting {ms}ms…", pct)
                time.sleep(ms / 1000.0)

            elif clean.startswith("I"):
                rp = read_map.get(idx)
                if rp:
                    cb(f"Reading {rp['element']} {rp['wavelength']}…", pct)
                    # Simulate a realistic ADC value with small noise
                    adc = SIMULATION_ADC_VALUE + random.randint(-200, 200)
                    adc = max(0, min(4095, adc))
                    key = f"{rp['element']}|{rp['wavelength']}"
                    results[key] = adc
                    time.sleep(0.02)  # small sim delay

            else:
                cb(f"Sending command…", pct)
                time.sleep(0.005)

        cb("Analysis complete.", 100)
        return results

    # ------------------------------------------------------------------
    # Real hardware execution
    # ------------------------------------------------------------------

    def _execute(self, commands, read_points, cb) -> dict:
        """
        Send commands over serial and collect real ADC responses.
        Uses the same logic as the hardware team's uart_handler.py
        but integrated here so we can report progress to the UI.
        """
        results  = {}
        total    = len(commands)
        read_map = {rp["command_index"]: rp for rp in read_points}

        with self._lock:
            for idx, cmd in enumerate(commands):
                pct   = 10 + int((idx / max(total, 1)) * 85)
                clean = cmd.split("#")[0].strip()

                if not clean:
                    continue

                try:
                    if clean.startswith("O,"):
                        # Output command
                        parts = clean.split(",")
                        port  = parts[1].strip()
                        val   = int(parts[2].strip())
                        if port == "B":
                            val = val & 0x7F
                        cb(f"OUT Port{port}={val}", pct)
                        self._conn.write((clean + "\n").encode())

                    elif clean.startswith("T,"):
                        # Delay
                        ms = int(clean.split(",")[1].strip())
                        cb(f"Waiting {ms}ms…", pct)
                        time.sleep(ms / 1000.0)

                    elif clean.startswith("I"):
                        # Read
                        rp = read_map.get(idx)
                        if rp:
                            cb(
                                f"Reading {rp['element']} "
                                f"{rp['wavelength']}…",
                                pct,
                            )
                        self._conn.write(b"I\n")

                        # Wait for D,value response
                        adc = self._read_adc()
                        if adc is not None and rp:
                            key = f"{rp['element']}|{rp['wavelength']}"
                            results[key] = adc

                except Exception as e:
                    self._last_error = str(e)
                    raise HardwareError(f"Command failed at idx {idx}: {e}")

                time.sleep(0.01)  # inter-command gap

        cb("Analysis complete.", 100)
        return results

    def _read_adc(self) -> Optional[int]:
        """Read one D,value response from serial with timeout."""
        deadline = time.time() + ADC_READ_TIMEOUT
        while time.time() < deadline:
            if self._conn.in_waiting:
                line = self._conn.readline().decode("utf-8", errors="ignore").strip()
                if line.startswith("D,"):
                    try:
                        return int(line.split(",")[1])
                    except (IndexError, ValueError):
                        pass
            time.sleep(0.005)
        return None


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------

class HardwareError(Exception):
    """Raised when hardware communication fails."""
    pass


# ---------------------------------------------------------------------------
# Module-level singleton — import and use this everywhere
# ---------------------------------------------------------------------------

hw = HardwareManager()