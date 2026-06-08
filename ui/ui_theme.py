"""
SpectraSoft — Centralized UI Theme & Styling
==============================================
Single source of truth for all UI styling.
"""

# =============================================================================
# SECTION 1: COLOR PALETTE
# =============================================================================

class Colors:
    BG_MAIN = "#d4d0c8"
    BG_WHITE = "#ffffff"
    BG_LIGHT_GRAY = "#f0f0f0"
    MENUBAR_BG = "#c0b8a8"   
    
    TEXT_BLACK = "black"
    TEXT_WHITE = "white"
    TEXT_DARK_GRAY = "#555"
    TEXT_MEDIUM_GRAY = "#666"
    TEXT_LIGHT_GRAY = "#888"
    TEXT_DISABLED = "#999"
    
    ACCENT_PRIMARY = "#0078d7"
    ACCENT_SECONDARY = "#5c9bd5"
    
    BORDER_DARK = "#999"
    BORDER_NORMAL = "#888"
    BORDER_LIGHT = "#aaa"
    BORDER_WHITE = "#ffffff"
    
    STATUS_SUCCESS = "green"
    STATUS_ERROR = "#cc0000"
    STATUS_INACTIVE = "#555"
    
    GRID_HEADER = "#d4d0c8"
    GRID_ALT_ROW = "#f0f0f0"
    GRID_LINE = "#c0c0c0"


# =============================================================================
# SECTION 2: FONTS
# =============================================================================

class Fonts:
    FAMILY_DEFAULT = "Arial"
    SIZE_SMALL = 8
    SIZE_NORMAL = 9
    SIZE_LARGE = 10
    SIZE_TITLE = 11
    SIZE_HEADER = 12
    WEIGHT_NORMAL = "normal"
    WEIGHT_BOLD = "bold"


# =============================================================================
# SECTION 3: SPACING & DIMENSIONS
# =============================================================================

class Spacing:
    MAIN_WINDOW_WIDTH = 1100
    MAIN_WINDOW_HEIGHT = 700
    PAGE_WINDOW_WIDTH = 900
    PAGE_WINDOW_HEIGHT = 650
    
    PADDING_LARGE = 8
    PADDING_NORMAL = 4
    PADDING_SMALL = 2
    
    MARGIN_LARGE = 8
    MARGIN_NORMAL = 4
    MARGIN_SMALL = 2
    
    ROW_HEIGHT = 24
    LABEL_WIDTH = 60
    COLUMN_WIDTH = 155
    UNIT_WIDTH = 50
    
    GROUP_PANEL_WIDTH = 210
    DIVIDER_WIDTH = 1
    
    BUTTON_MIN_WIDTH = 65
    BUTTON_PADDING_X = 8
    BUTTON_PADDING_Y = 3
    
    BORDER_OUTSET = "2px"
    BORDER_INSET = "2px"
    BORDER_NORMAL = "1px"


# =============================================================================
# SECTION 4: STYLESHEETS (as class attributes, computed once)
# =============================================================================

class Stylesheets:
    # Buttons
    BUTTON_NORMAL = (
        f"QPushButton{{"
        f"background:{Colors.BG_MAIN};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:{Spacing.BORDER_OUTSET} outset {Colors.BORDER_WHITE};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:{Spacing.BUTTON_PADDING_Y}px {Spacing.BUTTON_PADDING_X}px;"
        f"min-width:{Spacing.BUTTON_MIN_WIDTH}px;"
        f"}}"
        f"QPushButton:pressed{{"
        f"border:{Spacing.BORDER_INSET} inset {Colors.BORDER_NORMAL};"
        f"}}"
    )
    
    # Labels
    LABEL_NORMAL = (
        f"QLabel{{"
        f"background:{Colors.BG_MAIN};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:none;"
        f"}}"
    )
    
    LABEL_WITH_BORDER = (
        f"QLabel{{"
        f"background:{Colors.BG_MAIN};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_NORMAL};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:2px 4px;"
        f"}}"
    )
    
    LABEL_HEADER = (
        f"QLabel{{"
        f"background:{Colors.BG_MAIN};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_NORMAL};"
        f"font:bold {Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:2px 4px;"
        f"}}"
    )
    
    LABEL_HINT = (
        f"QLabel{{"
        f"color:{Colors.TEXT_MEDIUM_GRAY};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"text-align:center;"
        f"}}"
    )
    
    # Inputs
    LINEEDIT_NORMAL = (
        f"QLineEdit{{"
        f"background:{Colors.BG_WHITE};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_NORMAL};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:1px 3px;"
        f"}}"
    )
    
    LINEEDIT_READONLY = (
        f"QLineEdit{{"
        f"background:{Colors.BG_MAIN};"
        f"color:{Colors.TEXT_LIGHT_GRAY};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_NORMAL};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:1px 3px;"
        f"}}"
    )
    
    SPINBOX_NORMAL = (
        f"QSpinBox{{"
        f"background:{Colors.BG_WHITE};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_NORMAL};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:1px 3px;"
        f"}}"
    )
    
    COMBOBOX_NORMAL = (
        f"QComboBox{{"
        f"background:{Colors.BG_WHITE};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_NORMAL};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"}}"
        f"QComboBox QAbstractItemView{{"
        f"background:{Colors.BG_WHITE};"
        f"color:{Colors.TEXT_BLACK};"
        f"}}"
    )
    
    GROUPBOX_NORMAL = (
        f"QGroupBox{{"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_DARK};"
        f"margin-top:8px;"
        f"padding-top:4px;"
        f"background:{Colors.BG_MAIN};"
        f"}}"
        f"QGroupBox::title{{"
        f"subcontrol-origin:margin;"
        f"left:8px;"
        f"color:{Colors.TEXT_BLACK};"
        f"}}"
    )
    
    MENUBAR = (
        f"QMenuBar{{"
        f"background:{Colors.MENUBAR_BG};"
        f"color:{Colors.TEXT_BLACK};"
        f"border-bottom:1px solid {Colors.BORDER_DARK};"   # subtle separator
        f"}}"
        f"QMenuBar::item{{"
        f"background:{Colors.MENUBAR_BG};"
        f"color:{Colors.TEXT_BLACK};"
        f"padding:4px 12px;"           # more padding for clickable feel
        f"font:{Fonts.SIZE_LARGE}pt {Fonts.FAMILY_DEFAULT};"   # larger font
        f"}}"
        f"QMenuBar::item:selected{{"
        f"background:{Colors.ACCENT_PRIMARY};"
        f"color:{Colors.TEXT_WHITE};"
        f"}}"
        f"QMenu{{"
        f"background:{Colors.BG_WHITE};"      # white dropdown background
        f"color:{Colors.TEXT_BLACK};"
        f"border:1px solid {Colors.BORDER_DARK};"
        f"}}"
        f"QMenu::item{{"
        f"padding:4px 20px;"
        f"}}"
        f"QMenu::item:selected{{"
        f"background:{Colors.ACCENT_PRIMARY};"
        f"color:{Colors.TEXT_WHITE};"
        f"}}"
    )
    
    STATUSBAR = f"background:{Colors.BG_MAIN}; color:{Colors.TEXT_BLACK};"
    
    CELL_READONLY = (
        f"QLabel{{"
        f"background:{Colors.BG_LIGHT_GRAY};"
        f"color:{Colors.TEXT_DISABLED};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_NORMAL};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:1px 4px;"
        f"}}"
    )
    
    CELL_EDITABLE = (
        f"QLineEdit{{"
        f"background:{Colors.BG_WHITE};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_NORMAL};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:1px 4px;"
        f"}}"
    )
    
    TABLE_NORMAL = (
        f"QTableWidget{{"
        f"background:{Colors.BG_WHITE};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_LIGHT};"
        f"border-collapse:collapse;"
        f"alternate-background-color:{Colors.BG_LIGHT_GRAY};"
        f"gridline-color:{Colors.GRID_LINE};"
        f"}}"
        f"QHeaderView::section{{"
        f"background:{Colors.GRID_HEADER};"
        f"color:{Colors.TEXT_BLACK};"
        f"border:{Spacing.BORDER_NORMAL} solid {Colors.BORDER_LIGHT};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:2px;"
        f"}}"
    )
    
    SCROLLAREA = "border:none;"
    
    PANEL_MAIN = f"background:{Colors.BG_MAIN};"
    PANEL_WHITE = f"background:{Colors.BG_WHITE};"
    
    HEADER_BAR = (
        f"background:{Colors.ACCENT_SECONDARY};"
        f"color:{Colors.TEXT_WHITE};"
        f"font:bold {Fonts.SIZE_LARGE}pt {Fonts.FAMILY_DEFAULT};"
    )
    
    # Status label styles (just color/font, not full stylesheet)
    STATUS_LABEL_NORMAL = f"color:{Colors.TEXT_BLACK};"
    STATUS_LABEL_SUCCESS = f"color:{Colors.STATUS_SUCCESS};font-weight:bold;"
    STATUS_LABEL_ERROR = f"color:{Colors.STATUS_ERROR};font-weight:bold;"
    STATUS_LABEL_INACTIVE = f"color:{Colors.STATUS_INACTIVE};"


# =============================================================================
# SECTION 5: HELPER FUNCTIONS
# =============================================================================

def get_font(size: int = Fonts.SIZE_NORMAL, bold: bool = False):
    from PyQt6.QtGui import QFont
    f = QFont(Fonts.FAMILY_DEFAULT, size)
    if bold:
        f.setBold(True)
    return f

def get_color(color_hex: str):
    from PyQt6.QtGui import QColor
    return QColor(color_hex)

def build_button_style(bg_color=Colors.BG_MAIN, text_color=Colors.TEXT_BLACK,
                       border_color=Colors.BORDER_WHITE, font_size=Fonts.SIZE_NORMAL, bold=False):
    font_weight = Fonts.WEIGHT_BOLD if bold else ""
    return (
        f"QPushButton{{"
        f"background:{bg_color};"
        f"color:{text_color};"
        f"border:{Spacing.BORDER_OUTSET} outset {border_color};"
        f"font:{font_weight} {font_size}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:{Spacing.BUTTON_PADDING_Y}px {Spacing.BUTTON_PADDING_X}px;"
        f"min-width:{Spacing.BUTTON_MIN_WIDTH}px;"
        f"}}"
        f"QPushButton:pressed{{"
        f"border:{Spacing.BORDER_INSET} inset {Colors.BORDER_NORMAL};"
        f"}}"
    )

def build_label_style(bg_color=Colors.BG_MAIN, text_color=Colors.TEXT_BLACK,
                      bold=False, border=False, border_color=Colors.BORDER_NORMAL):
    font_weight = Fonts.WEIGHT_BOLD if bold else ""
    border_style = f"{Spacing.BORDER_NORMAL} solid {border_color};" if border else "none;"
    return (
        f"QLabel{{"
        f"background:{bg_color};"
        f"color:{text_color};"
        f"border:{border_style}"
        f"font:{font_weight} {Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:2px 4px;"
        f"}}"
    )

def build_input_style(bg_color=Colors.BG_WHITE, text_color=Colors.TEXT_BLACK,
                      border_color=Colors.BORDER_NORMAL):
    return (
        f"background:{bg_color};"
        f"color:{text_color};"
        f"border:{Spacing.BORDER_NORMAL} solid {border_color};"
        f"font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};"
        f"padding:1px 3px;"
    )