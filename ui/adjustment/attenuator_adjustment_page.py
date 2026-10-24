"""Native group-aware Attenuator Adjustment operation."""

import threading
import time

from PyQt6.QtCore import QObject, QThread, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.adjustment.service import (
    AdjustmentHistory,
    AttenuatorAdjustmentRunner,
    get_adjustment_preset,
    save_group_att,
    validate_att_value,
    validate_adjustment_channel,
)
from core.hardware.factory import create_spectrometer_controller
from core.persistence.configuration import get_or_create_instrument_configuration
from core.persistence.database import get_session
from core.persistence.models import AnalyticalGroup, MasterElement
from ui.adjustment.adjustment_graph import AdjustmentGraphWidget
from ui.anainf.page_02_attenuator import ordered_selected_elements


def load_adjustment_context(session, group_id: int, emission_unit_type: str) -> dict:
    """Load selected group channels and the system-level adjustment preset."""
    group = session.get(AnalyticalGroup, group_id)
    if group is None:
        raise ValueError(f"Analytical Group {group_id} does not exist")

    channel_data = group.page_03_channel if isinstance(group.page_03_channel, list) else []
    master_elements = session.query(MasterElement).order_by(MasterElement.itg_no).all()
    selected_elements = ordered_selected_elements(channel_data, master_elements)
    channel_by_itg = {}
    for channel in channel_data:
        try:
            channel_by_itg[int(channel.get("itg"))] = channel
        except (AttributeError, TypeError, ValueError):
            continue

    saved_att = {}
    for row in (group.page_02_attenuator or {}).get("rows", []):
        try:
            saved_att[int(row.get("itg_no"))] = int(row.get("att_value", 0))
        except (AttributeError, TypeError, ValueError):
            continue

    channels = []
    for element in selected_elements:
        channel = channel_by_itg.get(int(element.itg_no), {})
        seq = str(channel.get("seq", ""))
        condition = group.page_01_source or {}
        try:
            group_integration_ms = int(condition.get(f"integ_seq{seq}", 0) or 0)
        except (TypeError, ValueError):
            group_integration_ms = 0
        channels.append(
            {
                "itg": int(element.itg_no),
                "ele": element.ele_name or "",
                "wavelength": element.wavelength or "",
                "seq": seq,
                "source": condition.get(f"source_seq{seq}", ""),
                "group_integration_ms": group_integration_ms,
                "att_value": saved_att.get(int(element.itg_no), 0),
            }
        )

    return {
        "group": group,
        "condition": group.page_01_source or {},
        "channels": channels,
        "preset": get_adjustment_preset(emission_unit_type),
    }


class AdjustmentWorker(QObject):
    reading_ready = pyqtSignal(object)
    status_changed = pyqtSignal(str)
    failed = pyqtSignal(str)
    att_applied = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, condition, channel, preset, att_value):
        super().__init__()
        self.condition = condition
        self.channel = channel
        self.preset = preset
        self._att_value = att_value
        self._att_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._controller = None
        self._applied_att = int(att_value)

    @pyqtSlot(int)
    def update_att(self, att_value: int):
        value = validate_att_value(att_value)
        with self._att_lock:
            self._att_value = value
        if self._controller is not None:
            if not self._controller.set_attenuator(int(self.channel["itg"]), value):
                self.failed.emit("Unable to apply the new attenuator value")
                return
        self._applied_att = value
        self.att_applied.emit(value)

    @pyqtSlot()
    def stop(self):
        self._stop_event.set()

    @pyqtSlot()
    def run(self):
        controller = None
        runner = None
        try:
            controller = create_spectrometer_controller()
            self._controller = controller
            if not controller.connect():
                raise RuntimeError("Unable to connect to the spectrometer")
            runner = AttenuatorAdjustmentRunner(controller)
            self.status_changed.emit("Measuring selected channel...")
            while not self._stop_event.is_set():
                with self._att_lock:
                    att_value = self._att_value
                reading = runner.measure_once(
                    self.condition, self.channel, self.preset, att_value
                )
                self.reading_ready.emit(reading)
                self._stop_event.wait(0.2)
        except Exception as exc:
            self.failed.emit(str(exc))
        finally:
            if runner is not None:
                runner.shutdown()
            elif controller is not None:
                try:
                    controller.shutdown()
                except Exception:
                    pass
            if controller is not None:
                try:
                    controller.close()
                except Exception:
                    pass
            self._controller = None
            self.finished.emit()


class AttenuatorAdjustmentPage(QWidget):
    """Operator page for selecting and accepting production ATT."""

    att_update_requested = pyqtSignal(int)

    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self._context = {}
        self._thread = None
        self._worker = None
        self._history = AdjustmentHistory()
        self._last_applied_att = None
        self.setStyleSheet(
            "QWidget{background:#d4d0c8;color:#000000;}"
            "QLabel{color:#000000;}"
            "QPushButton{color:#000000;}"
        )
        self._build_ui()
        self._load()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)
        root.setSpacing(6)

        title = QLabel(f"Attenuator Adjustment - {self.group_name}")
        title.setStyleSheet("background:#5c9bd5;color:white;font:bold 10pt Arial;padding:5px;")
        root.addWidget(title)

        self._status = QLabel("Ready")
        root.addWidget(self._status)

        form = QFormLayout()
        self.channel_combo = QComboBox()
        self.channel_combo.currentIndexChanged.connect(self._on_channel_changed)
        form.addRow("Analytical Channel", self.channel_combo)

        self._unit_label = QLabel()
        form.addRow("Emission Unit", self._unit_label)
        self.change_unit_button = QPushButton(
            "Change emission unit in Instrument Configuration"
        )
        self.change_unit_button.clicked.connect(self._on_change_unit)
        form.addRow("", self.change_unit_button)
        self._guidance_label = QLabel()
        self._guidance_label.setWordWrap(True)
        form.addRow("Adjustment Guidance", self._guidance_label)
        self._sequence_label = QLabel()
        form.addRow("Group Sequence", self._sequence_label)

        self.att_spin = QSpinBox()
        self.att_spin.setRange(0, 63)
        form.addRow("ATT (0-63)", self.att_spin)
        root.addLayout(form)

        controls = QHBoxLayout()
        self.start_button = QPushButton("Start Measurement")
        self.start_button.clicked.connect(self._on_start)
        controls.addWidget(self.start_button)
        self.apply_button = QPushButton("Apply ATT")
        self.apply_button.clicked.connect(self._on_apply_att)
        self.apply_button.setEnabled(False)
        controls.addWidget(self.apply_button)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self._on_stop)
        self.stop_button.setEnabled(False)
        controls.addWidget(self.stop_button)
        self.accept_button = QPushButton("Accept ATT")
        self.accept_button.clicked.connect(self._on_accept)
        self.accept_button.setEnabled(False)
        controls.addWidget(self.accept_button)
        root.addLayout(controls)

        self._current_intensity = QLabel("Current intensity: —")
        self._average_intensity = QLabel("Average intensity: —")
        root.addWidget(self._current_intensity)
        root.addWidget(self._average_intensity)

        self.graph = AdjustmentGraphWidget()
        root.addWidget(self.graph, stretch=1)

        self.readings_table = QTableWidget(0, 4)
        self.readings_table.setHorizontalHeaderLabels(["Time", "ATT", "Intensity", "In Target"])
        self.readings_table.setMaximumHeight(130)
        root.addWidget(self.readings_table)

    def _load(self):
        session = get_session()
        try:
            config = get_or_create_instrument_configuration(session)
            self._context = load_adjustment_context(
                session, self.group_id, config.emission_unit_type
            )
        finally:
            session.close()

        preset = self._context["preset"]
        self.graph.set_target_band(preset.target_min, preset.target_max)
        self._unit_label.setText(preset.emission_unit_type.replace("_", "-"))
        self._guidance_label.setText(
            f"Scale x{preset.scale}; graduation {preset.graduation_min}-{preset.graduation_max}; "
            f"integration {preset.integration_ms / 1000:.0f}s; target {preset.target_min:.1f}-{preset.target_max:.1f}."
        )
        for channel in self._context["channels"]:
            self.channel_combo.addItem(
                f"{channel['itg']}: {channel['ele']}", channel
            )
        if not self._context["channels"]:
            self._status.setText("No valid selected analytical channels are configured.")
            self.start_button.setEnabled(False)
            self.accept_button.setEnabled(False)
        else:
            self._on_channel_changed(0)

    def _selected_channel(self):
        channel = self.channel_combo.currentData()
        return channel if isinstance(channel, dict) else None

    def _on_channel_changed(self, _index):
        channel = self._selected_channel()
        if not channel:
            return
        self.att_spin.setValue(int(channel.get("att_value", 0)))
        self._sequence_label.setText(
            f"SEQ {channel.get('seq') or '—'} | Source {channel.get('source') or '—'} | "
            f"Configured integration {channel.get('group_integration_ms', 0)} ms"
        )

    def _on_change_unit(self):
        """Open the system-level setting; HPSG/HVS is not group-specific."""
        if hasattr(self.main_window, "_open_instrument_configuration"):
            self.main_window._open_instrument_configuration()

    def _on_start(self):
        channel = self._selected_channel()
        if not channel:
            self._show_warning("Select an analytical channel first.")
            return
        valid, message = validate_adjustment_channel(channel)
        if not valid:
            self._show_warning(message)
            return
        if self._thread is not None:
            return

        self._history = AdjustmentHistory()
        self._last_applied_att = None
        self.graph.set_history([])
        self.readings_table.setRowCount(0)
        self.channel_combo.setEnabled(False)
        self.accept_button.setEnabled(False)
        self._worker = AdjustmentWorker(
            self._context["condition"],
            channel,
            self._context["preset"],
            self.att_spin.value(),
        )
        self._thread = QThread(self)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self.att_update_requested.connect(self._worker.update_att)
        self._worker.reading_ready.connect(self._on_reading)
        self._worker.status_changed.connect(self._status.setText)
        self._worker.failed.connect(self._on_worker_failed)
        self._worker.finished.connect(self._on_worker_finished)
        self._thread.start()
        self.start_button.setEnabled(False)
        self.apply_button.setEnabled(True)
        self.stop_button.setEnabled(True)

    def _on_apply_att(self):
        if self._worker is not None:
            self.att_update_requested.emit(self.att_spin.value())
            self._status.setText(f"Applying ATT {self.att_spin.value()}...")

    def _on_stop(self):
        if self._worker is not None:
            self._worker.stop()
            self._status.setText("Stopping measurement...")

    def _on_accept(self):
        channel = self._selected_channel()
        if not channel or not self._history.readings:
            return
        if self._worker is not None:
            self._worker.stop()
        session = get_session()
        try:
            accepted_att = self._last_applied_att
            if accepted_att is None:
                return
            save_group_att(session, self.group_id, channel, accepted_att)
        finally:
            session.close()
        channel["att_value"] = accepted_att
        self.accept_button.setEnabled(False)
        self._status.setText(f"Accepted ATT {accepted_att} for {channel['ele']}.")

    def _on_reading(self, reading):
        self._history.readings.append(reading)
        if (
            not self._history.att_markers
            or self._history.att_markers[-1][1] != reading.att_value
        ):
            self._history.att_markers.append((reading.timestamp, reading.att_value))
        self._last_applied_att = reading.att_value
        self.accept_button.setEnabled(True)
        graph_history = [
            (item.timestamp, item.intensity, item.att_value)
            for item in self._history.readings
        ]
        self.graph.set_history(graph_history)
        preset = self._context["preset"]
        in_target = preset.target_min <= reading.intensity <= preset.target_max
        row = self.readings_table.rowCount()
        self.readings_table.insertRow(row)
        values = [
            time.strftime("%H:%M:%S", time.localtime(reading.timestamp)),
            str(reading.att_value),
            f"{reading.intensity:.4f}",
            "Yes" if in_target else "No",
        ]
        for col, value in enumerate(values):
            self.readings_table.setItem(row, col, QTableWidgetItem(value))
        self._current_intensity.setText(f"Current intensity: {reading.intensity:.4f}")
        average = sum(item.intensity for item in self._history.readings) / len(self._history.readings)
        self._average_intensity.setText(f"Average intensity: {average:.4f}")

    def _on_worker_failed(self, message):
        self._status.setText(f"Measurement failed: {message}")
        self.accept_button.setEnabled(False)
        self._show_warning(message)

    def _on_worker_finished(self):
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait(1000)
            self._thread.deleteLater()
        if self._worker is not None:
            self._worker.deleteLater()
        self._thread = None
        self._worker = None
        self.start_button.setEnabled(bool(self._context.get("channels")))
        self.channel_combo.setEnabled(bool(self._context.get("channels")))
        self.apply_button.setEnabled(False)
        self.stop_button.setEnabled(False)

    def _show_warning(self, text):
        QMessageBox.warning(self, "Attenuator Adjustment", text)

    def closeEvent(self, event):
        self.shutdown_for_navigation()
        event.accept()

    def shutdown_for_navigation(self):
        """Stop hardware work before the main window replaces this page."""
        if self._worker is not None:
            self._worker.stop()
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait(2000)
