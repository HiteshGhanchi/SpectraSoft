"""Instrument-wide configuration screen."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.persistence.configuration import (
    get_or_create_instrument_configuration,
    set_emission_unit_type,
)
from core.persistence.database import get_session
from import_data.constants import EMISSION_UNIT_HPSG_300, EMISSION_UNIT_HVS


class InstrumentConfigurationPage(QWidget):
    """Edit the installed emission unit used by the whole spectrometer."""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet(
            "QWidget{background:#d4d0c8;color:#000000;}"
            "QLabel{color:#000000;}"
            "QPushButton{color:#000000;}"
        )
        self._build_ui()
        self._load()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 30, 40, 30)
        root.setSpacing(12)

        title = QLabel("INSTRUMENT CONFIGURATION")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "background:#5c9bd5;color:#000000;font:bold 11pt Arial;padding:6px;"
        )
        root.addWidget(title)

        explanation = QLabel(
            "Select the emission unit installed in the physical spectrometer. "
            "This value is stored once for the instrument and is read by "
            "Attenuator Adjustment."
        )
        explanation.setWordWrap(True)
        explanation.setStyleSheet("background:#d4d0c8;color:#000000;font:9pt Arial;")
        root.addWidget(explanation)

        label = QLabel("Emission Unit Type")
        label.setStyleSheet("font:bold 9pt Arial;")
        root.addWidget(label)

        self.emission_unit_combo = QComboBox()
        self.emission_unit_combo.addItem("HPSG-300", EMISSION_UNIT_HPSG_300)
        self.emission_unit_combo.addItem("HVS", EMISSION_UNIT_HVS)
        self.emission_unit_combo.setFixedWidth(260)
        self.emission_unit_combo.setStyleSheet(
            "QComboBox{background:#ffffff;color:#000000;border:1px solid #888888;padding:4px;}"
            "QComboBox QAbstractItemView{background:#ffffff;color:#000000;selection-background-color:#cce5ff;selection-color:#000000;}"
        )
        root.addWidget(self.emission_unit_combo)

        self.available_units_label = QLabel("Available: HPSG-300 and HVS")
        self.available_units_label.setStyleSheet(
            "background:#d4d0c8;color:#000000;font:9pt Arial;"
        )
        root.addWidget(self.available_units_label)

        self.status_label = QLabel()
        self.status_label.setStyleSheet("color:#000000;font:9pt Arial;")
        root.addWidget(self.status_label)

        save = QPushButton("Save Instrument Configuration")
        save.setFixedWidth(260)
        save.clicked.connect(self._on_save)
        root.addWidget(save)
        root.addStretch()

    def _load(self):
        session = get_session()
        try:
            config = get_or_create_instrument_configuration(session)
            index = self.emission_unit_combo.findData(config.emission_unit_type)
            if index >= 0:
                self.emission_unit_combo.setCurrentIndex(index)
            self.status_label.setText(
                f"Installed emission unit: {self.emission_unit_combo.currentText()}"
            )
        finally:
            session.close()

    def _on_save(self):
        session = get_session()
        try:
            config = set_emission_unit_type(
                session, self.emission_unit_combo.currentData()
            )
            self.status_label.setText(
                f"Saved: {config.emission_unit_type.replace('_', '-')}"
            )
            QMessageBox.information(
                self,
                "Saved",
                "Instrument emission-unit configuration saved.",
            )
        finally:
            session.close()
