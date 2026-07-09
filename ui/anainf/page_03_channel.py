"""
SpectraSoft — Page 3: Order of Analytical Channel & Internal Standard

Simple stable version with debug logging.

This page maps hardware channels (ITG) to analytical records, assigns sequences,
and selects the Internal Standard Element (ISE) reference for each element.

Columns:
- AR-No.: Auto-numbered 1 to 32
- ITG: Integrator number from Master Elements table
- ELE: Element name auto-filled from selected ITG
- NAME: User-defined report/display name, up to 5 chars
- SEQ: Sequence assignment, 1, 2, or 3
- ISE Ref: Internal Standard reference
    0 = no internal standard
    1-45 = ITG number of reference element

Important:
- No hardcoded Master Elements are used.
- If Master Elements is empty, ITG dropdowns remain empty.
- W-No / Working Number is intentionally not implemented.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QScrollArea,
    QMessageBox, QComboBox, QLineEdit
)
from PyQt6.QtCore import Qt, QSignalBlocker

from core.database import get_session
from core.models import AnalyticalGroup, MasterElement


MAX_ELEMENTS = 32


class ChannelPage(QWidget):

    def __init__(self, main_window, group_id: int, group_name: str):
        # print("[PAGE3 DEBUG] ChannelPage __init__ started.", flush=True)

        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name

        # print(
        #     f"[PAGE3 DEBUG] group_id={self.group_id}, group_name={self.group_name}",
        #     flush=True
        # )

        # Load Master Elements once only.
        # print("[PAGE3 DEBUG] Loading Master Elements cache...", flush=True)
        self._itg_to_ele = self._load_itg_element_map()
        # print(
        #     f"[PAGE3 DEBUG] Master Elements cache loaded: {len(self._itg_to_ele)} entries.",
        #     flush=True
        # )

        # Holds widgets row-wise
        self._rows = []

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        # print("[PAGE3 DEBUG] Building UI...", flush=True)
        self._build_ui()
        # print("[PAGE3 DEBUG] UI built successfully.", flush=True)

        # print("[PAGE3 DEBUG] Loading saved Page 3 data...", flush=True)
        self._load()
        # print("[PAGE3 DEBUG] ChannelPage __init__ completed.", flush=True)

    # =========================================================================
    # Master Element Cache
    # =========================================================================

    def _load_itg_element_map(self) -> dict:
        """
        Load Master Elements once.

        Empty element names are ignored because they represent unused channels.
        """
        # print("[PAGE3 DEBUG] _load_itg_element_map() started.", flush=True)

        session = get_session()
        try:
            rows = session.query(MasterElement).order_by(
                MasterElement.itg_no
            ).all()

            result = {
                str(r.itg_no): (r.ele_name or "").strip()
                for r in rows
                if r.ele_name and r.ele_name.strip()
            }

            # print(
            #     f"[PAGE3 DEBUG] _load_itg_element_map() found {len(result)} usable channels.",
            #     flush=True
            # )

            return result

        finally:
            session.close()
            # print("[PAGE3 DEBUG] _load_itg_element_map() session closed.", flush=True)

    def _build_itg_options(self) -> list:
        """
        Build ITG dropdown options from cached Master Elements only.
        No hardcoded fallback.
        """
        opts = [
            (f"{itg}: {ele}", itg)
            for itg, ele in self._itg_to_ele.items()
        ]

        # print(f"[PAGE3 DEBUG] Built {len(opts)} ITG options.", flush=True)
        return opts

    def _build_ise_options(self) -> list:
        """
        Build ISE dropdown options.

        0 is always available.
        Other values come from cached Master Elements only.
        """
        opts = [("0 (none)", 0)]

        for itg, ele in self._itg_to_ele.items():
            opts.append((f"{itg}: {ele}", int(itg)))

        # print(f"[PAGE3 DEBUG] Built {len(opts)} ISE options.", flush=True)
        return opts

    # =========================================================================
    # UI
    # =========================================================================

    def _build_ui(self):
        # print("[PAGE3 DEBUG] _build_ui() started.", flush=True)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar ──────────────────────────────────────────────────────
        self.title_bar = QLabel(f"Element Information - CH 0 - {self.group_name}")
        self.title_bar.setFixedHeight(24)
        self.title_bar.setContentsMargins(12, 0, 0, 0)
        self.title_bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.title_bar.setStyleSheet(
            "background:#5c9bd5;"
            "color:white;"
            "font:bold 10pt Arial;"
        )
        root.addWidget(self.title_bar)

        # ── Outer Frame ────────────────────────────────────────────────────
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:white;")
        root.addWidget(outer, stretch=1)

        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")
        outer_layout.addWidget(scroll)

        inner = QWidget()
        inner.setStyleSheet("background:#d4d0c8;")
        scroll.setWidget(inner)

        main_layout = QVBoxLayout(inner)
        main_layout.setContentsMargins(20, 16, 20, 12)
        main_layout.setSpacing(8)

        # ── Page Title ─────────────────────────────────────────────────────
        page_title = QLabel("ORDER OF ANALYTICAL CHANNEL & INTERNAL STANDARD")
        page_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        page_title.setStyleSheet(
            "QLabel{"
            "background:#d4d0c8;"
            "color:black;"
            "font:bold 10pt Arial;"
            "border:1px solid #888888;"
            "padding:4px;"
            "}"
        )
        main_layout.addWidget(page_title)

        # ── Grid Frame ─────────────────────────────────────────────────────
        grid_frame = QFrame()
        grid_frame.setStyleSheet(
            "QFrame{"
            "background:white;"
            "border:1px solid #888888;"
            "}"
        )

        grid = QGridLayout(grid_frame)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)

        widths = {
            0: 55,     # AR-No.
            1: 130,    # ITG
            2: 70,     # ELE
            3: 85,     # NAME
            4: 60,     # SEQ
            5: 120,    # ISE Ref
        }

        headers = ["AR-No.", "ITG", "ELE", "NAME", "SEQ", "ISE Ref"]

        # print("[PAGE3 DEBUG] Creating header row...", flush=True)

        for col, text in enumerate(headers):
            lbl = QLabel(text)
            lbl.setFixedSize(widths[col], 27)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(self._header_style())
            grid.addWidget(lbl, 0, col)

        # print("[PAGE3 DEBUG] Building dropdown options...", flush=True)
        itg_options = self._build_itg_options()
        ise_options = self._build_ise_options()

        # print("[PAGE3 DEBUG] Creating 32 rows...", flush=True)

        for row in range(MAX_ELEMENTS):
            ar_no = row + 1

            # AR-No.
            ar_lbl = QLabel(str(ar_no))
            ar_lbl.setFixedSize(widths[0], 27)
            ar_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ar_lbl.setStyleSheet(self._readonly_style())
            grid.addWidget(ar_lbl, row + 1, 0)

            # ITG combo
            itg_combo = QComboBox()
            itg_combo.setFixedSize(widths[1], 27)
            itg_combo.addItem("", "")

            for display, value in itg_options:
                itg_combo.addItem(display, value)

            itg_combo.setStyleSheet(self._combo_style())
            itg_combo.currentIndexChanged.connect(
                lambda idx, r=row: self._on_itg_changed(r)
            )
            grid.addWidget(itg_combo, row + 1, 1)

            # ELE label
            ele_lbl = QLabel("")
            ele_lbl.setFixedSize(widths[2], 27)
            ele_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ele_lbl.setStyleSheet(self._readonly_style())
            grid.addWidget(ele_lbl, row + 1, 2)

            # NAME edit
            name_edit = QLineEdit()
            name_edit.setFixedSize(widths[3], 27)
            name_edit.setMaxLength(5)
            name_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_edit.setStyleSheet(self._edit_style())
            grid.addWidget(name_edit, row + 1, 3)

            # SEQ combo
            seq_combo = QComboBox()
            seq_combo.setFixedSize(widths[4], 27)
            seq_combo.addItems(["", "1", "2", "3"])
            seq_combo.setStyleSheet(self._combo_style())
            grid.addWidget(seq_combo, row + 1, 4)

            # ISE combo
            ise_combo = QComboBox()
            ise_combo.setFixedSize(widths[5], 27)

            for display, value in ise_options:
                ise_combo.addItem(display, value)

            ise_combo.setStyleSheet(self._combo_style())
            grid.addWidget(ise_combo, row + 1, 5)

            self._rows.append({
                "ar": ar_lbl,
                "itg": itg_combo,
                "ele": ele_lbl,
                "name": name_edit,
                "seq": seq_combo,
                "ise": ise_combo,
            })

        # print(f"[PAGE3 DEBUG] Created {len(self._rows)} rows.", flush=True)

        # Center grid
        grid_wrapper = QHBoxLayout()
        grid_wrapper.addStretch()
        grid_wrapper.addWidget(grid_frame)
        grid_wrapper.addStretch()

        main_layout.addLayout(grid_wrapper)

        # ── Info / Clear Row ──────────────────────────────────────────────
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(6)

        btn_clear = QPushButton("Clear All")
        btn_clear.setStyleSheet(self._button_style())
        btn_clear.clicked.connect(self._on_clear)
        ctrl_layout.addWidget(btn_clear)

        ctrl_layout.addStretch()

        info_lbl = QLabel(
            "ISE Ref: 0 = No internal standard. Select an ITG number to ratio against."
        )
        info_lbl.setStyleSheet(
            "QLabel{"
            "color:#666666;"
            "font:9pt Arial;"
            "border:none;"
            "background:#d4d0c8;"
            "}"
        )
        ctrl_layout.addWidget(info_lbl)

        main_layout.addLayout(ctrl_layout)
        main_layout.addStretch()

        # ── Bottom Navigation ─────────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        btn_bar.setStyleSheet("background:#d4d0c8;")

        nav = QHBoxLayout(btn_bar)
        nav.setContentsMargins(12, 4, 12, 8)
        nav.setSpacing(4)

        for text, slot in [
            ("1:OK", self._on_ok),
            ("2:Next", self._on_next),
            ("3:Pre.", self._on_pre),
            ("4:Print", self._on_print),
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(self._button_style())
            btn.clicked.connect(slot)
            nav.addWidget(btn)

        nav.addStretch()

        cancel_btn = QPushButton("9:Cancel")
        cancel_btn.setStyleSheet(self._button_style())
        cancel_btn.clicked.connect(self._on_cancel)
        nav.addWidget(cancel_btn)

        root.addWidget(btn_bar)

        # print("[PAGE3 DEBUG] _build_ui() completed.", flush=True)

    # =========================================================================
    # Styles
    # =========================================================================

    def _header_style(self) -> str:
        return (
            "QLabel{"
            "background:#0078d7;"
            "color:white;"
            "font:bold 9pt Arial;"
            "border:1px solid #888888;"
            "padding:2px;"
            "}"
        )

    def _readonly_style(self) -> str:
        return (
            "QLabel{"
            "background:#d4d0c8;"
            "color:black;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:1px;"
            "}"
        )

    def _edit_style(self) -> str:
        return (
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:1px 2px;"
            "}"
        )

    def _combo_style(self) -> str:
        return (
            "QComboBox{"
            "background:white;"
            "color:black;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:1px 2px;"
            "}"
            "QComboBox QAbstractItemView{"
            "background:white;"
            "color:black;"
            "selection-background-color:#0078d7;"
            "selection-color:white;"
            "}"
        )

    def _button_style(self) -> str:
        return (
            "QPushButton{"
            "background:#d4d0c8;"
            "color:black;"
            "border:2px outset #aaaaaa;"
            "font:9pt Arial;"
            "padding:4px 12px;"
            "min-width:60px;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )

    # =========================================================================
    # Events
    # =========================================================================

    def _on_itg_changed(self, row_index: int):
        """Auto-fill ELE from cached ITG map."""
        # print(f"[PAGE3 DEBUG] _on_itg_changed() row={row_index + 1}", flush=True)

        if row_index < 0 or row_index >= len(self._rows):
            # print("[PAGE3 DEBUG] Invalid row index in _on_itg_changed().", flush=True)
            return

        row = self._rows[row_index]
        itg = row["itg"].currentData()

        if itg:
            ele = self._itg_to_ele.get(str(itg), "")
            row["ele"].setText(ele)
            # print(
            #     f"[PAGE3 DEBUG] Row {row_index + 1}: ITG={itg}, ELE={ele}",
            #     flush=True
            # )
        else:
            row["ele"].setText("")
            # print(f"[PAGE3 DEBUG] Row {row_index + 1}: ITG cleared.", flush=True)

        self._update_ch_count()

    # =========================================================================
    # Data
    # =========================================================================

    def _collect(self) -> list:
        # print("[PAGE3 DEBUG] _collect() started.", flush=True)

        data = []

        for row in self._rows:
            itg = row["itg"].currentData()
            ele = row["ele"].text().strip()
            name = row["name"].text().strip()
            seq = row["seq"].currentText().strip()
            ise_ref = row["ise"].currentData()

            if itg:
                data.append({
                    "itg": str(itg),
                    "ele": ele,
                    "name": name,
                    "seq": seq,
                    "ise_ref": int(ise_ref) if ise_ref is not None else 0,
                })

        # print(f"[PAGE3 DEBUG] _collect() collected {len(data)} rows.", flush=True)
        return data

    def _populate_table_from_data(self, data: list):
        """Fill UI safely."""
        # print(
        #     f"[PAGE3 DEBUG] _populate_table_from_data() started with {len(data)} rows.",
        #     flush=True
        # )

        # Clear all
        for idx, row in enumerate(self._rows):
            with QSignalBlocker(row["itg"]):
                row["itg"].setCurrentIndex(0)

            with QSignalBlocker(row["seq"]):
                row["seq"].setCurrentIndex(0)

            with QSignalBlocker(row["ise"]):
                row["ise"].setCurrentIndex(0)

            row["ele"].setText("")
            row["name"].setText("")

        # print("[PAGE3 DEBUG] Existing UI rows cleared.", flush=True)

        # Fill existing data
        for idx, entry in enumerate(data):
            if idx >= len(self._rows):
                break

            row = self._rows[idx]

            itg_val = str(entry.get("itg", ""))
            ele_val = str(entry.get("ele", ""))
            name_val = str(entry.get("name", ""))
            seq_val = str(entry.get("seq", ""))
            ise_ref_val = entry.get("ise_ref", 0)

            # print(
            #     f"[PAGE3 DEBUG] Filling row {idx + 1}: "
            #     f"ITG={itg_val}, ELE={ele_val}, NAME={name_val}, "
            #     f"SEQ={seq_val}, ISE={ise_ref_val}",
            #     flush=True
            # )

            with QSignalBlocker(row["itg"]):
                itg_index = row["itg"].findData(itg_val)
                row["itg"].setCurrentIndex(itg_index if itg_index >= 0 else 0)

            if ele_val:
                row["ele"].setText(ele_val)
            elif itg_val:
                row["ele"].setText(self._itg_to_ele.get(itg_val, ""))
            else:
                row["ele"].setText("")

            row["name"].setText(name_val[:5])

            with QSignalBlocker(row["seq"]):
                seq_index = row["seq"].findText(seq_val)
                row["seq"].setCurrentIndex(seq_index if seq_index >= 0 else 0)

            with QSignalBlocker(row["ise"]):
                ise_index = row["ise"].findData(ise_ref_val)
                row["ise"].setCurrentIndex(ise_index if ise_index >= 0 else 0)

        self._update_ch_count()

        # print("[PAGE3 DEBUG] _populate_table_from_data() completed.", flush=True)

    def _load_data(self):
        # print("[PAGE3 DEBUG] _load_data() started.", flush=True)

        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)

            if g and g.page_03_channel and isinstance(g.page_03_channel, list):
                # print(
                #     f"[PAGE3 DEBUG] Existing page_03_channel found: "
                #     f"{len(g.page_03_channel)} rows.",
                #     flush=True
                # )
                self._populate_table_from_data(g.page_03_channel)
                return

        finally:
            session.close()
            # print("[PAGE3 DEBUG] _load_data() session closed.", flush=True)

        # print("[PAGE3 DEBUG] No saved Page 3 data. Loading empty grid.", flush=True)
        self._populate_table_from_data([])

    def _save_data(self):
        # print("[PAGE3 DEBUG] _save_data() started.", flush=True)

        data = self._collect()

        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_03_channel = data
                session.commit()
                # print(
                #     f"[PAGE3 DEBUG] Saved page_03_channel with {len(data)} rows.",
                #     flush=True
                # )
        finally:
            session.close()
            # print("[PAGE3 DEBUG] _save_data() session closed.", flush=True)

    # =========================================================================
    # Validation
    # =========================================================================

    def _validate_rows(self) -> bool:
        # print("[PAGE3 DEBUG] _validate_rows() started.", flush=True)

        used_itgs = set()

        for index, row in enumerate(self._rows):
            itg = row["itg"].currentData()
            seq = row["seq"].currentText().strip()

            if not itg:
                continue

            itg_str = str(itg)

            if itg_str in used_itgs:
                self._show_msg(
                    "Invalid Channel Mapping",
                    f"ITG {itg_str} is selected more than once.",
                    QMessageBox.Icon.Warning
                )
                return False

            used_itgs.add(itg_str)

            if seq not in ["1", "2", "3"]:
                self._show_msg(
                    "Invalid SEQ",
                    f"AR-No. {index + 1}: Please select SEQ 1, 2, or 3.",
                    QMessageBox.Icon.Warning
                )
                return False

        # print("[PAGE3 DEBUG] _validate_rows() passed.", flush=True)
        return True

    # =========================================================================
    # Helpers
    # =========================================================================

    def _update_ch_count(self):
        count = 0

        for row in self._rows:
            if row["itg"].currentData():
                count += 1

        self.title_bar.setText(
            f"Element Information - CH {count} - {self.group_name}"
        )

    # =========================================================================
    # Buttons
    # =========================================================================

    def _on_clear(self):
        # print("[PAGE3 DEBUG] Clear All clicked.", flush=True)

        if QMessageBox.question(
            self,
            "Clear All",
            "Remove all elements?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self._populate_table_from_data([])

    def _on_ok(self):
        # print("[PAGE3 DEBUG] OK clicked.", flush=True)

        if not self._validate_rows():
            return

        self._save_data()
        self._show_msg("Saved", "Element information saved successfully.")

    def _on_next(self):
        # print("[PAGE3 DEBUG] Next clicked.", flush=True)

        if not self._validate_rows():
            return

        self._save_data()

        try:
            from ui.anainf.page_04_drift import DriftCorrectionPage
            self.main_window.set_right_widget(
                DriftCorrectionPage(
                    self.main_window,
                    self.group_id,
                    self.group_name
                )
            )
        except ImportError:
            self._show_msg(
                "Next Page",
                "Page 4 (Drift Correction) is not built yet."
            )

    def _on_pre(self):
        # print("[PAGE3 DEBUG] Previous clicked.", flush=True)

        if not self._validate_rows():
            return

        self._save_data()

        try:
            from ui.anainf.page_02_attenuator import AttenuatorPage
            self.main_window.set_right_widget(
                AttenuatorPage(
                    self.main_window,
                    self.group_id,
                    self.group_name
                )
            )
        except ImportError:
            pass

    def _on_print(self):
        # print("[PAGE3 DEBUG] Print clicked.", flush=True)
        self._show_msg("Print", "Print coming soon.")

    def _on_cancel(self):
        # print("[PAGE3 DEBUG] Cancel clicked.", flush=True)

        if self._show_question("Cancel", "Discard changes?"):
            self._load()
            self._on_pre()

    # =========================================================================
    # Message Boxes
    # =========================================================================

    def _show_msg(self, title, text, icon=QMessageBox.Icon.Information):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStyleSheet(
            "QLabel{color:black;font:9pt Arial;}"
            "QPushButton{"
            "background:#d4d0c8;"
            "color:black;"
            "border:2px outset #aaaaaa;"
            "font:9pt Arial;"
            "padding:4px 12px;"
            "min-width:60px;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )
        msg.exec()

    def _show_question(self, title, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        msg.setStyleSheet(
            "QLabel{color:black;font:9pt Arial;}"
            "QPushButton{"
            "background:#d4d0c8;"
            "color:black;"
            "border:2px outset #aaaaaa;"
            "font:9pt Arial;"
            "padding:4px 12px;"
            "min-width:60px;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )
        return msg.exec() == QMessageBox.StandardButton.Yes

    # =========================================================================
    # Load / Save Entry Points
    # =========================================================================

    def _load(self):
        self._load_data()

    def _save(self):
        self._save_data()