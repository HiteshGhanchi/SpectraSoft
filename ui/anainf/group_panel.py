"""
SpectraSoft — Permanent Left Group Panel
Always visible. Selecting a group loads the page on the right.
Follows tkinter reference layout exactly.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QFrame,
    QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from core.database import get_session
from core.models import AnalyticalGroup
from constants import DEFAULT_GROUPS

BG = "#d4d0c8"
BTN = (
    "QPushButton{background:#d4d0c8;color:black;"
    "border:2px outset #ffffff;font:9pt Arial;padding:3px;}"
    "QPushButton:pressed{border:2px inset #888;}"
)


class GroupPanel(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(BG))
        self.setPalette(p)
        self._build_ui()
        self._load()
        
    def _launch_runner(self):
        from ui.analysis.runner import RunnerDashboard
        # The runner dashboard takes over the ENTIRE window, so we replace the central layout
        runner = RunnerDashboard(self.main_window)
        # Fix applied here: Use the new toggle function!
        self.main_window.set_left_panel_visible(False) 
        self.main_window.set_right_widget(runner)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(4, 4, 4, 4)
        root.setSpacing(4)

        # ── "Analytical Group Information" label ──────────────────────
        title = QLabel("Analytical Group Information")
        title.setFont(QFont("Arial", 9))
        title.setStyleSheet(f"background:{BG};color:black;")
        root.addWidget(title)

        # ── Raised bordered panel (matching tkinter left_panel) ───────
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.Box)
        panel.setFrameShadow(QFrame.Shadow.Raised)
        panel.setLineWidth(2)
        panel.setStyleSheet(f"background:{BG};")

        pl = QVBoxLayout(panel)
        pl.setContentsMargins(8, 6, 8, 8)
        pl.setSpacing(4)

        # "Analytical Group" header
        hdr = QLabel("Analytical Group")
        hdr.setFont(QFont("Arial", 9))
        hdr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.setStyleSheet(f"background:{BG};color:black;")
        pl.addWidget(hdr)

        # Listbox
        self._list = QListWidget()
        self._list.setFont(QFont("Arial", 9))
        self._list.setStyleSheet(
            "QListWidget{background:white;color:black;border:1px solid #aaa;}"
            "QListWidget::item{padding:1px 2px;color:black;}"
            "QListWidget::item:selected{background:#0078d7;color:white;}"
        )
        self._list.itemDoubleClicked.connect(self._on_select)
        pl.addWidget(self._list)

        # --- THE ORIGINAL BUTTONS ---
        for label, slot in [
            ("1:Select",        self._on_select),
            ("2:Detail",        self._on_detail),
            ("3:Arrange",       self._on_arrange),
            ("5:New",           self._on_new),
            ("8:Delete",        self._on_delete),
            ("9:WC Coef. Copy", self._on_wc_copy),
        ]:
            b = QPushButton(label)
            b.setStyleSheet(
                "QPushButton{background:#d4d0c8;color:black;border:2px outset #ffffff;"
                "font:9pt Arial;padding:3px 8px;min-width:65px;}"
                "QPushButton:pressed{border:2px inset #888;}"
            )
            b.clicked.connect(slot)
            pl.addWidget(b)

        # Add the panel to the main layout
        root.addWidget(panel)

        # --- THE NEW RUN ANALYSIS BUTTON (Outside the loop!) ---
        btn_run = QPushButton("RUN ANALYSIS MODE")
        btn_run.setStyleSheet("background: #0078d7; color: white; font: bold 10pt Arial; padding: 10px;")
        btn_run.clicked.connect(self._launch_runner)
        root.addWidget(btn_run)


    def _load(self):
        session = get_session()
        try:
            groups = session.query(AnalyticalGroup).order_by(
                AnalyticalGroup.display_order, AnalyticalGroup.id).all()
            if not groups:
                for i, name in enumerate(DEFAULT_GROUPS):
                    session.add(AnalyticalGroup(name=name, display_order=i))
                session.commit()
                groups = session.query(AnalyticalGroup).order_by(
                    AnalyticalGroup.display_order).all()
            self._list.clear()
            for g in groups:
                item = QListWidgetItem(g.name)
                item.setData(Qt.ItemDataRole.UserRole, g.id)
                self._list.addItem(item)
            if self._list.count() > 0:
                self._list.setCurrentRow(0)
        finally:
            session.close()

    def _selected(self):
        item = self._list.currentItem()
        if item:
            return item.data(Qt.ItemDataRole.UserRole), item.text()
        return None, None

    def highlight(self, group_id: int):
        """Highlight the given group in the list (called by pages)."""
        for i in range(self._list.count()):
            item = self._list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == group_id:
                self._list.setCurrentRow(i)
                break

    # ------------------------------------------------------------------
    def _on_select(self):
        gid, name = self._selected()
        if gid is None:
            QMessageBox.warning(self, "Warning", "Please select a group first.")
            return
        from ui.anainf.page_01_condition import AnalyticalConditionPage
        self.main_window.set_right_widget(
            AnalyticalConditionPage(self.main_window, gid, name))

    def _on_detail(self):
        gid, name = self._selected()
        if gid is None:
            QMessageBox.warning(self, "Warning", "Please select a group first.")
            return
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, gid)
            cond = g.page_01_condition or {}
            QMessageBox.information(self, "Group Detail",
                f"<b>{name}</b><br><br>"
                f"Method: {cond.get('analytical_method','—')}<br>"
                f"Purge Seq1: {cond.get('purge_seq1','—')} sec<br>"
                f"Source Seq1: {cond.get('source_seq1','—')}<br>"
                f"Source Seq2: {cond.get('source_seq2','—')}")
        finally:
            session.close()

    def _on_arrange(self):
        QMessageBox.information(self, "Arrange",
            "Reordering available in next update.")

    def _on_new(self):
        name, ok = QInputDialog.getText(self, "New Group", "Enter group name:")
        if not ok or not name.strip():
            return
        name = name.strip()
        session = get_session()
        try:
            if session.query(AnalyticalGroup).filter_by(name=name).first():
                QMessageBox.warning(self, "Duplicate", f"'{name}' already exists.")
                return
            g = AnalyticalGroup(name=name,
                                display_order=session.query(AnalyticalGroup).count())
            session.add(g)
            session.commit()
            session.refresh(g)
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, g.id)
            self._list.addItem(item)
            self._list.setCurrentItem(item)
        finally:
            session.close()

    def _on_delete(self):
        gid, name = self._selected()
        if gid is None:
            QMessageBox.warning(self, "Warning", "Please select a group first.")
            return
        if QMessageBox.question(
            self, "Delete", f"Delete '{name}'? Cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, gid)
            if g:
                session.delete(g)
                session.commit()
            self._list.takeItem(self._list.currentRow())
            self.main_window._show_home_content()
        finally:
            session.close()

    def _on_wc_copy(self):
        gid, name = self._selected()
        if gid is None:
            QMessageBox.warning(self, "Warning", "Please select a source group first.")
            return
        session = get_session()
        try:
            dest_names = [g.name for g in
                          session.query(AnalyticalGroup).order_by(
                              AnalyticalGroup.display_order).all()
                          if g.id != gid]
        finally:
            session.close()
        if not dest_names:
            QMessageBox.information(self, "WC Coef. Copy", "No other groups.")
            return
        dest_name, ok = QInputDialog.getItem(
            self, "WC Coef. Copy",
            f"Copy WC coefficients FROM '{name}' TO:", dest_names, 0, False)
        if not ok:
            return
        session = get_session()
        try:
            src = session.get(AnalyticalGroup, gid)
            dst = session.query(AnalyticalGroup).filter_by(name=dest_name).first()
            if src and dst:
                dst.page_07_working_curve = src.page_07_working_curve
                session.commit()
                QMessageBox.information(self, "Done",
                    f"Copied from '{name}' to '{dest_name}'.")
        finally:
            session.close()