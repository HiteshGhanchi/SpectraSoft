"""Maintenance administration page with safe backup and journal controls."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QWidget,
)

from core.persistence.backup_service import BackupService
from core.persistence.portable_package import PortablePackageService


class DatabaseOperationWorker(QThread):
    completed = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(
        self,
        service,
        destination=None,
        *,
        operation="backup",
        restore_source=None,
        dispose_callback=None,
        parent=None,
    ):
        super().__init__(parent)
        self.service = service
        self.destination = destination
        self.operation = operation
        self.restore_source = restore_source
        self.dispose_callback = dispose_callback

    def run(self):
        try:
            if self.operation == "package_export":
                result = self.service.export_package(self.destination)
            elif self.operation == "package_import":
                result = self.service.import_package(
                    self.restore_source,
                    confirmed=True,
                )
            elif self.restore_source is None:
                result = self.service.create_backup(self.destination)
            else:
                result = self.service.restore(
                    self.restore_source,
                    confirmed=True,
                    dispose_callback=self.dispose_callback,
                )
            self.completed.emit(result)
        except Exception as exc:  # surfaced to the page as a user-facing status
            self.failed.emit(str(exc))


class MaintenancePage(QWidget):
    """Operator-facing maintenance status, journal, and database administration."""

    def __init__(self, maintenance_service, *, database_path=None, dispose_callback=None, parent=None):
        super().__init__(parent)
        self.maintenance_service = maintenance_service
        self.database_path = Path(database_path or "data.db").expanduser().resolve()
        self.dispose_callback = dispose_callback
        self.backup_service = BackupService(self.database_path, dispose_callback=dispose_callback)
        self.portable_service = PortablePackageService(
            self.database_path,
            dispose_callback=dispose_callback,
        )
        self._backup_worker = None
        self._no_button = QMessageBox.StandardButton.No

        self.status_label = QLabel("Ready")
        self.operation_buttons = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Maintenance and Administration")
        title.setStyleSheet("font-weight: bold; font-size: 14pt;")
        layout.addWidget(title)

        hardware_box = QGroupBox("Instrument maintenance capabilities")
        hardware_layout = QFormLayout(hardware_box)
        for operation in self.maintenance_service.OPERATIONS:
            capability = self.maintenance_service.capability(operation)
            button = QPushButton(capability.label)
            button.setEnabled(capability.available)
            button.setToolTip(capability.reason)
            button.clicked.connect(lambda _checked=False, op=operation: self._on_verified_operation(op))
            self.operation_buttons[operation] = button
            hardware_layout.addRow(button, QLabel("Verified integration available" if capability.available else capability.reason))
        layout.addWidget(hardware_box)

        journal_box = QGroupBox("Record operator-confirmed maintenance")
        journal_layout = QFormLayout(journal_box)
        self.manual_operation_combo = QComboBox()
        for operation in self.maintenance_service.OPERATIONS:
            self.manual_operation_combo.addItem(self.maintenance_service.LABELS[operation], operation)
        self.operator_edit = QLineEdit()
        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setPlaceholderText("Manual observation or completion note")
        record_button = QPushButton("Record manual completion")
        record_button.clicked.connect(self._on_record_manual)
        journal_layout.addRow("Operation:", self.manual_operation_combo)
        journal_layout.addRow("Operator:", self.operator_edit)
        journal_layout.addRow("Notes:", self.notes_edit)
        journal_layout.addRow(record_button)
        layout.addWidget(journal_box)

        backup_box = QGroupBox("SQLite system backup and restore")
        backup_layout = QFormLayout(backup_box)
        self.backup_path_edit = QLineEdit(str(self.database_path.with_name("data-backup.db")))
        backup_button = QPushButton("Create verified backup")
        backup_button.clicked.connect(self._on_backup)
        self.restore_path_edit = QLineEdit()
        dry_run_button = QPushButton("Verify restore (dry run)")
        dry_run_button.clicked.connect(self._on_restore_dry_run)
        restore_button = QPushButton("Restore with confirmation")
        restore_button.clicked.connect(self._on_restore)
        backup_layout.addRow("Backup destination:", self.backup_path_edit)
        backup_layout.addRow(backup_button)
        backup_layout.addRow("Restore source:", self.restore_path_edit)
        backup_layout.addRow(dry_run_button, restore_button)
        layout.addWidget(backup_box)

        package_box = QGroupBox("Portable all-data package")
        package_layout = QFormLayout(package_box)
        self.export_package_path_edit = QLineEdit(
            str(self.database_path.with_name("spectrasoft-export.zip"))
        )
        export_package_button = QPushButton("Export all data package")
        export_package_button.clicked.connect(self._on_export_package)
        self.import_package_path_edit = QLineEdit()
        verify_package_button = QPushButton("Verify package (dry run)")
        verify_package_button.clicked.connect(self._on_verify_package)
        import_package_button = QPushButton("Import package with confirmation")
        import_package_button.clicked.connect(self._on_import_package)
        package_layout.addRow("Export destination:", self.export_package_path_edit)
        package_layout.addRow(export_package_button)
        package_layout.addRow("Import package:", self.import_package_path_edit)
        package_layout.addRow(verify_package_button, import_package_button)
        layout.addWidget(package_box)

        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        layout.addStretch()

    def _on_backup(self):
        if self._backup_worker is not None:
            return
        destination = self.backup_path_edit.text().strip()
        if not destination:
            self.status_label.setText("Backup destination is required.")
            return
        self.status_label.setText("Creating SQLite online backup...")
        self._backup_worker = DatabaseOperationWorker(self.backup_service, destination, parent=self)
        self._backup_worker.completed.connect(self._on_worker_complete)
        self._backup_worker.failed.connect(self._on_worker_failed)
        self._backup_worker.finished.connect(self._on_worker_finished)
        self._backup_worker.start()

    def _on_restore_dry_run(self):
        source = self._restore_source_path()
        if source is None:
            self.status_label.setText("Restore source is required.")
            return
        try:
            result = self.backup_service.restore(source, dry_run=True)
            self.status_label.setText(
                f"Dry run verified {result.validation.table_count} SQLite tables; no data was changed."
            )
        except Exception as exc:
            self.status_label.setText(f"Restore dry run failed: {exc}")

    def _on_restore(self):
        source = self._restore_source_path()
        if source is None:
            self.status_label.setText("Restore source is required.")
            return
        answer = QMessageBox.question(
            self,
            "Confirm database restore",
            "Restore this SQLite backup? A pre-restore backup will be preserved first.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            self.status_label.setText("Restore requires confirmation; no data was changed.")
            return
        self.status_label.setText("Restoring database after preserving the pre-restore backup...")
        self._backup_worker = DatabaseOperationWorker(
            self.backup_service,
            self.database_path,
            restore_source=source,
            dispose_callback=self.dispose_callback,
            parent=self,
        )
        self._backup_worker.completed.connect(self._on_worker_complete)
        self._backup_worker.failed.connect(self._on_worker_failed)
        self._backup_worker.finished.connect(self._on_worker_finished)
        self._backup_worker.start()

    def _on_export_package(self):
        if self._backup_worker is not None:
            return
        destination = self.export_package_path_edit.text().strip()
        if not destination:
            self.status_label.setText("Portable export destination is required.")
            return
        self.status_label.setText("Exporting and validating all application data...")
        self._backup_worker = DatabaseOperationWorker(
            self.portable_service,
            destination,
            operation="package_export",
            parent=self,
        )
        self._backup_worker.completed.connect(self._on_worker_complete)
        self._backup_worker.failed.connect(self._on_worker_failed)
        self._backup_worker.finished.connect(self._on_worker_finished)
        self._backup_worker.start()

    def _on_verify_package(self):
        source = self._package_source_path()
        if source is None:
            self.status_label.setText("Portable import package is required.")
            return
        try:
            result = self.portable_service.import_package(source, dry_run=True)
            self.status_label.setText(
                f"Package verified: {getattr(result, 'database').table_count} tables; no data was changed."
            )
        except Exception as exc:
            self.status_label.setText(f"Portable package verification failed: {exc}")

    def _on_import_package(self):
        if self._backup_worker is not None:
            return
        source = self._package_source_path()
        if source is None:
            self.status_label.setText("Portable import package is required.")
            return
        answer = QMessageBox.question(
            self,
            "Confirm portable data import",
            "Import this complete data package? The current database will first be preserved as a pre-import backup.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            self.status_label.setText("Portable import requires confirmation; no data was changed.")
            return
        self.status_label.setText("Importing package after preserving the pre-import backup...")
        self._backup_worker = DatabaseOperationWorker(
            self.portable_service,
            operation="package_import",
            restore_source=source,
            dispose_callback=self.dispose_callback,
            parent=self,
        )
        self._backup_worker.completed.connect(self._on_worker_complete)
        self._backup_worker.failed.connect(self._on_worker_failed)
        self._backup_worker.finished.connect(self._on_worker_finished)
        self._backup_worker.start()

    def _restore_source_path(self):
        text = self.restore_path_edit.text().strip()
        if text:
            return Path(text).expanduser().resolve()
        fallback = getattr(self, "_restore_source", None)
        return Path(fallback).expanduser().resolve() if fallback is not None else None

    def _package_source_path(self):
        text = self.import_package_path_edit.text().strip()
        if text:
            return Path(text).expanduser().resolve()
        fallback = getattr(self, "_import_package_source", None)
        return Path(fallback).expanduser().resolve() if fallback is not None else None

    def _on_worker_complete(self, result):
        if hasattr(result, "package") and hasattr(result, "restore"):
            self.status_label.setText(
                f"Portable import complete; pre-import backup: {result.restore.pre_restore_backup}"
            )
        elif hasattr(result, "tables") and hasattr(result, "path"):
            self.status_label.setText(
                f"Portable export complete and verified: {result.path} ({len(result.tables)} tables)"
            )
        if getattr(result, "restored", False):
            self.status_label.setText(f"Restore complete; pre-restore backup: {result.pre_restore_backup}")
        elif not (hasattr(result, "package") or hasattr(result, "tables")):
            self.status_label.setText(f"Backup complete and verified: {result.path}")

    def _on_worker_failed(self, message):
        self.status_label.setText(f"Database operation failed: {message}")

    def _on_worker_finished(self):
        self._backup_worker = None

    def _on_verified_operation(self, operation):
        operator = self.operator_edit.text().strip()
        if not operator:
            self.status_label.setText("Enter an operator before running verified maintenance.")
            return
        try:
            entry = self.maintenance_service.perform(
                operation,
                operator=operator,
                notes=self.notes_edit.toPlainText(),
            )
            self.status_label.setText(f"{entry.operation} completed and recorded as hardware work.")
        except Exception as exc:
            self.status_label.setText(f"Maintenance operation failed: {exc}")

    def _on_record_manual(self):
        operator = self.operator_edit.text().strip()
        if not operator:
            self.status_label.setText("Operator is required to record maintenance.")
            return
        operation = self.manual_operation_combo.currentData()
        try:
            entry = self.maintenance_service.record_manual_completion(
                operation,
                operator=operator,
                notes=self.notes_edit.toPlainText(),
            )
            self.status_label.setText(f"{entry.operation} recorded as operator-confirmed manual maintenance.")
        except Exception as exc:
            self.status_label.setText(f"Could not record maintenance: {exc}")

    def shutdown_for_navigation(self):
        if self._backup_worker is not None:
            self._backup_worker.quit()
            self._backup_worker.wait(2000)
            self._backup_worker = None
