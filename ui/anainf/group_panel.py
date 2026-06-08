"""
SpectraSoft — Permanent Left Group Panel
Always visible. Selecting a group loads the page on the right.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QFrame,
    QInputDialog, QMessageBox
)
from PyQt6.QtCore import Qt

from core.database import get_session
from core.models import AnalyticalGroup
from ui.ui_theme import Colors, Stylesheets, Spacing, Fonts, get_font, get_color


class GroupPanel(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), get_color(Colors.BG_MAIN))
        self.setPalette(p)
        self._build_ui()
        self._load()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(Spacing.PADDING_NORMAL, Spacing.PADDING_NORMAL,
                               Spacing.PADDING_NORMAL, Spacing.PADDING_NORMAL)
        root.setSpacing(Spacing.PADDING_NORMAL)

        title = QLabel("Analytical Group Information")
        title.setFont(get_font())
        title.setStyleSheet(Stylesheets.LABEL_NORMAL)
        root.addWidget(title)

        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.Box)
        panel.setFrameShadow(QFrame.Shadow.Raised)
        panel.setLineWidth(2)
        panel.setStyleSheet(Stylesheets.PANEL_MAIN)

        pl = QVBoxLayout(panel)
        pl.setContentsMargins(Spacing.PADDING_LARGE, 6,
                              Spacing.PADDING_LARGE, Spacing.PADDING_LARGE)
        pl.setSpacing(Spacing.PADDING_NORMAL)

        hdr = QLabel("Analytical Group")
        hdr.setFont(get_font())
        hdr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.setStyleSheet(Stylesheets.LABEL_NORMAL)
        pl.addWidget(hdr)

        # List with drag-and-drop reordering
        self._list = QListWidget()
        self._list.setFont(get_font())
        self._list.setStyleSheet(
            f"QListWidget{{"
            f"background:{Colors.BG_WHITE};"
            f"color:{Colors.TEXT_BLACK};"
            f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_LIGHT};"
            f"}}"
            f"QListWidget::item{{padding:1px 2px;color:{Colors.TEXT_BLACK};}}"
            f"QListWidget::item:selected{{"
            f"background:{Colors.ACCENT_PRIMARY};"
            f"color:{Colors.TEXT_WHITE};"
            f"}}"
        )
        self._list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self._list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self._list.model().rowsMoved.connect(self._on_rows_moved)
        self._list.itemDoubleClicked.connect(self._on_open)
        pl.addWidget(self._list)

        # Buttons: New, Delete, WC Coef. Copy
        for label, slot in [
            ("New",           self._on_new),
            ("Delete",        self._on_delete),
            ("WC Coef. Copy", self._on_wc_copy),
        ]:
            btn = QPushButton(label)
            btn.setStyleSheet(Stylesheets.BUTTON_NORMAL)
            btn.clicked.connect(slot)
            pl.addWidget(btn)

        root.addWidget(panel)

        # No large RUN ANALYSIS MODE button – removed

    def _load(self):
        session = get_session()
        try:
            groups = session.query(AnalyticalGroup).order_by(
                AnalyticalGroup.display_order, AnalyticalGroup.id).all()
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
        for i in range(self._list.count()):
            item = self._list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == group_id:
                self._list.setCurrentRow(i)
                break

    def _on_rows_moved(self):
        """Save new display order after drag-and-drop."""
        session = get_session()
        try:
            for i in range(self._list.count()):
                item = self._list.item(i)
                gid = item.data(Qt.ItemDataRole.UserRole)
                g = session.get(AnalyticalGroup, gid)
                if g:
                    g.display_order = i
            session.commit()
        finally:
            session.close()

    def _on_open(self):
        """Double-click opens the group pages."""
        gid, name = self._selected()
        if gid is None:
            return
        from ui.anainf.page_01_condition import AnalyticalConditionPage
        self.main_window.set_right_widget(
            AnalyticalConditionPage(self.main_window, gid, name))

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
            g = AnalyticalGroup(
                name=name,
                display_order=session.query(AnalyticalGroup).count()
            )
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
            dest_names = [
                g.name for g in session.query(AnalyticalGroup).order_by(
                    AnalyticalGroup.display_order).all()
                if g.id != gid
            ]
        finally:
            session.close()
        if not dest_names:
            QMessageBox.information(self, "WC Coef. Copy", "No other groups to copy to.")
            return
        dest_name, ok = QInputDialog.getItem(
            self, "WC Coef. Copy",
            f"Copy WC coefficients FROM '{name}' TO:",
            dest_names, 0, False
        )
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
                    f"Copied WC coefficients from '{name}' to '{dest_name}'.")
        finally:
            session.close()