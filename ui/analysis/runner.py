from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSplitter, QMessageBox,
    QLineEdit, QDialog, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

from core.database import get_session
from core.models import AnalyticalGroup

BG = "#d4d0c8"
BTN = ("QPushButton{background:#d4d0c8;color:black;border:2px outset #ffffff;"
       "font:bold 9pt Arial;padding:5px 8px;min-width:65px;}"
       "QPushButton:pressed{border:2px inset #888;}"
       "QPushButton:disabled{color:#888; border:2px solid #ccc;}")

class GroupSelectionDialog(QDialog):
    """Popup dialog triggered by S4:Group to pick a technique from the database."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Analytical Group")
        self.setFixedSize(300, 400)
        self.setStyleSheet(f"background:{BG}; color:black; font:9pt Arial;")
        self.selected_group_id = None
        self.selected_group_name = None
        
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background:white; color:black; border:1px solid #aaa;")
        layout.addWidget(self.list_widget)

        # Load groups from Database
        session = get_session()
        try:
            groups = session.query(AnalyticalGroup).order_by(AnalyticalGroup.id).all()
            for g in groups:
                item = QListWidgetItem(f"{g.id} - {g.name}")
                item.setData(Qt.ItemDataRole.UserRole, (g.id, g.name))
                self.list_widget.addItem(item)
        finally:
            session.close()

        self.list_widget.itemDoubleClicked.connect(self.accept_selection)

        btn_layout = QHBoxLayout()
        btn_select = QPushButton("1:Select")
        btn_select.setStyleSheet(BTN)
        btn_select.clicked.connect(self.accept_selection)
        
        btn_cancel = QPushButton("9:Cancel")
        btn_cancel.setStyleSheet(BTN)
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_select)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

    def accept_selection(self):
        item = self.list_widget.currentItem()
        if item:
            self.selected_group_id, self.selected_group_name = item.data(Qt.ItemDataRole.UserRole)
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please select a group first.")


class RunnerDashboard(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_group_id = None
        self.current_group_name = None
        
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(BG))
        self.setPalette(p)
        
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(5, 5, 5, 5)
        root.setSpacing(5)

        # --- 1. TOP BUTTON ROW (S1 - S12) ---
        top_btn_layout = QHBoxLayout()
        top_btn_layout.setSpacing(2)
        top_buttons = [
            "S1:Next", "S2:Add", "S3:Mode", "S4:Group", "S5:Cancel", "S6:End", 
            "S7:Reset", "S8:Modify", "S9:Freq", "S10:Print", "S11:Round", "S12:Alloy"
        ]
        self.top_btns = {}
        for txt in top_buttons:
            btn = QPushButton(txt)
            btn.setStyleSheet(BTN)
            top_btn_layout.addWidget(btn)
            self.top_btns[txt.split(":")[0]] = btn # Store by S1, S2, etc.
            
        # Hook up S4
        self.top_btns["S4"].clicked.connect(self._on_s4_group_clicked)
        root.addLayout(top_btn_layout)

        # --- 2. MAIN DISPLAY AREA (Splitter) ---
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left Side (Will hold the Results Table)
        self.left_display = QFrame()
        self.left_display.setFrameShape(QFrame.Shape.Box)
        self.left_display.setFrameShadow(QFrame.Shadow.Sunken)
        self.left_display.setStyleSheet("background: white;")
        left_layout = QVBoxLayout(self.left_display)
        lbl_results = QLabel("Results Table (Pending Step 5)")
        lbl_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_results.setStyleSheet("color: #aaa; font: 14pt Arial;")
        left_layout.addWidget(lbl_results)
        
        # Right Side (Will hold Stats/Graph)
        self.right_display = QFrame()
        self.right_display.setFrameShape(QFrame.Shape.Box)
        self.right_display.setFrameShadow(QFrame.Shadow.Sunken)
        self.right_display.setStyleSheet("background: #e8e8e8;")
        right_layout = QVBoxLayout(self.right_display)
        lbl_stats = QLabel("Statistics / Graph (Pending Step 5)")
        lbl_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_stats.setStyleSheet("color: #aaa; font: 14pt Arial;")
        right_layout.addWidget(lbl_stats)

        self.splitter.addWidget(self.left_display)
        self.splitter.addWidget(self.right_display)
        self.splitter.setSizes([600, 300]) # 66% / 33% split roughly
        root.addWidget(self.splitter, stretch=1)

        # --- 3. STATUS BAR ---
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.Shape.Panel)
        status_frame.setFrameShadow(QFrame.Shadow.Raised)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(5, 2, 5, 2)
        
        # Indicators D P F CT N
        ind_layout = QHBoxLayout()
        ind_layout.setSpacing(2)
        for letter in ["D", "P", "F", "CT", "N"]:
            lbl = QLabel(letter)
            lbl.setFixedSize(20, 20)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("background: #aaa; color: black; border: 1px solid #666; font: bold 8pt Arial;")
            ind_layout.addWidget(lbl)
        status_layout.addLayout(ind_layout)
        status_layout.addSpacing(20)

        # Group Info
        status_layout.addWidget(QLabel("Group:"))
        self.ui_group_name = QLineEdit("No Group Selected")
        self.ui_group_name.setReadOnly(True)
        self.ui_group_name.setFixedWidth(200)
        self.ui_group_name.setStyleSheet("background: #ddd; color: black; border: 1px solid #aaa; font: bold 9pt Arial;")
        status_layout.addWidget(self.ui_group_name)
        status_layout.addStretch()

        # AN / TAN Counters
        status_layout.addWidget(QLabel("AN:"))
        self.ui_an = QLineEdit("0")
        self.ui_an.setReadOnly(True)
        self.ui_an.setFixedWidth(40)
        self.ui_an.setStyleSheet("background: black; color: #0f0; font: bold 10pt Arial;")
        self.ui_an.setAlignment(Qt.AlignmentFlag.AlignRight)
        status_layout.addWidget(self.ui_an)
        
        status_layout.addWidget(QLabel("TAN:"))
        self.ui_tan = QLineEdit("0")
        self.ui_tan.setReadOnly(True)
        self.ui_tan.setFixedWidth(40)
        self.ui_tan.setStyleSheet("background: black; color: #0f0; font: bold 10pt Arial;")
        self.ui_tan.setAlignment(Qt.AlignmentFlag.AlignRight)
        status_layout.addWidget(self.ui_tan)
        
        root.addWidget(status_frame)

        # --- 4. BOTTOM BUTTON ROW (1 - 12) ---
        bot_btn_layout = QHBoxLayout()
        bot_btn_layout.setSpacing(2)
        bot_buttons = [
            "1:Start", "2:Stop", "3:Charge", "4:Print", "5:File", "6:Trans", 
            "7:Cal", "8:Init", "9:Recycle", "10:Recal", "11:Master", "12:Quit"
        ]
        self.bot_btns = {}
        for txt in bot_buttons:
            btn = QPushButton(txt)
            btn.setStyleSheet(BTN)
            bot_btn_layout.addWidget(btn)
            self.bot_btns[txt.split(":")[0]] = btn # Store by 1, 2, etc.

        # Initially disable Start and Recal until a group is selected
        self.bot_btns["1"].setEnabled(False)
        self.bot_btns["10"].setEnabled(False)

        # Hook up essential bottom buttons
        self.bot_btns["1"].clicked.connect(self._on_start_clicked)
        self.bot_btns["12"].clicked.connect(self._on_quit_clicked)
        
        root.addLayout(bot_btn_layout)

    # --- FUNCTIONAL HOOKS ---

    def _on_s4_group_clicked(self):
        """Opens the database dialog to select an analytical technique."""
        dialog = GroupSelectionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.current_group_id = dialog.selected_group_id
            self.current_group_name = dialog.selected_group_name
            
            # Update Status Bar
            self.ui_group_name.setText(f"{self.current_group_id} - {self.current_group_name}")
            self.ui_group_name.setStyleSheet("background: white; color: black; border: 1px solid #aaa; font: bold 9pt Arial;")
            
            # Unlock the hardware run buttons!
            self.bot_btns["1"].setEnabled(True)
            self.bot_btns["10"].setEnabled(True)

    def _on_start_clicked(self):
        """Placeholder for Step 3: Background Threading."""
        QMessageBox.information(self, "Analysis Started", 
            f"Ready to run group '{self.current_group_name}'!\n\n"
            "In Step 3, this button will lock the UI and start the QThread to run the hardware.")

    def _on_quit_clicked(self):
        """Safely returns the user to the AnaInf offline editor."""
        reply = QMessageBox.question(self, "Quit Analysis", 
            "Are you sure you want to return to the Offline Editor?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
        if reply == QMessageBox.StandardButton.Yes:
            # Fix applied here: Use the toggle to bring the menu back
            self.main_window.set_left_panel_visible(True)
            self.main_window._show_home_content()