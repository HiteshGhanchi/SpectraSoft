"""
SpectraSoft — Main Window
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStatusBar, QFrame, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from core.persistence.database import DB_PATH, SessionLocal, engine
from core.maintenance.service import MaintenanceService
from ui.theme import harmonize_widget_tree


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpectraSoft")
        self.setObjectName("mainWindow")
        self.setMinimumSize(1200, 720)
        self.resize(1360, 820)

        self._current_action = None
        self._uart = None
        self._active_right_widget = None

        self._build_menu()
        self._build_body()
        self._build_status_bar()

    # =========================================================================
    # Menu
    # =========================================================================

    def _build_menu(self):
        mb = self.menuBar()
        mb.setObjectName("topMenuBar")

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

        # ── Instrument Settings ──────────────────────────────────────────
        settings_m = mb.addMenu("Settings")
        self.action_instrument_configuration = QAction(
            "Instrument Configuration", self
        )
        self.action_instrument_configuration.setCheckable(True)
        self.action_instrument_configuration.triggered.connect(
            self._open_instrument_configuration
        )
        settings_m.addAction(self.action_instrument_configuration)

        # ── Attenuator Adjustment ─────────────────────────────────────────
        adjustment_m = mb.addMenu("Attenuator Adjustment")
        self.action_attenuator_adjustment = QAction(
            "Attenuator Adjustment", self
        )
        self.action_attenuator_adjustment.setCheckable(True)
        self.action_attenuator_adjustment.triggered.connect(
            self._open_attenuator_adjustment
        )
        adjustment_m.addAction(self.action_attenuator_adjustment)

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

        report_m = mb.addMenu("Report")
        self.action_report = QAction("Filed Results", self)
        self.action_report.setCheckable(True)
        self.action_report.triggered.connect(self._open_report)
        report_m.addAction(self.action_report)

        maintenance_m = mb.addMenu("Maintenance")
        self.action_maintenance = QAction("Maintenance and Backup", self)
        self.action_maintenance.setCheckable(True)
        self.action_maintenance.triggered.connect(self._open_maintenance)
        maintenance_m.addAction(self.action_maintenance)

        result_m = mb.addMenu("Result Settings")
        self.action_result_settings = QAction("Product / R Control / Optional", self)
        self.action_result_settings.setCheckable(True)
        self.action_result_settings.triggered.connect(self._open_result_settings)
        result_m.addAction(self.action_result_settings)

        guide_m = mb.addMenu("Workflow Guide")
        self.action_workflow_guide = QAction("Workflow Guide", self)
        self.action_workflow_guide.setCheckable(True)
        self.action_workflow_guide.triggered.connect(self._open_workflow_guide)
        guide_m.addAction(self.action_workflow_guide)

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
        root.setObjectName("contentSurface")
        self.setCentralWidget(root)

        h = QHBoxLayout(root)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        from ui.anainf.group_panel import GroupPanel
        self._group_panel = GroupPanel(self)
        self._group_panel.setObjectName("navigationRail")
        self._group_panel.setMinimumWidth(240)
        self._group_panel.setMaximumWidth(280)
        h.addWidget(self._group_panel)

        self._div = QFrame()
        self._div.setObjectName("shellDivider")
        self._div.setFrameShape(QFrame.Shape.VLine)
        self._div.setFrameShadow(QFrame.Shadow.Sunken)
        h.addWidget(self._div)

        self._right = QWidget()
        self._right.setObjectName("contentSurface")
        self._right.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
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
                if hasattr(item.widget(), "shutdown_for_navigation"):
                    item.widget().shutdown_for_navigation()
                item.widget().deleteLater()

        harmonize_widget_tree(widget)
        self._right_layout.addWidget(widget)
        self._active_right_widget = widget

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
        sb.setObjectName("statusBar")
        self.setStatusBar(sb)

        # No automatic hardware connection here.
        self.conn_status_label = QLabel("⚪ Not Connected")
        self.conn_status_label.setObjectName("connectionStatusLabel")
        sb.addWidget(self.conn_status_label)

    # =========================================================================
    # Menu Actions
    # =========================================================================

    def _open_source_codes(self):
        from ui.settings.source_codes_page import SourceCodesPage
        self._set_active_menu(self.action_source)
        self.set_right_widget(SourceCodesPage(self))

    def _open_instrument_configuration(self):
        from ui.settings.instrument_configuration_page import InstrumentConfigurationPage

        self._set_active_menu(self.action_instrument_configuration)
        self.set_right_widget(InstrumentConfigurationPage(self))

    def _open_attenuator_adjustment(self):
        gid, gname = self._get_current_group()
        if gid is None:
            self._warn_no_group()
            return

        from ui.adjustment.attenuator_adjustment_page import AttenuatorAdjustmentPage

        self._set_active_menu(self.action_attenuator_adjustment)
        self.set_right_widget(AttenuatorAdjustmentPage(self, gid, gname))

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

    def _open_report(self):
        gid, gname = self._get_current_group()
        if gid is None:
            self._warn_no_group()
            return
        from ui.report.result_report_page import ResultReportPage
        self._set_active_menu(self.action_report)
        self.set_right_widget(ResultReportPage(self, gid, gname))

    def _open_maintenance(self):
        from ui.maintenance.maintenance_page import MaintenancePage

        def dispose_database():
            engine.dispose()

        service = MaintenanceService(SessionLocal)
        self._set_active_menu(self.action_maintenance)
        self.set_right_widget(
            MaintenancePage(
                service,
                database_path=DB_PATH,
                dispose_callback=dispose_database,
            )
        )

    def _open_result_settings(self):
        gid, gname = self._get_current_group()
        if gid is None:
            self._warn_no_group()
            return
        from ui.anainf.page_10_result_settings import ResultSettingsPage
        self._set_active_menu(self.action_result_settings)
        self.set_right_widget(ResultSettingsPage(self, gid, gname))

    def _open_workflow_guide(self):
        from ui.help.workflow_guide_page import WorkflowGuidePage

        self._set_active_menu(self.action_workflow_guide)
        self.set_right_widget(WorkflowGuidePage(self))

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
