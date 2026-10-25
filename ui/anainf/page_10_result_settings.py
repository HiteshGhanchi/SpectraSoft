"""Result, product-limit, and repeated-burn calculation settings."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QTableWidget, QTableWidgetItem, QCheckBox,
    QLineEdit, QMessageBox, QAbstractItemView,
)

from core.persistence.database import get_session
from core.persistence.models import (
    AnalyticalGroup,
    ProductSpecification,
    RControlSetting,
    ResultCalculationSetting,
)


class ResultSettingsPage(QWidget):
    """Stores product limits, R-control coefficients, and optional switches."""

    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self._build_ui()
        self._load()

    def _build_ui(self):
        root = QVBoxLayout(self)
        title = QLabel(f"Result and Calculation Settings - {self.group_name}")
        title.setStyleSheet("background:#5c9bd5;color:white;font:bold 10pt Arial;padding:5px;")
        root.addWidget(title)
        self.tabs = QTabWidget()

        product = QWidget()
        product_layout = QVBoxLayout(product)
        self.product_table = QTableWidget(0, 6)
        self.product_table.setHorizontalHeaderLabels([
            "Product", "Element", "Lower", "Upper", "Trace", "Delete",
        ])
        product_layout.addWidget(self.product_table)
        product_buttons = QHBoxLayout()
        add_product = QPushButton("Add Product Limit")
        add_product.clicked.connect(self._add_product_row)
        product_buttons.addWidget(add_product)
        product_buttons.addStretch()
        product_layout.addLayout(product_buttons)
        self.tabs.addTab(product, "Product Specifications")

        r_control = QWidget()
        r_layout = QVBoxLayout(r_control)
        self.r_table = QTableWidget(0, 5)
        self.r_table.setHorizontalHeaderLabels(["Element", "A", "B", "C", "Delete"])
        r_layout.addWidget(self.r_table)
        r_buttons = QHBoxLayout()
        add_r = QPushButton("Add R-Control Row")
        add_r.clicked.connect(self._add_r_row)
        r_buttons.addWidget(add_r)
        r_buttons.addStretch()
        r_layout.addLayout(r_buttons)
        self.tabs.addTab(r_control, "R Control")

        optional = QWidget()
        optional_layout = QVBoxLayout(optional)
        self.normalization_check = QCheckBox("Enable optional 100% / virtual-composition correction")
        self.skip_points_edit = QLineEdit()
        self.skip_points_edit.setPlaceholderText("Optional channel skip points, e.g. FE=0.0; C=0.0")
        optional_layout.addWidget(self.normalization_check)
        optional_layout.addWidget(QLabel("Channel skip points:"))
        optional_layout.addWidget(self.skip_points_edit)
        optional_layout.addWidget(QLabel(
            "The scientific 100% conversion formula remains method-defined; this screen only stores the operator switch and skip-point data."
        ))
        optional_layout.addStretch()
        self.tabs.addTab(optional, "Optional Calculations")
        root.addWidget(self.tabs, stretch=1)

        buttons = QHBoxLayout()
        save = QPushButton("Save")
        save.clicked.connect(self._save)
        buttons.addWidget(save)
        previous = QPushButton("Previous")
        previous.clicked.connect(self._on_previous)
        buttons.addWidget(previous)
        buttons.addStretch()
        root.addLayout(buttons)

    def _load(self):
        session = get_session()
        try:
            products = session.query(ProductSpecification).filter_by(
                analytical_group_id=self.group_id
            ).order_by(ProductSpecification.product_name, ProductSpecification.element_key).all()
            self.product_table.setRowCount(0)
            for row in products:
                self._add_product_row(row)

            r_rows = session.query(RControlSetting).filter_by(
                analytical_group_id=self.group_id
            ).order_by(RControlSetting.element_key).all()
            self.r_table.setRowCount(0)
            for row in r_rows:
                self._add_r_row(row)

            settings = session.query(ResultCalculationSetting).filter_by(
                analytical_group_id=self.group_id
            ).one_or_none()
            data = settings.settings if settings else {}
            self.normalization_check.setChecked(bool(data.get("normalization_enabled", False)))
            self.skip_points_edit.setText(str(data.get("skip_points", "")))
        finally:
            session.close()

    def _set_cell(self, table, row, column, value):
        table.setItem(row, column, QTableWidgetItem(str(value)))

    def _add_product_row(self, record=None):
        row = self.product_table.rowCount()
        self.product_table.insertRow(row)
        values = [
            getattr(record, "product_name", "") if record else "",
            getattr(record, "element_key", "") if record else "",
            getattr(record, "lower_limit", "") if record else "",
            getattr(record, "upper_limit", "") if record else "",
            getattr(record, "trace_limit", "") if record else "",
            "",
        ]
        for column, value in enumerate(values):
            self._set_cell(self.product_table, row, column, value)

    def _add_r_row(self, record=None):
        row = self.r_table.rowCount()
        self.r_table.insertRow(row)
        values = [
            getattr(record, "element_key", "") if record else "",
            getattr(record, "a", 0.0) if record else 0.0,
            getattr(record, "b", 0.0) if record else 0.0,
            getattr(record, "c", 0.0) if record else 0.0,
            "",
        ]
        for column, value in enumerate(values):
            self._set_cell(self.r_table, row, column, value)

    def _text(self, table, row, column):
        item = table.item(row, column)
        return item.text().strip() if item else ""

    def _save(self):
        session = get_session()
        try:
            session.query(ProductSpecification).filter_by(
                analytical_group_id=self.group_id
            ).delete(synchronize_session=False)
            for row in range(self.product_table.rowCount()):
                product = self._text(self.product_table, row, 0)
                element = self._text(self.product_table, row, 1).upper()
                if not product or not element:
                    continue
                session.add(ProductSpecification(
                    analytical_group_id=self.group_id,
                    product_name=product,
                    element_key=element,
                    lower_limit=float(self._text(self.product_table, row, 2)) if self._text(self.product_table, row, 2) else None,
                    upper_limit=float(self._text(self.product_table, row, 3)) if self._text(self.product_table, row, 3) else None,
                    trace_limit=float(self._text(self.product_table, row, 4)) if self._text(self.product_table, row, 4) else None,
                ))

            session.query(RControlSetting).filter_by(
                analytical_group_id=self.group_id
            ).delete(synchronize_session=False)
            for row in range(self.r_table.rowCount()):
                element = self._text(self.r_table, row, 0).upper()
                if not element:
                    continue
                session.add(RControlSetting(
                    analytical_group_id=self.group_id,
                    element_key=element,
                    a=float(self._text(self.r_table, row, 1) or 0),
                    b=float(self._text(self.r_table, row, 2) or 0),
                    c=float(self._text(self.r_table, row, 3) or 0),
                ))

            settings = session.query(ResultCalculationSetting).filter_by(
                analytical_group_id=self.group_id
            ).one_or_none()
            if settings is None:
                settings = ResultCalculationSetting(analytical_group_id=self.group_id)
                session.add(settings)
            settings.settings = {
                "normalization_enabled": self.normalization_check.isChecked(),
                "skip_points": self.skip_points_edit.text().strip(),
            }
            session.commit()
        except (TypeError, ValueError) as error:
            session.rollback()
            QMessageBox.warning(self, "Invalid Settings", str(error))
            return
        finally:
            session.close()
        QMessageBox.information(self, "Saved", "Result and calculation settings saved.")

    def _on_previous(self):
        from ui.anainf.page_09_purity import PurityCalculationPage

        self._save()
        self.main_window.set_right_widget(
            PurityCalculationPage(self.main_window, self.group_id, self.group_name)
        )
