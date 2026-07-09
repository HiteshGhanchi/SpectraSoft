"""
SpectraSoft — Main Window
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStatusBar, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpectraSoft")

        # Fixed size — window cannot be resized
        self.setFixedSize(1100, 680)

        self._current_action = None
        self._uart = None

        self._build_menu()
        self._build_body()
        self._build_status_bar()

    # =========================================================================
    # Menu
    # =========================================================================

    def _build_menu(self):
        mb = self.menuBar()
        mb.setStyleSheet(
            "QMenuBar{"
            "background:#c0b8a8;"
            "color:#000000;"
            "border-bottom:1px solid #888888;"
            "}"
            "QMenuBar::item{"
            "background:#c0b8a8;"
            "color:#000000;"
            "padding:2px 10px;"
            "}"
            "QMenuBar::item:selected{"
            "background:#0078d7;"
            "color:#ffffff;"
            "}"
            "QMenu{"
            "background:#ffffff;"
            "color:#000000;"
            "border:1px solid #888888;"
            "}"
            "QMenu::item:selected{"
            "background:#0078d7;"
            "color:#ffffff;"
            "}"
        )

        # ── Analytical Group ─────────────────────────────────────────────
        group_m = mb.addMenu("Analytical Group")
        self.action_group = QAction("Analytical Group", self)
        self.action_group.setCheckable(True)
        self.action_group.triggered.connect(self._show_home_content)
        group_m.addAction(self.action_group)

        # ── Master Elements ──────────────────────────────────────────────
        master_m = mb.addMenu("Master Elements")
        self.action_master = QAction("Master Elements", self)
        self.action_master.setCheckable(True)
        self.action_master.triggered.connect(self._open_master_elements)
        master_m.addAction(self.action_master)

        # ── Source Codes ─────────────────────────────────────────────────
        source_m = mb.addMenu("Source Codes")
        self.action_source = QAction("Source Codes", self)
        self.action_source.setCheckable(True)
        self.action_source.triggered.connect(self._open_source_codes)
        source_m.addAction(self.action_source)

        # ── Analysis Menu ────────────────────────────────────────────────
        analysis_m = mb.addMenu("Analysis")

        self.action_analysis = QAction("Analysis Jobs", self)
        self.action_analysis.setCheckable(True)
        self.action_analysis.triggered.connect(self._open_job_selection)
        analysis_m.addAction(self.action_analysis)

        # ── Regression Menu ──────────────────────────────────────────────
        regression_m = mb.addMenu("Regression")

        self.action_chemical_standards = QAction("Chemical Standards", self)
        self.action_chemical_standards.setCheckable(True)
        self.action_chemical_standards.triggered.connect(
            self._open_chemical_standards
        )
        regression_m.addAction(self.action_chemical_standards)

        self.action_regression_calc = QAction("Regression Calculation", self)
        self.action_regression_calc.setCheckable(True)
        self.action_regression_calc.triggered.connect(
            self._open_regression_calculation
        )
        regression_m.addAction(self.action_regression_calc)

        self.action_matrix_calc = QAction("Matrix Coefficient Calculation", self)
        self.action_matrix_calc.setCheckable(True)
        self.action_matrix_calc.triggered.connect(
            self._open_matrix_calculation
        )
        regression_m.addAction(self.action_matrix_calc)

        regression_m.addSeparator()

        self.action_working_curve_page = QAction("Working Curve Coefficients", self)
        self.action_working_curve_page.setCheckable(True)
        self.action_working_curve_page.triggered.connect(
            self._open_working_curve_page
        )
        regression_m.addAction(self.action_working_curve_page)

        # Default: Analytical Group checked
        self.action_group.setChecked(True)
        self._current_action = self.action_group

    def _set_active_menu(self, action):
        if self._current_action:
            self._current_action.setChecked(False)

        action.setChecked(True)
        self._current_action = action

    # =========================================================================
    # Body
    # =========================================================================

    def _build_body(self):
        root = QWidget()
        root.setStyleSheet("background:#d4d0c8;")
        self.setCentralWidget(root)

        h = QHBoxLayout(root)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        from ui.anainf.group_panel import GroupPanel
        self._group_panel = GroupPanel(self)
        self._group_panel.setFixedWidth(230)
        h.addWidget(self._group_panel)

        self._div = QFrame()
        self._div.setFrameShape(QFrame.Shape.VLine)
        self._div.setFrameShadow(QFrame.Shadow.Sunken)
        self._div.setStyleSheet("color:#aaaaaa;")
        h.addWidget(self._div)

        self._right = QWidget()
        self._right.setStyleSheet("background:#d4d0c8;")
        self._right_layout = QVBoxLayout(self._right)
        self._right_layout.setContentsMargins(0, 0, 0, 0)
        self._right_layout.setSpacing(0)
        h.addWidget(self._right, stretch=1)

        self._show_home_content()

    # =========================================================================
    # Right Panel Management
    # =========================================================================

    def set_right_widget(self, widget):
        while self._right_layout.count():
            item = self._right_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._right_layout.addWidget(widget)

        if hasattr(widget, "wants_fullscreen") and callable(widget.wants_fullscreen):
            self.set_fullscreen_mode(widget.wants_fullscreen())
        else:
            self.set_fullscreen_mode(False)

    def set_left_panel_visible(self, visible: bool):
        self._group_panel.setVisible(visible)
        self._div.setVisible(visible)

    def set_fullscreen_mode(self, enabled: bool):
        self.set_left_panel_visible(not enabled)

    # =========================================================================
    # Home / Default View
    # =========================================================================

    def _show_home_content(self):
        self._set_active_menu(self.action_group)
        self.set_fullscreen_mode(False)

        w = QWidget()
        w.setStyleSheet("background:#d4d0c8;")
        v = QVBoxLayout(w)
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hint = QLabel(
            "Select an Analytical Group from the left panel.\n\n"
            "Use Analysis → Analysis Jobs for hardware jobs.\n"
            "Use Regression → Chemical Standards / Regression Calculation "
            "for working curve setup."
        )
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet(
            "QLabel{"
            "background:#d4d0c8;"
            "color:#666666;"
            "border:none;"
            "font:9pt Arial;"
            "}"
        )
        v.addWidget(hint)

        self.set_right_widget(w)

    # =========================================================================
    # Status Bar
    # =========================================================================

    def _build_status_bar(self):
        sb = QStatusBar()
        sb.setStyleSheet("background:#d4d0c8; color:#000000;")
        self.setStatusBar(sb)

        # No automatic hardware connection here.
        self.conn_status_label = QLabel("⚪ Not Connected")
        self.conn_status_label.setStyleSheet(
            "padding: 2px 8px; font: 9pt Arial;"
        )
        sb.addWidget(self.conn_status_label)

    # =========================================================================
    # Menu Actions
    # =========================================================================

    def _open_source_codes(self):
        from ui.settings.source_codes_page import SourceCodesPage
        self._set_active_menu(self.action_source)
        self.set_right_widget(SourceCodesPage(self))

    def _open_master_elements(self):
        from ui.settings.master_elements_page import MasterElementsPage
        self._set_active_menu(self.action_master)
        self.set_right_widget(MasterElementsPage(self))

    def _open_job_selection(self):
        """
        Open hardware analysis job selection page.

        This still requires an Analytical Group because all jobs depend on AG data.
        """
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        self._set_active_menu(self.action_analysis)

        from ui.analysis.job_selection import JobSelectionPage
        self.set_right_widget(JobSelectionPage(self))

    # =========================================================================
    # Regression Menu Actions
    # =========================================================================

    def _open_chemical_standards(self):
        """
        Open chemical standards input page.

        This page stores certified/lab chemical values for standards.
        Data is saved into:
            AnalyticalGroup.page_05_chemical_standards
        """
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        self._set_active_menu(self.action_chemical_standards)

        try:
            from ui.regression.chemical_standards_page import ChemicalStandardsPage

            self.set_right_widget(
                ChemicalStandardsPage(
                    self,
                    gid,
                    gname
                )
            )

        except ImportError:
            QMessageBox.information(
                self,
                "Regression",
                "Chemical Standards page is not built yet."
            )

    def _open_regression_calculation(self):
        """
        Open regression calculation page.

        This page calculates a,b,c,d using:
            page_05_wc_measurements
            page_05_chemical_standards

        Then it files coefficients into:
            page_05_wc
        """
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        self._set_active_menu(self.action_regression_calc)

        try:
            from ui.regression.regression_calculation_page import RegressionCalculationPage

            self.set_right_widget(
                RegressionCalculationPage(
                    self,
                    gid,
                    gname
                )
            )

        except ImportError:
            QMessageBox.information(
                self,
                "Regression",
                "Regression Calculation page is not built yet."
            )
            
    def _open_matrix_calculation(self):
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        self._set_active_menu(self.action_matrix_calc)

        try:
            from ui.regression.matrix_calculation_page import MatrixCalculationPage

            self.set_right_widget(
                MatrixCalculationPage(
                    self,
                    gid,
                    gname
                )
            )

        except ImportError:
            QMessageBox.information(
                self,
                "Regression",
                "Matrix Coefficient Calculation page is not built yet."
            )

    def _open_working_curve_page(self):
        """
        Open Page 5 working curve coefficients directly from Regression menu.
        """
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        self._set_active_menu(self.action_working_curve_page)

        try:
            from ui.anainf.page_05_working_curve import WorkingCurvePage

            self.set_right_widget(
                WorkingCurvePage(
                    self,
                    gid,
                    gname
                )
            )

        except ImportError:
            QMessageBox.information(
                self,
                "Regression",
                "Working Curve page is not built yet."
            )

    # =========================================================================
    # Helpers
    # =========================================================================

    def _get_current_group(self):
        if hasattr(self._group_panel, "_selected"):
            gid, gname = self._group_panel._selected()
            if gid is not None:
                return gid, gname

        return None, None

    def _warn_no_group(self):
        QMessageBox.warning(
            self,
            "No Analytical Group Selected",
            "Please select an Analytical Group from the left panel first."
        )