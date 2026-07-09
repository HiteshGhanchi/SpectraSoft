"""
SpectraSoft — Job 3: 2-Point Recalibration

This page performs 2-point recalibration using Page 4 H/L sample mappings.

Workflow:
1. User selects a Page 4 H/L sample name.
2. User presses Start one or more times to collect N burns.
3. The page calculates AVE for that sample.
4. User presses "Store Sample / Next Sample".
5. Repeat for all required H/L samples.
6. User presses "Cal / File".
7. The software calculates α and β for each Page 4 row where both H and L
   samples were measured in the current session.

Formula:
    alpha = (H_Target - L_Target) / (I_H - I_L)
    beta  = H_Target - (alpha * I_H)

Important:
- Uses processed intensities from AnalysisWorker, not raw ADC.
- Blank H/L values are skipped.
- "*" H/L values are skipped.
- Existing k values are preserved.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
    QProgressBar, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QFileDialog, QComboBox
)
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QTextDocument, QPageLayout
from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog

from core.analysis_worker import AnalysisWorker
from core.database import get_session
from core.models import AnalyticalGroup

import csv


class Job3RecalPage(QWidget):
    """Job 3: 2-Point Recalibration page."""

    def __init__(self, main_window, group_id: int, group_name: str, job_type: str = "3"):
        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self.job_type = job_type

        self.worker = None

        # Current selected sample burns:
        # [
        #   {"C": 95.1, "SI": 80.2, ...},
        #   {"C": 95.4, "SI": 80.5, ...}
        # ]
        self.results = []

        # Stored session sample averages:
        # {
        #   "GOLD_A": {"C": 95.2, "SI": 80.3},
        #   "GOLD_C": {"C": 31.5, "SI": 42.1},
        # }
        self.sample_results = {}

        self.element_names = []
        self.required_samples = []

        self.an_count = 0
        self.tan_count = 0

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._build_ui()
        self._setup_job_ui()
        self._load_elements()
        self._load_required_samples()
        self._populate_sample_dropdown()
        self._update_table()
        self._update_progress_summary()

    # =========================================================================
    # UI
    # =========================================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar ─────────────────────────────────────────────────────
        title_bar = QWidget()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("background:#5c9bd5;")

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(12, 0, 12, 0)

        self.title_label = QLabel(f"Job 3: 2-Point Recalibration - {self.group_name}")
        self.title_label.setStyleSheet("color:white;font:bold 10pt Arial;")

        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        root.addWidget(title_bar)

        # ── Outer Frame ──────────────────────────────────────────────────
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:white;")
        root.addWidget(outer, stretch=1)

        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(10, 10, 10, 10)
        outer_layout.setSpacing(6)

        # ── Parameter area ───────────────────────────────────────────────
        self.params_area = QWidget()
        self.params_area.setFixedHeight(44)
        outer_layout.addWidget(self.params_area)

        # ── Progress Bar ─────────────────────────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(
            "QProgressBar{"
            "background:#f0f0f0;"
            "border:1px solid #888888;"
            "height:20px;"
            "text-align:center;"
            "}"
            "QProgressBar::chunk{"
            "background:#0078d7;"
            "}"
        )
        outer_layout.addWidget(self.progress_bar)

        # ── Status Label ─────────────────────────────────────────────────
        self.status_label = QLabel(
            "Ready. Select a Page 4 H/L sample, run burns, then store the sample."
        )
        self.status_label.setStyleSheet(
            "QLabel{"
            "background:#d4d0c8;"
            "color:#333333;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        outer_layout.addWidget(self.status_label)

        # ── Progress Summary ─────────────────────────────────────────────
        self.recal_summary_label = QLabel("")
        self.recal_summary_label.setStyleSheet(
            "QLabel{"
            "background:#f0ece4;"
            "color:#333333;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        self.recal_summary_label.setFixedHeight(34)
        outer_layout.addWidget(self.recal_summary_label)

        # ── ST Counter ───────────────────────────────────────────────────
        self.st_counter = QLabel("ST No.: —")
        self.st_counter.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.st_counter.setStyleSheet("font:bold 9pt Arial; color:#555555;")
        outer_layout.addWidget(self.st_counter)

        # ── Results Table ────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setStyleSheet(
            "QTableWidget{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "gridline-color:#888888;"
            "font:9pt Arial;"
            "}"
            "QTableWidget::item{"
            "border:1px solid #888888;"
            "padding:0px 4px;"
            "color:black;"
            "background:white;"
            "}"
            "QHeaderView::section{"
            "background:#0078d7;"
            "color:white;"
            "font:bold 9pt Arial;"
            "border:1px solid #888888;"
            "padding:2px 4px;"
            "}"
            "QTableWidget::item:selected{"
            "background:#cce5ff;"
            "color:black;"
            "}"
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setDefaultSectionSize(27)

        outer_layout.addWidget(self.table, stretch=1)

        # ── Footer ───────────────────────────────────────────────────────
        footer = QWidget()
        footer.setAutoFillBackground(True)
        footer.setStyleSheet("background:#d4d0c8; border-top:1px solid #888888;")
        footer.setFixedHeight(28)

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(10, 4, 10, 4)
        footer_layout.setSpacing(20)

        self.an_label = QLabel("AN: 0")
        self.an_label.setStyleSheet("font:9pt Arial; color:black;")
        footer_layout.addWidget(self.an_label)

        self.tan_label = QLabel("TAN: 0")
        self.tan_label.setStyleSheet("font:9pt Arial; color:black;")
        footer_layout.addWidget(self.tan_label)

        footer_layout.addStretch()

        outer_layout.addWidget(footer)

        # ── Buttons ──────────────────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        bbp = btn_bar.palette()
        bbp.setColor(btn_bar.backgroundRole(), Qt.GlobalColor.lightGray)
        btn_bar.setPalette(bbp)
        btn_bar.setFixedHeight(40)

        btn_layout = QHBoxLayout(btn_bar)
        btn_layout.setContentsMargins(0, 4, 0, 4)
        btn_layout.setSpacing(4)

        btn_style = self._button_style()

        self.btn_start = QPushButton("Start")
        self.btn_start.setStyleSheet(btn_style)
        self.btn_start.clicked.connect(self._on_start)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setStyleSheet(btn_style)
        self.btn_stop.clicked.connect(self._on_stop)
        self.btn_stop.setEnabled(False)

        self.btn_store = QPushButton("Store Sample / Next Sample")
        self.btn_store.setStyleSheet(btn_style)
        self.btn_store.clicked.connect(self._on_store_sample)

        self.btn_cal = QPushButton("Cal / File")
        self.btn_cal.setStyleSheet(btn_style)
        self.btn_cal.clicked.connect(self._on_cal_file)

        self.btn_reset = QPushButton("Reset Current")
        self.btn_reset.setStyleSheet(btn_style)
        self.btn_reset.clicked.connect(self._on_reset_current)

        self.btn_reset_session = QPushButton("Reset Session")
        self.btn_reset_session.setStyleSheet(btn_style)
        self.btn_reset_session.clicked.connect(self._on_reset_session)

        self.btn_export = QPushButton("Export CSV")
        self.btn_export.setStyleSheet(btn_style)
        self.btn_export.clicked.connect(self._on_export)

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addWidget(self.btn_store)
        btn_layout.addWidget(self.btn_cal)
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_reset_session)
        btn_layout.addWidget(self.btn_export)

        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(btn_style)
        cancel_btn.clicked.connect(self._on_cancel)
        btn_layout.addWidget(cancel_btn)

        outer_layout.addWidget(btn_bar)

    def _setup_job_ui(self):
        if self.params_area.layout():
            while self.params_area.layout().count():
                item = self.params_area.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            old_layout = self.params_area.layout()
            if old_layout:
                old_layout.deleteLater()

        layout = QVBoxLayout(self.params_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        row = QHBoxLayout()
        row.setSpacing(8)

        lbl = QLabel("Sample Name:")
        lbl.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl)

        self.sample_name = QComboBox()
        self.sample_name.setFixedWidth(280)
        self.sample_name.setStyleSheet(
            "QComboBox{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
            "QComboBox QAbstractItemView{"
            "background:white;"
            "color:black;"
            "selection-background-color:#0078d7;"
            "selection-color:white;"
            "}"
        )
        row.addWidget(self.sample_name)

        row.addStretch()
        layout.addLayout(row)

    def _button_style(self) -> str:
        return (
            "QPushButton{"
            "background:#d4d0c8;"
            "color:black;"
            "border:2px outset #aaaaaa;"
            "font:9pt Arial;"
            "padding:4px 12px;"
            "min-width:70px;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )

    # =========================================================================
    # Load Page 3 / Page 4 Data
    # =========================================================================

    def _load_elements(self):
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group and group.page_03_channel:
                for entry in group.page_03_channel:
                    name = str(entry.get("name", "")).strip()
                    ele = str(entry.get("ele", "")).strip()
                    itg = str(entry.get("itg", "")).strip()

                    display_name = name or ele or (f"ITG{itg}" if itg else "")

                    if display_name:
                        self.element_names.append(display_name)

        finally:
            session.close()

    def _load_required_samples(self):
        """
        Load unique H/L sample names from Page 4.

        Job 3 uses only H and L samples.
        Blank and "*" are ignored.
        """
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group or not group.page_04_drift:
                self.required_samples = []
                return

            page4 = group.page_04_drift

            if not isinstance(page4, dict):
                self.required_samples = []
                return

            rows = page4.get("rows", [])

            if not isinstance(rows, list):
                self.required_samples = []
                return

            samples = set()

            for row in rows:
                for key in ["h_sample", "l_sample"]:
                    sample = str(row.get(key, "")).strip().upper()

                    if not sample:
                        continue

                    if sample == "*":
                        continue

                    samples.add(sample)

            self.required_samples = sorted(samples)

        finally:
            session.close()

    def _populate_sample_dropdown(self):
        self.sample_name.clear()
        self.sample_name.addItem("", "")

        for sample in self.required_samples:
            self.sample_name.addItem(sample, sample)

    def _current_sample_name(self) -> str:
        return str(self.sample_name.currentData() or "").strip().upper()

    # =========================================================================
    # Table / Averages
    # =========================================================================

    def _update_table(self):
        if not self.element_names:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.status_label.setText(
                "No elements configured. Complete Page 3 before running Job 3."
            )
            return

        num_burns = len(self.results)
        num_cols = 2 + num_burns

        self.table.setRowCount(len(self.element_names))
        self.table.setColumnCount(num_cols)

        headers = ["Element", "AVE"]

        for i in range(num_burns):
            headers.append(f"N={i + 1}")

        self.table.setHorizontalHeaderLabels(headers)

        self.table.setColumnWidth(0, 90)
        self.table.setColumnWidth(1, 90)

        for i in range(num_burns):
            self.table.setColumnWidth(2 + i, 90)

        averages = self._calculate_averages()

        for row, elem in enumerate(self.element_names):
            elem_item = QTableWidgetItem(elem)
            elem_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, elem_item)

            if elem in averages:
                avg_item = QTableWidgetItem(f"{averages:.5f}")
                avg_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.table.setItem(row, 1, avg_item)

            for burn_index, burn in enumerate(self.results):
                val = burn.get(elem, 0.0)
                try:
                    val_float = float(val)
                except (TypeError, ValueError):
                    val_float = 0.0

                val_item = QTableWidgetItem(f"{val_float:.5f}")
                val_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.table.setItem(row, 2 + burn_index, val_item)

        self.table.resizeRowsToContents()

    def _calculate_averages(self) -> dict:
        averages = {}

        for elem in self.element_names:
            values = []

            for burn in self.results:
                if elem in burn:
                    try:
                        values.append(float(burn[elem]))
                    except (TypeError, ValueError):
                        pass

            if values:
                averages[elem] = sum(values) / len(values)

        return averages

    def _update_footer_counts(self):
        self.an_label.setText(f"AN: {self.an_count}")
        self.tan_label.setText(f"TAN: {self.tan_count}")

    def _update_progress_summary(self):
        measured = sorted(self.sample_results.keys())
        required = self.required_samples

        missing = [s for s in required if s not in self.sample_results]

        ready_count, total_candidate_count = self._count_ready_rows()

        self.recal_summary_label.setText(
            f"Required samples: {', '.join(required) if required else 'None'}   |   "
            f"Measured: {', '.join(measured) if measured else 'None'}   |   "
            f"Missing: {', '.join(missing) if missing else 'None'}   |   "
            f"Rows ready for α/β: {ready_count}/{total_candidate_count}"
        )

    def _count_ready_rows(self) -> tuple[int, int]:
        page4_rows = self._get_page4_rows()
        ready = 0
        total = 0

        for row in page4_rows:
            h_sample = str(row.get("h_sample", "")).strip().upper()
            l_sample = str(row.get("l_sample", "")).strip().upper()

            if not h_sample or not l_sample:
                continue

            if h_sample == "*" or l_sample == "*":
                continue

            total += 1

            if h_sample in self.sample_results and l_sample in self.sample_results:
                ready += 1

        return ready, total

    def _get_page4_rows(self) -> list:
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group or not group.page_04_drift:
                return []

            page4 = group.page_04_drift

            if not isinstance(page4, dict):
                return []

            rows = page4.get("rows", [])

            return rows if isinstance(rows, list) else []

        finally:
            session.close()

    # =========================================================================
    # Actions
    # =========================================================================

    def _on_start(self):
        if self.worker and self.worker.isRunning():
            return

        if not self.element_names:
            QMessageBox.warning(
                self,
                "No Elements",
                "No elements are configured for this analytical group.\n\n"
                "Please complete Page 3 before running Job 3."
            )
            return

        sample = self._current_sample_name()

        if not sample:
            QMessageBox.warning(
                self,
                "Sample Required",
                "Please select a sample name from Page 4 H/L mapping."
            )
            return

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.sample_name.setEnabled(False)

        self.status_label.setText(f"Starting 2-point recalibration burn for {sample}...")
        self.progress_bar.setValue(0)

        self.worker = AnalysisWorker(
            group_id=self.group_id,
            params={
                "sample_name": sample,
                "job_type": "3"
            }
        )

        self.worker.progress.connect(self._on_progress)
        self.worker.result.connect(self._on_result)
        self.worker.error.connect(self._on_error)
        self.worker.finished.connect(self._on_finished)

        self.worker.start()

    def _on_stop(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.status_label.setText("Stopping...")
            self.btn_stop.setEnabled(False)

    def _on_progress(self, step: str, percent: int):
        self.status_label.setText(step)
        self.progress_bar.setValue(percent)

    def _on_result(self, results: dict):
        if "intensities" in results:
            data = results["intensities"]
        elif "raw_adc" in results:
            data = results["raw_adc"]
        else:
            data = results

        self.an_count += 1
        self.tan_count += 1
        self._update_footer_counts()

        self.results.append(data)

        self.st_counter.setText(f"ST No.: {len(self.results)}")
        self._update_table()

        self.status_label.setText(
            f"Burn {len(self.results)} complete for sample {self._current_sample_name()}."
        )
        self.progress_bar.setValue(100)

    def _on_error(self, error_msg: str):
        QMessageBox.critical(self, "Analysis Error", error_msg)

        self.status_label.setText(f"Error: {error_msg}")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.sample_name.setEnabled(True)
        self.progress_bar.setValue(0)

    def _on_finished(self):
        self.worker = None

        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

        if self.status_label.text() == "Stopping...":
            self.status_label.setText("Stopped")

    def _on_store_sample(self):
        sample = self._current_sample_name()

        if not sample:
            QMessageBox.warning(
                self,
                "Sample Required",
                "Please select a sample before storing."
            )
            return

        if not self.results:
            QMessageBox.warning(
                self,
                "No Data",
                "No burns are available for the current sample."
            )
            return

        averages = self._calculate_averages()

        if not averages:
            QMessageBox.warning(
                self,
                "No Data",
                "No valid average intensities are available."
            )
            return

        if sample in self.sample_results:
            reply = QMessageBox.question(
                self,
                "Overwrite Sample",
                f"Sample {sample} was already stored in this session.\n\nOverwrite it?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        self.sample_results[sample] = averages

        self.results = []
        self.st_counter.setText("ST No.: —")
        self.sample_name.setEnabled(True)
        self._update_table()
        self._update_progress_summary()

        self.status_label.setText(
            f"Sample {sample} stored. Set next sample and press Start."
        )

    def _on_reset_current(self):
        if self.results:
            reply = QMessageBox.question(
                self,
                "Reset Current Sample",
                "Clear burns for the currently selected sample?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        self.results = []
        self.st_counter.setText("ST No.: —")
        self.sample_name.setEnabled(True)
        self._update_table()
        self.status_label.setText("Current sample reset.")

    def _on_reset_session(self):
        reply = QMessageBox.question(
            self,
            "Reset Session",
            "Clear all stored sample measurements in this Job 3 session?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self.results = []
        self.sample_results = {}
        self.st_counter.setText("ST No.: —")
        self.sample_name.setEnabled(True)
        self._update_table()
        self._update_progress_summary()
        self.status_label.setText("Session reset.")

    # =========================================================================
    # Cal / File
    # =========================================================================

    def _on_cal_file(self):
        if not self.sample_results:
            QMessageBox.warning(
                self,
                "No Stored Samples",
                "No sample averages are stored. Use Store Sample / Next Sample first."
            )
            return

        updated, skipped = self._calculate_and_file_alpha_beta()

        if updated == 0:
            QMessageBox.warning(
                self,
                "No Rows Updated",
                "No Page 4 rows had both H and L samples measured.\n\n"
                f"Skipped rows: {skipped}"
            )
            return

        QMessageBox.information(
            self,
            "Recalibration Completed",
            f"2-point recalibration completed.\n\n"
            f"Rows updated: {updated}\n"
            f"Rows skipped: {skipped}"
        )

        self._update_progress_summary()
        self.status_label.setText(
            f"Cal / File completed. Updated α and β for {updated} rows."
        )

    def _calculate_and_file_alpha_beta(self) -> tuple[int, int]:
        """
        Calculate and file alpha/beta into Page 4.

        For each Page 4 row:
        - H and L samples must be non-empty and not "*".
        - Both H and L samples must be measured in this session.
        - Element must exist in both sample average dictionaries.
        - H/L targets must be valid.
        - I_H - I_L must not be zero.
        """
        session = get_session()
        updated = 0
        skipped = 0

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return 0, 0

            page4 = group.page_04_drift

            if not isinstance(page4, dict) or not isinstance(page4.get("rows"), list):
                return 0, 0

            rows = page4["rows"]

            for row in rows:
                elem = str(row.get("name", "")).strip()

                if not elem:
                    skipped += 1
                    continue

                h_sample = str(row.get("h_sample", "")).strip().upper()
                l_sample = str(row.get("l_sample", "")).strip().upper()

                if not h_sample or not l_sample:
                    skipped += 1
                    continue

                if h_sample == "*" or l_sample == "*":
                    skipped += 1
                    continue

                if h_sample not in self.sample_results:
                    skipped += 1
                    continue

                if l_sample not in self.sample_results:
                    skipped += 1
                    continue

                h_values = self.sample_results[h_sample]
                l_values = self.sample_results[l_sample]

                if elem not in h_values or elem not in l_values:
                    skipped += 1
                    continue

                try:
                    i_h = float(h_values[elem])
                    i_l = float(l_values[elem])
                    h_target = float(str(row.get("h_target", "0")).strip() or "0")
                    l_target = float(str(row.get("l_target", "0")).strip() or "0")
                except (TypeError, ValueError):
                    skipped += 1
                    continue

                # If both targets are zero, row is effectively unconfigured.
                if h_target == 0.0 and l_target == 0.0:
                    skipped += 1
                    continue

                denom = i_h - i_l

                if denom == 0.0:
                    skipped += 1
                    continue

                alpha = (h_target - l_target) / denom
                beta = h_target - (alpha * i_h)

                row["alpha"] = f"{alpha:.4f}"
                row["beta"] = f"{beta:.5f}"

                # k is preserved. If missing, use neutral default.
                if not str(row.get("k_coeff", "")).strip():
                    row["k_coeff"] = "1.0000"

                updated += 1

            group.page_04_drift = page4
            session.commit()

            return updated, skipped

        finally:
            session.close()

    # =========================================================================
    # Export / Print
    # =========================================================================

    def _on_export(self):
        if not self.results and not self.sample_results:
            QMessageBox.warning(self, "No Data", "No data to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Job 3 Results",
            "job3_recalibration_results.csv",
            "CSV Files (*.csv)"
        )

        if not path:
            return

        try:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)

                writer.writerow(["Stored Sample Measurements"])

                all_elements = self.element_names

                writer.writerow(["Sample"] + all_elements)

                for sample, values in self.sample_results.items():
                    row = [sample]

                    for elem in all_elements:
                        val = values.get(elem, "")
                        row.append(f"{float(val):.5f}" if val != "" else "")

                    writer.writerow(row)

                writer.writerow([])
                writer.writerow(["Current Sample Table"])

                headers = []

                for col in range(self.table.columnCount()):
                    header_item = self.table.horizontalHeaderItem(col)
                    headers.append(header_item.text() if header_item else "")

                writer.writerow(headers)

                for row_idx in range(self.table.rowCount()):
                    row_data = []

                    for col in range(self.table.columnCount()):
                        item = self.table.item(row_idx, col)
                        row_data.append(item.text() if item else "")

                    writer.writerow(row_data)

            QMessageBox.information(
                self,
                "Exported",
                f"Results exported to:\n{path}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def _on_print(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setPageOrientation(QPageLayout.Orientation.Landscape)

        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self._render_print_page)
        preview.exec()

    def _render_print_page(self, printer):
        doc = QTextDocument()
        doc.setHtml(self._generate_html_report())
        doc.print(printer)

    def _generate_html_report(self) -> str:
        timestamp = QDate.currentDate().toString("dd-MM-yyyy")

        stored_rows = []

        for sample, values in self.sample_results.items():
            cells = f"<td>{sample}</td>"

            for elem in self.element_names:
                val = values.get(elem, "")
                cells += f"<td>{float(val):.5f}</td>" if val != "" else "<td></td>"

            stored_rows.append(f"<tr>{cells}</tr>")

        element_headers = "".join(f"<th>{e}</th>" for e in self.element_names)

        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; font-size: 9pt; }}
                th {{ background-color: #34495e; color: white; padding: 5px; }}
                td {{ border: 1px solid #777; padding: 4px; }}
            </style>
        </head>
        <body>
            <h1>SpectraSoft Job 3 Recalibration Report - {self.group_name}</h1>
            <p><b>Date:</b> {timestamp}</p>
            <h2>Stored Sample Measurements</h2>
            <table>
                <tr><th>Sample</th>{element_headers}</tr>
                {''.join(stored_rows)}
            </table>
        </body>
        </html>
        """

    # =========================================================================
    # Navigation
    # =========================================================================

    def _on_cancel(self):
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Cancel Analysis",
                "Analysis is still running. Stop and cancel?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.worker.stop()
                QTimer.singleShot(500, self._go_back)
            else:
                return
        else:
            self._go_back()

    def _go_back(self):
        from ui.analysis.job_selection import JobSelectionPage
        self.main_window.set_right_widget(JobSelectionPage(self.main_window))

    def wants_fullscreen(self) -> bool:
        return True