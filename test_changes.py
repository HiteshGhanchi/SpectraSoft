"""
SpectraSoft - Targeted Change Verification Tests
================================================
Tests the three specific changes requested:
  1. Display form/frame resizability (logic-level check)
  2. CSV data storage organized by channel number
  3. HV setting hex address system for channels 10-15

Run from the SpectraSoft/ folder:
    python test_changes.py

Hardware-dependent tests are clearly identified and SKIPPED automatically
when hardware is not connected.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


PASS = 0
FAIL = 0


def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        print(f"  [PASS] {name}" + (f" - {detail}" if detail else ""))
        PASS += 1
    else:
        print(f"  [FAIL] {name}" + (f" - {detail}" if detail else ""))
        FAIL += 1


def check_skip(name, detail=""):
    """Mark a test as hardware-dependent (skipped in simulation)."""
    print(f"  [SKIP] {name} (hardware required)" + (f" - {detail}" if detail else ""))


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 1: Display Form Resizability
# ═══════════════════════════════════════════════════════════════════════════════

def test_display_resizability():
    print("\n[TEST 1] Display form / frame resizability")

    # Read main_window.py and verify setFixedSize is removed
    mw_path = os.path.join(os.path.dirname(__file__), "ui", "main_window.py")
    with open(mw_path, "r", encoding="utf-8") as f:
        src = f.read()

    # Check that setFixedSize is NOT used (it prevented resizing)
    check(
        "setFixedSize removed from MainWindow",
        "setFixedSize" not in src,
        "setFixedSize was replaced with setMinimumSize + resize"
    )

    # Check that setMinimumSize is used instead (allows expansion)
    check(
        "setMinimumSize present in MainWindow",
        "setMinimumSize" in src
    )

    # Check that resize() is called to set initial size
    check(
        "resize() call present to set initial dimensions",
        "self.resize(1100, 680)" in src
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 2: CSV Data Storage - Channel-Number Organization
# ═══════════════════════════════════════════════════════════════════════════════

def test_csv_channel_organization():
    print("\n[TEST 2] CSV data storage - channel-number organization")

    from core.csv_override import list_st_numbers, load_st_values, _is_channel_based
    import csv as csv_module

    csv_path = os.path.join(os.path.dirname(__file__), "sequence_data.csv")
    check("sequence_data.csv exists", os.path.isfile(csv_path))

    # ── Verify new CSV format ────────────────────────────────────────────────
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv_module.reader(f)
        header1 = next(reader, [])
        header2 = next(reader, [])
        data_rows = list(reader)

    check(
        "Header row 0 identifies channel-based format",
        _is_channel_based(header1),
        f"First cell: '{header1[0] if header1 else '(empty)'}'"
    )

    # Check rows are keyed by integer channel numbers
    channel_numbers = []
    for row in data_rows:
        if not row or not row[0].strip():
            continue
        try:
            ch = int(row[0].strip())
            channel_numbers.append(ch)
        except ValueError:
            pass

    check(
        "Data rows use integer channel numbers (col 0)",
        len(channel_numbers) > 0,
        f"{len(channel_numbers)} rows with channel numbers found"
    )

    # Check rows are sorted in ascending channel order
    check(
        "Channel numbers are in ascending order",
        channel_numbers == sorted(channel_numbers),
        f"First 5 channels: {channel_numbers[:5]}"
    )

    # ── Channels 10-15 are present ───────────────────────────────────────────
    for ch in range(10, 16):
        check(
            f"Channel {ch} is present in CSV",
            ch in channel_numbers
        )

    # ── Element names are in column 1 ─────────────────────────────────────────
    ele_names_col1 = []
    for row in data_rows:
        if row and row[0].strip():
            try:
                int(row[0].strip())
                if len(row) > 1:
                    ele_names_col1.append(row[1].strip())
            except ValueError:
                pass

    check(
        "Element names are stored in column 1 (not column 0)",
        len(ele_names_col1) > 0,
        f"First 5: {ele_names_col1[:5]}"
    )

    # ── list_st_numbers works with new format ──────────────────────────────────
    st_numbers = list_st_numbers(csv_path)
    check(
        "list_st_numbers() returns ST numbers from channel-based CSV",
        len(st_numbers) > 0,
        f"ST numbers: {st_numbers[:4]}"
    )

    # ── load_st_values returns element-keyed dict from channel-based CSV ───────
    if st_numbers:
        st = st_numbers[0]
        values = load_st_values(st, csv_path)
        check(
            f"load_st_values('{st}') returns non-empty dict",
            len(values) > 0,
            f"{len(values)} elements loaded"
        )
        # Keys should be element names (strings), not channel numbers
        all_str_keys = all(isinstance(k, str) for k in values.keys())
        check(
            "load_st_values() keys are element names (str)",
            all_str_keys,
            f"Sample keys: {list(values.keys())[:3]}"
        )

    # ── Backward compat: legacy format still works ─────────────────────────────
    from core.csv_override import _is_channel_based as _icb
    fake_legacy_header = ["ST No. ->", "ABCD", "DEFG"]
    check(
        "_is_channel_based() returns False for legacy header",
        not _icb(fake_legacy_header)
    )

    # ── Export format check ────────────────────────────────────────────────────
    job5_path = os.path.join(os.path.dirname(__file__), "ui", "analysis", "analysis_run_job5.py")
    with open(job5_path, "r", encoding="utf-8") as f:
        job5_src = f.read()

    check(
        "Export CSV writes 'Channel No' as first header column",
        '"Channel No"' in job5_src or "'Channel No'" in job5_src
    )
    check(
        "Export CSV writes 'Element' as second header column",
        '"Element"' in job5_src or "'Element'" in job5_src
    )
    check(
        "Export CSV iterates element_names (not table rows) for channel order",
        "enumerate(self.element_names)" in job5_src
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TEST 3: HV Setting - Hex Address System + Channel Range 10-15
# ═══════════════════════════════════════════════════════════════════════════════

def test_hv_hex_addressing():
    print("\n[TEST 3] HV setting - hex address system + channels 10–15")

    from core.hv_controller import HVController, MIN_CHANNEL, MAX_CHANNEL

    # ── channel_to_hex_address mapping ──────────────────────────────────────
    expected = {
        1:  "00",
        2:  "01",
        9:  "08",
        10: "09",
        11: "0A",
        12: "0B",
        13: "0C",
        14: "0D",
        15: "0E",
        16: "0F",
    }

    for ch, expected_hex in expected.items():
        result = HVController.channel_to_hex_address(ch)
        check(
            f"Channel {ch:2d} -> hex address {expected_hex}",
            result == expected_hex,
            f"got '{result}'"
        )

    # ── A–F are NOT rejected as invalid ─────────────────────────────────────
    for ch in range(10, 16):
        addr = HVController.channel_to_hex_address(ch)
        # The address for ch=11 is "0A" - must not be rejected
        is_valid_hex = True
        try:
            int(addr, 16)   # parse as hex
        except ValueError:
            is_valid_hex = False
        check(
            f"Channel {ch} address '{addr}' is a valid hex string (A–F not rejected)",
            is_valid_hex
        )

    # ── validate_channel ────────────────────────────────────────────────────
    check("Channel 1 is valid",  HVController.validate_channel(1))
    check("Channel 15 is valid", HVController.validate_channel(15))
    check("Channel 0 is invalid", not HVController.validate_channel(0))
    check("Channel -1 is invalid", not HVController.validate_channel(-1))
    check(
        f"Channel {MAX_CHANNEL + 1} is invalid (beyond MAX)",
        not HVController.validate_channel(MAX_CHANNEL + 1)
    )

    # ── ValueError for out-of-range channels ─────────────────────────────────
    raised_for_zero = False
    try:
        HVController.channel_to_hex_address(0)
    except ValueError:
        raised_for_zero = True
    check("channel_to_hex_address(0) raises ValueError", raised_for_zero)

    raised_for_neg = False
    try:
        HVController.channel_to_hex_address(-1)
    except ValueError:
        raised_for_neg = True
    check("channel_to_hex_address(-1) raises ValueError", raised_for_neg)

    # ── Sequence engine hex format ──────────────────────────────────────────
    # Verify the format string in sequence_engine.py is {:02X}
    se_path = os.path.join(os.path.dirname(__file__), "core", "sequence_engine.py")
    with open(se_path, "r", encoding="utf-8") as f:
        se_src = f.read()
    check(
        "sequence_engine.py uses {:02X} (uppercase hex) for element address",
        ":02X}" in se_src
    )

    # ── Attenuator programmer hex format ────────────────────────────────────
    ap_path = os.path.join(os.path.dirname(__file__), "core", "attenuator_programmer.py")
    with open(ap_path, "r", encoding="utf-8") as f:
        ap_src = f.read()
    check(
        "attenuator_programmer.py uses {:02X} (uppercase hex) for element address",
        ":02X}" in ap_src
    )

    # ── MainWindow toggle_hv no longer has the TODO stub ────────────────────
    mw_path = os.path.join(os.path.dirname(__file__), "ui", "main_window.py")
    with open(mw_path, "r", encoding="utf-8") as f:
        mw_src = f.read()
    check(
        "MainWindow.toggle_hv() no longer has bare TODO stub",
        "# TODO: Send command to MCU" not in mw_src
    )
    check(
        "MainWindow.toggle_hv() references HVController",
        "HVController" in mw_src
    )

    # ── Hardware-dependent tests ─────────────────────────────────────────────
    print()
    check_skip(
        "set_hv_on(10, value) sends 'O,A,09'",
        "Requires CH340 USB-UART adapter + MCU"
    )
    check_skip(
        "set_hv_on(11, value) sends 'O,A,0A'",
        "Requires CH340 USB-UART adapter + MCU"
    )
    check_skip(
        "set_hv_on(15, value) sends 'O,A,0E'",
        "Requires CH340 USB-UART adapter + MCU"
    )
    check_skip(
        "set_hv_off() sends 'O,A,00'",
        "Requires CH340 USB-UART adapter + MCU"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("  SpectraSoft - Targeted Change Verification Tests")
    print("=" * 65)

    test_display_resizability()
    test_csv_channel_organization()
    test_hv_hex_addressing()

    print("\n" + "=" * 65)
    print(f"  Results: {PASS} passed, {FAIL} failed")
    print("=" * 65)

    if FAIL == 0:
        print("  All verifiable tests PASSED.")
        print("  Hardware-dependent tests (SKIP) require physical device.\n")
    else:
        print("  Some tests FAILED - review output above.\n")

    sys.exit(0 if FAIL == 0 else 1)
