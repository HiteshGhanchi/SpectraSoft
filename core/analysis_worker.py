"""
SpectraSoft — Analysis Worker (Job 5 Only)
============================================

Runs ONLY Job 5: INT.1 (Raw Intensity) in a background thread.

This is the "sanity check" job used to verify:
- Hardware connection is working
- Spark sequence is executed
- ATT values are programmed
- ADC/intensity values are displayed

Important development mode:
- The MCU is still connected.
- Real UART commands are still sent.
- Real MCU sequence still runs.
- If SIMULATION_FROM_CSV = True, the final ADC/intensity data displayed
  in Job 5 is taken from CSV instead of the MCU ADC result.

This is useful when the MCU is connected but the main spectrometer machine
is not connected yet, causing MCU ADC readings to be 0.
"""

from PyQt6.QtCore import QThread, pyqtSignal

from core.uart_manager import UARTManager
from core.sequence_engine import SequenceEngine
from core.attenuator_programmer import AttenuatorProgrammer
from core.database import get_session
from core.models import AnalyticalGroup

import pandas as pd
import os


# ============================================================================
# Job 5 Simulation Settings
# ============================================================================

# True:
#   MCU still receives all commands, but displayed data comes from CSV.
#
# False:
#   Displayed data comes from actual MCU ADC readings.
SIMULATION_FROM_EXCEL = False

# CSV file path.
# If relative, it is resolved from the project root.
SIMULATION_EXCEL_PATH = "simulation_data.csv"


class AnalysisWorker(QThread):
    """
    Background worker for Job 5: INT.1 Raw Intensity.

    Signals:
        progress(str, int): Status message and progress percentage.
        result(dict): Raw/intensity result payload.
        error(str): Error message.
        finished(): Emitted when worker finishes.
    """

    progress = pyqtSignal(str, int)
    result = pyqtSignal(dict)
    error = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, group_id: int, params: dict = None):
        super().__init__()

        self.group_id = group_id
        self.params = params or {}

        self._abort = False
        self._group_data = None

    def stop(self):
        """Request to abort the running analysis."""
        self._abort = True

    # =========================================================================
    # Main Worker Flow
    # =========================================================================

    def run(self):
        """
        Executes Job 5: INT.1 Raw Intensity.

        Flow:
        1. Load group data
        2. Connect to MCU
        3. Program ATT values
        4. Run real MCU sequence
        5. If simulation enabled, replace ADC/intensity data from CSV
        6. Emit result to Job5RunPage
        """
        try:
            # ── Step 1: Load group data ─────────────────────────────────
            self.progress.emit("Loading group data...", 5)

            self._group_data = self._load_group_data()

            if self._group_data is None:
                self.error.emit(f"Group {self.group_id} not found.")
                return

            if self._abort:
                self.error.emit("Aborted by user.")
                return

            # ── Step 2: Connect to hardware lazily ──────────────────────
            self.progress.emit("Connecting to hardware...", 10)

            uart = UARTManager()

            # Important:
            # This connects only when Start is pressed.
            # If already connected, UARTManager.connect() reuses the open port.
            if not uart.connect():
                self.error.emit(
                    "Failed to connect to hardware.\n"
                    "Check that the CH340 adapter is plugged in and the MCU is powered."
                )
                return

            if self._abort:
                self.error.emit("Aborted by user.")
                return

            # ── Step 3: Program attenuators every burn ──────────────────
            self.progress.emit("Programming attenuators...", 15)

            att_rows = self._group_data.get("page_02_attenuator", {}).get("rows", [])

            programmer = AttenuatorProgrammer(uart)
            prog_count = programmer.program_all(att_rows)

            print(f"[JOB5] Programmed {prog_count} attenuators", flush=True)

            if self._abort:
                self.error.emit("Aborted by user.")
                return

            # ── Step 4: Execute real MCU burn sequence ──────────────────
            self.progress.emit("Running burn sequence...", 20)

            sequence = SequenceEngine(uart)

            raw_adc_from_mcu = sequence.execute_full_sequence(
                page1_data=self._group_data.get("page_01_source", {}),
                page3_data=self._group_data.get("page_03_channel", []),
                progress_cb=lambda s, p: self.progress.emit(s, p)
            )

            if self._abort:
                self.error.emit("Aborted by user.")
                return

            # ── Step 5: Decide real ADC or CSV simulation output ────────
            if SIMULATION_FROM_EXCEL:
                self.progress.emit("Using Excel simulation data...", 82)

                simulated_intensities = self._load_simulated_intensities_from_excel()

                # Keep approximate raw_adc as well for reporting/debugging.
                # The UI displays intensities.
                raw_adc = self._make_raw_adc_from_display_values(simulated_intensities)
                results = simulated_intensities

                overflows = self._check_intensity_overflows(results)

                print("[JOB5] MCU raw ADC was read but display data was replaced by Excel.", flush=True)
                print(f"[JOB5] MCU raw ADC: {raw_adc_from_mcu}", flush=True)
                print(f"[JOB5] CSV intensities: {results}", flush=True)

            else:
                self.progress.emit("Processing intensities...", 85)

                raw_adc = raw_adc_from_mcu
                results = self._apply_ise_ratio(raw_adc)

                overflows = self._check_raw_adc_overflows(raw_adc)

            # ── Step 6: Emit result ─────────────────────────────────────
            self.progress.emit("Done!", 100)

            self.result.emit({
                "type": "INT.1",
                "sample": self.params.get("sample_name", "Unknown"),
                "raw_adc": raw_adc,
                "intensities": results,
                "overflows": overflows,
                "simulation": SIMULATION_FROM_EXCEL,
            })

        except Exception as e:
            self.error.emit(str(e))

        finally:
            self.finished.emit()

    # =========================================================================
    # Database
    # =========================================================================

    def _load_group_data(self) -> dict:
        """Load all page data for the group from the database."""
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return None

            return {
                "group_name": group.name,  
                "page_01_source": group.page_01_source,
                "page_02_attenuator": group.page_02_attenuator,
                "page_03_channel": group.page_03_channel,
            }

        finally:
            session.close()

    # =========================================================================
    # Excel Simulation
    # =========================================================================

    def _resolve_simulation_excel_path(self) -> str:

        if os.path.isabs(SIMULATION_EXCEL_PATH):
            return SIMULATION_EXCEL_PATH

        project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        return os.path.join(
            project_root,
            SIMULATION_EXCEL_PATH
        )


    def _load_simulated_intensities_from_excel(self) -> dict:
        """
        Workbook:

            simulation_data.xlsx

        Sheets:

            SUS
            CARBON_STEEL
            CAST_IRON

        Sheet Format:

            ITG | ELE | SAMPLE001 | SAMPLE002 | SAMPLE003

        Example:

            ITG,ELE,SAMPLE001,SAMPLE002
            1,FE,0.851,0.850
            2,CR,0.174,0.170
            3,NI,0.083,0.081
        """

        path = self._resolve_simulation_excel_path()

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Simulation workbook not found:\n{path}"
            )

        group_name = str(
            self._group_data.get("group_name", "")
        ).strip()

        if not group_name:
            raise ValueError(
                "Analytical group name not found."
            )

        try:
            df = pd.read_excel(
                path,
                sheet_name=group_name
            )

        except Exception:
            raise ValueError(
                f"Workbook does not contain sheet:\n{group_name}"
            )

        columns = [str(c).strip() for c in df.columns]

        if len(columns) < 3:
            raise ValueError(
                f"Sheet '{group_name}' must contain:\n"
                "ITG,ELE,<Sample Columns>"
            )

        sample_name = (
            self.params.get("sample_name", "")
            .strip()
            .upper()
        )

        value_column = columns[2]

        for col in columns[2:]:
            if col.upper() == sample_name:
                value_column = col
                break

        page3 = self._group_data.get(
            "page_03_channel",
            []
        )

        itg_to_display = {}

        for entry in page3:

            itg = str(
                entry.get("itg", "")
            ).strip()

            if not itg:
                continue

            display_name = (
                str(entry.get("name", "")).strip()
                or str(entry.get("ele", "")).strip()
                or f"ITG{itg}"
            )

            itg_to_display[itg] = display_name

        results = {}

        for _, row in df.iterrows():

            try:
                itg = str(int(row["ITG"])).strip()
            except Exception:
                continue

            if itg not in itg_to_display:
                continue

            try:
                value = float(row[value_column])
            except Exception:
                continue

            display_name = itg_to_display[itg]

            results[display_name] = value

        if not results:
            raise ValueError(
                f"No simulation data loaded for group '{group_name}'."
            )

        return results

    def _make_raw_adc_from_display_values(self, values: dict) -> dict:
        """
        Make approximate raw ADC values from display values.

        If value is 0.0 to 1.0:
            Treat as normalized intensity and convert to ADC counts.

        If value is greater than 1.0:
            Treat as already ADC-like and clamp to 0-4095.

        This is mainly for reporting/debugging while CSV simulation is enabled.
        """
        raw_adc = {}

        for name, value in values.items():
            try:
                v = float(value)
            except (TypeError, ValueError):
                v = 0.0

            if 0.0 <= v <= 1.0:
                adc = int(round(v * 4095))
            else:
                adc = int(round(v))

            adc = max(0, min(4095, adc))
            raw_adc[name] = adc

        return raw_adc

    # =========================================================================
    # Processing
    # =========================================================================

    def _display_key_for_page3_entry(self, entry: dict) -> str:
        """
        Build the same display key used by Job5RunPage.

        Preference:
        1. Page 3 NAME
        2. Page 3 ELE
        3. ITG fallback
        """
        name = str(entry.get("name", "")).strip()
        ele = str(entry.get("ele", "")).strip()
        itg = str(entry.get("itg", "")).strip()

        return name or ele or (f"ITG{itg}" if itg else "")

    def _apply_ise_ratio(self, raw_adc: dict) -> dict:
        """
        Apply Internal Standard ratio if configured on Page 3.

        Modes:
        1. ISE = 0:
            normalized intensity = ADC / 4095

        2. ISE > 0:
            relative intensity = element ADC / reference ADC * 100
        """
        page3_data = self._group_data.get("page_03_channel", []) or []

        ise_map = {}
        itg_to_key = {}

        for entry in page3_data:
            key = self._display_key_for_page3_entry(entry)

            if not key:
                continue

            try:
                itg = int(entry.get("itg", 0))
            except (TypeError, ValueError):
                itg = 0

            try:
                ise_ref = int(entry.get("ise_ref", 0))
            except (TypeError, ValueError):
                ise_ref = 0

            ise_map[key] = ise_ref
            itg_to_key[itg] = key

        results = {}

        for key, adc_value in raw_adc.items():
            try:
                adc_value = float(adc_value)
            except (TypeError, ValueError):
                adc_value = 0.0

            ise_ref = ise_map.get(key, 0)

            if ise_ref > 0:
                ref_key = itg_to_key.get(ise_ref)

                if ref_key and ref_key in raw_adc:
                    try:
                        ref_adc = float(raw_adc[ref_key])
                    except (TypeError, ValueError):
                        ref_adc = 0.0

                    if ref_adc > 0:
                        results[key] = (adc_value / ref_adc) * 100.0
                    else:
                        results[key] = 0.0
                else:
                    results[key] = adc_value / 4095.0

            else:
                results[key] = adc_value / 4095.0

        return results

    # =========================================================================
    # Overflow Checks
    # =========================================================================

    def _check_raw_adc_overflows(self, raw_adc: dict) -> list:
        """
        Check overflow using raw ADC.

        0.8 of 4095 is the functional overflow threshold.
        """
        overflows = []
        overflow_limit = int(0.8 * 4095)

        for name, value in raw_adc.items():
            try:
                adc = int(value)
            except (TypeError, ValueError):
                adc = 0

            if adc >= overflow_limit:
                overflows.append(name)

        return overflows

    def _check_intensity_overflows(self, intensities: dict) -> list:
        """
        Check overflow using displayed intensity values.

        Used mainly for CSV simulation where values are already display values.
        """
        overflows = []

        for name, value in intensities.items():
            try:
                v = float(value)
            except (TypeError, ValueError):
                v = 0.0

            if v > 0.8:
                overflows.append(name)

        return overflows