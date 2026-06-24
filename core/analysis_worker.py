"""
SpectraSoft — Analysis Worker
================================
Runs spectrometer analysis in a background QThread to keep the UI responsive.

Signals:
    progress(str, int) – progress step and percentage (0-100)
    result(dict) – analysis results (raw intensities + processed data)
    error(str) – error message
    finished() – emitted when the worker finishes (success or failure)

Usage:
    worker = AnalysisWorker(group_id, job_type, params)
    worker.progress.connect(update_progress_bar)
    worker.result.connect(display_results)
    worker.error.connect(show_error)
    worker.finished.connect(enable_ui)
    worker.start()
    # To abort:
    worker.stop()
"""

from PyQt6.QtCore import QThread, pyqtSignal

from core.database import get_session
from core.models import AnalyticalGroup
from core.hardware import hw, HardwareError
import traceback


class AnalysisWorker(QThread):
    """Background worker for spectrometer analysis."""

    progress = pyqtSignal(str, int)   # step_name, percent (0-100)
    result = pyqtSignal(dict)         # final results
    error = pyqtSignal(str)           # error message
    finished = pyqtSignal()           # always emitted at the end

    def __init__(self, group_id: int, job_type: str, params: dict = None):
        """
        Args:
            group_id: Analytical Group ID
            job_type: 'X', 'Y', '2', '3', '4', '5', '6', '7', '8'
            params: dict with job-specific parameters:
                - For Job X/Y: {"sample_name": str}
                - For Job 2: {"k_sample": str}
                - For Job 3: {"h_sample": str, "l_sample": str}
                - For Job 4: {"master_sample": str}
                - For Job 8: {"h_sample": str, "l_sample": str, "k_sample": str}
                - Others: {}
        """
        super().__init__()
        self.group_id = group_id
        self.job_type = job_type
        self.params = params or {}
        self._abort = False

    def stop(self):
        """Request to abort the running analysis."""
        self._abort = True

    def run(self):
        """Main thread entry point."""
        try:
            # 1. Load group data
            self.progress.emit("Loading group data…", 5)
            group_data = self._load_group_data()
            if group_data is None:
                self.error.emit(f"Group {self.group_id} not found.")
                return

            if self._abort:
                self.error.emit("Aborted by user.")
                return

            # 2. Prepare progress callback for hardware
            def progress_cb(step: str, percent: int):
                if self._abort:
                    raise HardwareError("Aborted")
                self.progress.emit(step, percent)

            # 3. Run the appropriate job
            self.progress.emit(f"Running Job {self.job_type}…", 10)
            if self.job_type == 'X':
                results = self._run_content_analysis(group_data, progress_cb)
            elif self.job_type == 'Y':
                results = self._run_three_time_analysis(group_data, progress_cb)
            elif self.job_type == '2':
                results = self._run_1_point_recal(group_data, progress_cb)
            elif self.job_type == '3':
                results = self._run_2_point_recal(group_data, progress_cb)
            elif self.job_type == '4':
                results = self._run_master_curve_recal(group_data, progress_cb)
            elif self.job_type == '5':
                results = self._run_int1(group_data, progress_cb)
            elif self.job_type == '6':
                results = self._run_int2(group_data, progress_cb)
            elif self.job_type == '7':
                results = self._run_int2_wc(group_data, progress_cb)
            elif self.job_type == '8':
                results = self._run_int2_target(group_data, progress_cb)
            else:
                self.error.emit(f"Unknown job type: {self.job_type}")
                return

            if self._abort:
                self.error.emit("Aborted by user.")
                return

            # 4. Emit results
            self.progress.emit("Analysis complete.", 100)
            self.result.emit(results)

        except HardwareError as e:
            if str(e) == "Aborted":
                self.error.emit("Analysis aborted by user.")
            else:
                self.error.emit(f"Hardware error: {str(e)}")
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        finally:
            self.finished.emit()

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_group_data(self) -> dict:
        """Load all page data for the group."""
        session = get_session()
        try:
            group = session.get(AnalyticalGroup, self.group_id)
            if not group:
                return None
            return {
                "page_01_condition": group.page_01_condition,
                "page_02_attenuator": group.page_02_attenuator,
                "page_03_element": group.page_03_element,
                "page_04_drift": group.page_04_drift,
                "page_05_wc": group.page_05_wc,
                "page_06_matrix": group.page_06_matrix,
                "page_07_master": group.page_07_master,
                "page_08_display": group.page_08_display,
                "page_09_purity": group.page_09_purity,
            }
        finally:
            session.close()

    # ------------------------------------------------------------------
    # Job implementations
    # ------------------------------------------------------------------

    def _run_content_analysis(self, group_data: dict, progress_cb):
        """Job X: Content Analysis."""
        raw = hw.run_analysis(group_data, progress_cb)
        return {
            "type": "content",
            "sample": self.params.get("sample_name", "Unknown"),
            "raw_intensities": raw,
            "concentrations": {},  # Placeholder for future correction
        }

    def _run_three_time_analysis(self, group_data: dict, progress_cb):
        """Job Y: 3-Time Analysis."""
        results = []
        for i in range(3):
            if self._abort:
                raise HardwareError("Aborted")
            progress_cb(f"Burn {i+1}/3", 10 + i * 25)
            raw = hw.run_analysis(group_data, progress_cb)
            results.append(raw)
        avg = {}
        for key in results[0].keys():
            vals = [r.get(key, 0) for r in results]
            avg[key] = sum(vals) / len(vals)
        return {
            "type": "3-time",
            "sample": self.params.get("sample_name", "Unknown"),
            "burns": results,
            "average": avg,
        }

    def _run_1_point_recal(self, group_data: dict, progress_cb):
        """Job 2: 1-Point Recalibration."""
        raw = hw.run_analysis(group_data, progress_cb)
        return {
            "type": "1-point recal",
            "k_sample": self.params.get("k_sample", ""),
            "raw_intensities": raw,
            "k": 1.0,  # Placeholder
        }

    def _run_2_point_recal(self, group_data: dict, progress_cb):
        """Job 3: 2-Point Recalibration."""
        progress_cb("Measuring H standard…", 20)
        raw_h = hw.run_analysis(group_data, progress_cb)
        if self._abort:
            raise HardwareError("Aborted")
        progress_cb("Measuring L standard…", 60)
        raw_l = hw.run_analysis(group_data, progress_cb)
        return {
            "type": "2-point recal",
            "h_sample": self.params.get("h_sample", ""),
            "l_sample": self.params.get("l_sample", ""),
            "raw_h": raw_h,
            "raw_l": raw_l,
            "alpha": 1.0,  # Placeholder
            "beta": 0.0,   # Placeholder
        }

    def _run_master_curve_recal(self, group_data: dict, progress_cb):
        """Job 4: Master Curve Recalibration."""
        raw = hw.run_analysis(group_data, progress_cb)
        return {
            "type": "master curve recal",
            "master_sample": self.params.get("master_sample", ""),
            "raw_intensities": raw,
            "ac": 0.0,  # Placeholder
            "mc": 1.0,  # Placeholder
        }

    def _run_int1(self, group_data: dict, progress_cb):
        """Job 5: INT.1 (Raw Intensity)."""
        raw = hw.run_analysis(group_data, progress_cb)
        return {
            "type": "INT.1",
            "raw_intensities": raw,
        }

    def _run_int2(self, group_data: dict, progress_cb):
        """Job 6: INT.2 (Drift Corrected)."""
        raw = hw.run_analysis(group_data, progress_cb)
        return {
            "type": "INT.2",
            "raw_intensities": raw,
        }

    def _run_int2_wc(self, group_data: dict, progress_cb):
        """Job 7: INT.2 for Working Curve."""
        raw = hw.run_analysis(group_data, progress_cb)
        return {
            "type": "INT.2 for WC",
            "raw_intensities": raw,
        }

    # =========================================================================
    # JOB 8: INT.2 for Target
    # =========================================================================

    def _run_int2_target(self, group_data: dict, progress_cb):
        """
        Job 8: INT.2 for Target.

        Measures H, L, and K standards and saves the intensities as targets
        on Page 4 of the Analytical Group.

        Workflow:
            1. Run burn on H standard → Get H intensity
            2. Run burn on L standard → Get L intensity
            3. Run burn on K standard → Get K intensity
            4. Save all intensities to page_04_drift in the database

        Args:
            group_data: Dictionary containing all page data
            progress_cb: Callback for progress updates

        Returns:
            dict: Results with sample names and measured intensities

        Raises:
            HardwareError: If aborted or hardware fails
        """
        h_sample = self.params.get("h_sample", "A")
        l_sample = self.params.get("l_sample", "B")
        k_sample = self.params.get("k_sample", "C")

        results = {}

        # ── Step 1: Measure High Standard (H) ──────────────────────────────
        progress_cb(f"Measuring H standard ({h_sample})…", 20)
        raw_h = hw.run_analysis(group_data, progress_cb)
        if self._abort:
            raise HardwareError("Aborted")
        results["h_intensities"] = raw_h
        results["h_sample"] = h_sample

        # ── Step 2: Measure Low Standard (L) ──────────────────────────────
        progress_cb(f"Measuring L standard ({l_sample})…", 50)
        raw_l = hw.run_analysis(group_data, progress_cb)
        if self._abort:
            raise HardwareError("Aborted")
        results["l_intensities"] = raw_l
        results["l_sample"] = l_sample

        # ── Step 3: Measure 1-Point Standard (K) ──────────────────────────
        progress_cb(f"Measuring K standard ({k_sample})…", 80)
        raw_k = hw.run_analysis(group_data, progress_cb)
        if self._abort:
            raise HardwareError("Aborted")
        results["k_intensities"] = raw_k
        results["k_sample"] = k_sample

        # ── Step 4: Save targets to Page 4 ──────────────────────────────
        progress_cb("Saving target values…", 90)
        self._save_targets_to_page4(h_sample, l_sample, k_sample, raw_h, raw_l, raw_k)

        results["type"] = "INT.2 for Target"
        results["saved"] = True

        progress_cb("Target values saved.", 100)
        return results

    def _save_targets_to_page4(self, h_sample: str, l_sample: str, k_sample: str,
                               raw_h: dict, raw_l: dict, raw_k: dict):
        """
        Save measured intensities as targets on Page 4.

        The targets are saved per element. Since the hardware measures
        ALL elements simultaneously, we store the intensity for each element
        separately.

        For each element, we store:
            - H_target: intensity from High standard
            - L_target: intensity from Low standard
            - K_target: intensity from 1-point standard

        Args:
            h_sample: Name of the High standard
            l_sample: Name of the Low standard
            k_sample: Name of the 1-point standard
            raw_h: Raw intensities from High standard
            raw_l: Raw intensities from Low standard
            raw_k: Raw intensities from 1-point standard
        """
        session = get_session()
        try:
            group = session.get(AnalyticalGroup, self.group_id)
            if not group:
                raise ValueError(f"Group {self.group_id} not found.")

            # Get current Page 4 data (or create if empty)
            drift_data = group.page_04_drift or {}

            # ── Get the first element's intensity as the target ──────────
            # For simplicity, we use the first element's intensity.
            # In a real implementation, we might store per-element targets.
            # But the old system stores a single target value per element
            # (the one used as the "master" for drift correction).
            #
            # For simplicity, we use the first key in the dictionary.
            # A more robust implementation would store per-element targets.
            h_target = list(raw_h.values())[0] if raw_h else 0.0
            l_target = list(raw_l.values())[0] if raw_l else 0.0
            k_target = list(raw_k.values())[0] if raw_k else 0.0

            # ── Update Page 4 with targets ──────────────────────────────
            drift_data["h_sample"] = h_sample
            drift_data["l_sample"] = l_sample
            drift_data["k_sample"] = k_sample
            drift_data["h_target"] = h_target
            drift_data["l_target"] = l_target
            drift_data["k_target"] = k_target

            # Keep existing alpha, beta, k if they exist
            # (They should be 1.0, 0.0, 1.0 by default)
            drift_data.setdefault("alpha", 1.0)
            drift_data.setdefault("beta", 0.0)
            drift_data.setdefault("k_coeff", 1.0)

            # ── Save back to database ─────────────────────────────────────
            group.page_04_drift = drift_data
            session.commit()

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()