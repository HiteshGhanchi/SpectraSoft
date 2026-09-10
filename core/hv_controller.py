"""
SpectraSoft — HV (High Voltage) Controller
============================================
Handles setting High Voltage (HV) per channel using the hex address system.

Protocol
--------
The device expects UART commands of the form:

    O,A,<hex_addr>      — Select channel / set address
    O,A,<hex_value>     — Set the HV value for that channel

Channel → Hex Address Mapping (0-based offset from base address)
-----------------------------------------------------------------
Channel 1  (decimal 1)  → 0x00 (hex 00)
Channel 2  (decimal 2)  → 0x01 (hex 01)
...
Channel 9  (decimal 9)  → 0x08 (hex 08)
Channel 10 (decimal 10) → 0x09 (hex 09)
Channel 11 (decimal 11) → 0x0A (hex 0A)   ← must NOT be treated as decimal
Channel 12 (decimal 12) → 0x0B (hex 0B)
Channel 13 (decimal 13) → 0x0C (hex 0C)
Channel 14 (decimal 14) → 0x0D (hex 0D)
Channel 15 (decimal 15) → 0x0E (hex 0E)
Channel 16 (decimal 16) → 0x0F (hex 0F)
...

The key fix: channel numbers 10–15 map to hex digits A–F.
Using Python's built-in {:02X} format string handles this correctly for ALL
channel values; there is no need to treat A–F as invalid.

IMPORTANT: Never use str.isdigit() or int() with base 10 to validate hex
addresses — hex characters A–F are valid and must not be rejected.
"""

import time
from typing import Optional
from core.uart_manager import UARTManager


# ── Protocol constants ────────────────────────────────────────────────────────
# These must match the MCU firmware's expected command bytes.

HV_CHANNEL_BASE = 0x00     # Address offset for channel 1 (channel_no - 1 = addr)
MAX_CHANNEL     = 64       # Maximum supported hardware channel number (1-based)
MIN_CHANNEL     = 1        # Minimum supported hardware channel number (1-based)

HV_CMD_DELAY    = 0.050    # 50 ms between HV commands


class HVController:
    """
    Controls the High Voltage (HV) setting per channel over UART.

    Channel numbering is 1-based (1 = first channel).
    Internally, address = channel_number - 1, formatted as uppercase 2-digit hex.

    Examples:
        channel 1  → address 0x00 → command "O,A,00"
        channel 9  → address 0x08 → command "O,A,08"
        channel 10 → address 0x09 → command "O,A,09"
        channel 11 → address 0x0A → command "O,A,0A"   ← A is valid hex, NOT decimal
        channel 15 → address 0x0E → command "O,A,0E"
        channel 16 → address 0x0F → command "O,A,0F"
    """

    def __init__(self, uart: UARTManager):
        self.uart = uart

    # ── Public helpers ──────────────────────────────────────────────────────

    @staticmethod
    def channel_to_hex_address(channel_no: int) -> str:
        """
        Convert a 1-based channel number to its 2-digit uppercase hex address string.

        Args:
            channel_no: 1-based channel number (1–MAX_CHANNEL).

        Returns:
            Two-character uppercase hex string, e.g. "00", "09", "0A", "0F".

        Raises:
            ValueError: If channel_no is out of the valid range.
        """
        if not (MIN_CHANNEL <= channel_no <= MAX_CHANNEL):
            raise ValueError(
                f"Channel number {channel_no} is out of range "
                f"[{MIN_CHANNEL}, {MAX_CHANNEL}]."
            )
        addr = channel_no - 1          # 0-based address
        return f"{addr:02X}"           # uppercase hex, always 2 digits; A–F are valid

    @staticmethod
    def validate_channel(channel_no: int) -> bool:
        """Return True if channel_no is within the valid hardware range."""
        return MIN_CHANNEL <= channel_no <= MAX_CHANNEL

    def set_hv_on(self, channel_no: int, hv_value: int) -> bool:
        """
        Send HV ON command for the given channel.

        The protocol selects the channel by address, then sends the HV value.
        Channels 10–15 are addressed as 09–0E (hex) — NOT as decimal 09–15.

        Args:
            channel_no: 1-based channel number (1–MAX_CHANNEL).
            hv_value:   HV value to set (device-specific range, 0–255 typical).

        Returns:
            True if both UART commands were acknowledged.

        Raises:
            ValueError: If channel_no is invalid.
        """
        hex_addr  = self.channel_to_hex_address(channel_no)
        hex_value = f"{int(hv_value) & 0xFF:02X}"

        print(
            f"  [HVController] Set HV for channel {channel_no} "
            f"(addr=0x{hex_addr}): value=0x{hex_value}"
        )

        # Step 1: Select the channel by address
        if not self.uart.send_command(f"O,A,{hex_addr}", wait_ack=True):
            print(f"  [HVController] Channel select failed for channel {channel_no}")
            return False
        time.sleep(HV_CMD_DELAY)

        # Step 2: Send the HV value
        if not self.uart.send_command(f"O,A,{hex_value}", wait_ack=True):
            print(f"  [HVController] HV value send failed for channel {channel_no}")
            return False

        return True

    def set_hv_off(self) -> bool:
        """
        Send HV OFF command (zero-out Port A).

        Returns:
            True if the UART command was acknowledged.
        """
        print("  [HVController] HV OFF")
        return self.uart.send_command("O,A,00", wait_ack=True)

    def set_hv_for_all_channels(
        self,
        channel_hv_map: dict,
        progress_cb=None
    ) -> int:
        """
        Set HV values for a dict of {channel_no: hv_value} entries.

        Channels are processed in ascending numerical order (1, 2, … 10, 11 … 15 …).
        This ensures the hex-addressed channels 10–15 (A–F) are handled correctly.

        Args:
            channel_hv_map: Dict mapping int channel_no → int hv_value.
            progress_cb:    Optional callable(message: str, percent: int).

        Returns:
            Number of channels successfully programmed.
        """
        success_count = 0
        channel_nos   = sorted(channel_hv_map.keys())   # ascending numeric order
        total         = len(channel_nos)

        for i, ch_no in enumerate(channel_nos):
            hv_val = channel_hv_map[ch_no]

            if progress_cb:
                pct = int((i / total) * 100) if total else 0
                progress_cb(
                    f"Setting HV for channel {ch_no} "
                    f"(addr={self.channel_to_hex_address(ch_no)})...",
                    pct
                )

            try:
                if self.set_hv_on(ch_no, hv_val):
                    success_count += 1
            except ValueError as e:
                print(f"  [HVController] Skipping invalid channel: {e}")

        if progress_cb:
            progress_cb("HV programming complete.", 100)

        return success_count
