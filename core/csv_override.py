"""
SpectraSoft - CSV Override Loader
===================================
Reads sequence_data.csv and returns pre-stored ADC values for a given
ST Number.  Used in Demo Mode: hardware still executes the full burn
sequence, but the results returned to the GUI are the known-good CSV
values for the selected sample - not live ADC readings.

CSV format (channel-number-based - current format):
    Row 1:  Channel No ->,  (blank),  ABCD,  DEFG,  DEFAULT, DEFAULT, ...
    Row 2:  Element     ->,  (blank),  Seq1,  Seq2,   Seq3,   Seq1, ...
    Row 3+: <channel_no>, <element_name>, <value>, ...

CSV format (legacy element-name-based - also supported for backward compat):
    Row 1:  ST No. ->,  ABCD,  DEFG,  DEFAULT, DEFAULT, DEFAULT, ...
    Row 2:  Sequence ->, , ,   Seq1,   Seq2,    Seq3,   Seq1, ...
    Row 3+: <element>, <value>, ...

The function load_st_values() returns a flat dict:
    { element_display_name: adc_value (int/float), ... }
combining all three sequences for the given ST Number.
"""

import csv
import os
from typing import Dict, Optional, List

# Path relative to the project root (same folder as main.py)
CSV_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "sequence_data.csv")

# Header markers that identify channel-based format.
# The first cell of row 1 in a channel-based CSV starts with one of these
# (comparison is done after stripping and lowercasing).
_CHANNEL_HEADER_MARKERS = (
    "channel no",
    "channel_no",
    "ch no",
    "ch_no",
    "channel no ->",
    "channel_no ->",
    "ch no ->",
    "ch_no ->",
)


def _is_channel_based(header1: List[str]) -> bool:
    """Return True if the CSV uses the new channel-number-based layout."""
    if not header1:
        return False
    first_cell = header1[0].strip().lower()
    # Accept exact match or prefix match (e.g. "channel no -> ...")
    return any(
        first_cell == m or first_cell.startswith(m)
        for m in _CHANNEL_HEADER_MARKERS
    )


def list_st_numbers(csv_path: str = CSV_FILE) -> List[str]:
    """
    Return a list of unique ST Numbers found in the CSV header.
    Ignores empty/blank ST entries (columns used for channel/element labels etc.).
    Works for both channel-based and legacy element-name-based CSV formats.
    """
    if not os.path.isfile(csv_path):
        return []

    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header1 = next(reader, None)   # first header row
            if header1 is None or len(header1) < 2:
                return []

            is_channel = _is_channel_based(header1)

            seen = set()
            result = []
            # In channel-based format, col 0 = "Channel No", col 1 = "Element" labels,
            # data starts at col 2. In legacy format, col 0 = "ST No. ->", data at col 1.
            start_col = 2 if is_channel else 1
            for cell in header1[start_col:]:
                st = cell.strip()
                if st and st not in seen:
                    seen.add(st)
                    result.append(st)
            return result
    except Exception:
        return []


def load_st_values(st_number: str, csv_path: str = CSV_FILE) -> Dict[str, float]:
    """
    Load all ADC values for the given ST Number from sequence_data.csv.

    Supports both CSV formats:
      - Channel-number-based (new): rows keyed by channel number; element name in col 1.
      - Element-name-based (legacy): rows keyed by element name in col 0.

    Returns a flat dict:
        { "element_name": adc_value (float), ... }
    combining all sequences for the given ST Number.

    The returned dict is always keyed by element name so the rest of the
    application continues to work unchanged.

    If the ST Number is not found, returns an empty dict.
    """
    if not os.path.isfile(csv_path):
        print(f"  [csv_override] CSV not found: {csv_path}")
        return {}

    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header1 = next(reader, None)   # ST No / Channel No row
            header2 = next(reader, None)   # Sequence / Element row

            if header1 is None or header2 is None:
                return {}

            is_channel = _is_channel_based(header1)

            # ── Column index resolution ────────────────────────────────────
            if is_channel:
                # col 0 = "Channel No ->" label
                # col 1 = "Element ->" label
                # col 2+ = ST data columns
                data_start_col = 2
            else:
                # Legacy: col 0 = "ST No. ->" label; col 1+ = ST data columns
                data_start_col = 1

            # Find column indices whose ST label matches st_number
            target_cols = []
            for col_idx in range(data_start_col, len(header1)):
                st_cell = (header1[col_idx] or "").strip()
                if st_cell == st_number:
                    target_cols.append(col_idx)

            if not target_cols:
                print(f"  [csv_override] ST '{st_number}' not found in CSV.")
                return {}

            # ── Read data rows ─────────────────────────────────────────────
            results = {}

            if is_channel:
                # Channel-based format:
                #   col 0 = channel_no (integer, primary sort key)
                #   col 1 = element_name
                #   col 2+ = data values

                # Collect all rows into a list sorted by channel number
                rows_by_channel = []
                for row in reader:
                    if not row:
                        continue
                    ch_str = row[0].strip() if row[0].strip() else None
                    if ch_str is None:
                        continue
                    try:
                        ch_no = int(ch_str)
                    except ValueError:
                        continue  # skip non-integer channel rows (e.g., header remnants)

                    ele_name = row[1].strip() if len(row) > 1 else ""
                    rows_by_channel.append((ch_no, ele_name, row))

                # Sort by channel number (guarantees channel-ordered processing)
                rows_by_channel.sort(key=lambda x: x[0])

                for ch_no, ele_name, row in rows_by_channel:
                    if not ele_name:
                        continue
                    for col_idx in target_cols:
                        if col_idx < len(row):
                            cell = row[col_idx].strip()
                            if cell:
                                try:
                                    results[ele_name] = float(cell)
                                    break  # Use first non-empty sequence value
                                except ValueError:
                                    pass

            else:
                # Legacy element-name-based format:
                #   col 0 = element_name
                #   col 1+ = data values
                for row in reader:
                    if not row:
                        continue
                    ele_name = row[0].strip()
                    if not ele_name:
                        continue

                    for col_idx in target_cols:
                        if col_idx < len(row):
                            cell = row[col_idx].strip()
                            if cell:
                                try:
                                    results[ele_name] = float(cell)
                                    break
                                except ValueError:
                                    pass

            print(f"  [csv_override] Loaded {len(results)} elements for ST '{st_number}'"
                  f" ({'channel-based' if is_channel else 'legacy element-based'} format)")
            return results

    except Exception as e:
        print(f"  [csv_override] Error reading CSV: {e}")
        return {}
