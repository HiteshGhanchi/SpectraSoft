"""Dependency-free observed-versus-predicted working-curve chart."""

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget

from ui.theme import COLORS


class WorkingCurveChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []
        self.target_line = []
        self.residuals = []
        self.setObjectName("chartSurface")
        self.setMinimumHeight(180)
        self.setStyleSheet(
            f"background:{COLORS['surface']};border:1px solid {COLORS['border_strong']};"
        )

    def set_points(self, points, coefficients):
        del coefficients
        self.points = list(points or [])
        self.target_line = [
            (float(point["chemical"]), float(point["predicted"]))
            for point in self.points
        ]
        self.residuals = [float(point.get("residual", 0.0)) for point in self.points]
        self.update()

    def paintEvent(self, event):
        del event
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(COLORS["surface"]))
        plot = QRectF(42, 12, max(1, self.width() - 54), max(1, self.height() - 28))
        painter.setPen(QPen(QColor(COLORS["muted"]), 1))
        painter.drawRect(plot)
        if not self.points:
            painter.end()
            return

        values = [float(point["chemical"]) for point in self.points]
        predicted = [float(point["predicted"]) for point in self.points]
        low = min(values + predicted)
        high = max(values + predicted)
        span = high - low or 1.0

        def point(x, y):
            return (
                plot.left() + ((x - low) / span) * plot.width(),
                plot.bottom() - ((y - low) / span) * plot.height(),
            )

        painter.setPen(QPen(QColor(COLORS["chart_green"]), 1, Qt.PenStyle.DashLine))
        start = point(low, low)
        end = point(high, high)
        painter.drawLine(int(start[0]), int(start[1]), int(end[0]), int(end[1]))

        painter.setPen(QPen(QColor(COLORS["chart_blue"]), 6))
        for actual, estimate in zip(values, predicted):
            x, y = point(actual, estimate)
            painter.drawPoint(int(x), int(y))
        painter.end()
