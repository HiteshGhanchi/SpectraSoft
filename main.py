"""
SpectraSoft — Main Entry Point
Run:  python main.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from core.persistence.database import init_db
from ui.main_window import MainWindow
from ui.theme import apply_theme


def main():
    init_db()

    app = QApplication(sys.argv)
    apply_theme(app)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
