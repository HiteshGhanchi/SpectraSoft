"""Small dependency-free live graph for ATT adjustment readings."""

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget

from ui.theme import COLORS


def normalized_time_positions(history) -> list[float]:
    """Return x-axis positions normalized from the readings' timestamps."""
    if not history:
        return []
    timestamps = [float(item[0]) for item in history]
    start = timestamps[0]
    span = timestamps[-1] - start
    if span <= 0:
        denominator = max(1, len(timestamps) - 1)
        return [index / denominator for index in range(len(timestamps))]
    return [(timestamp - start) / span for timestamp in timestamps]


class AdjustmentGraphWidget(QWidget):
    """Paint intensity history, target band, and ATT-change markers."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.target_band = (0.5, 0.6)
        self.history = []
        self.setObjectName("chartSurface")
        self.setMinimumHeight(230)
        self.setStyleSheet(
            f"background:{COLORS['surface']};border:1px solid {COLORS['border_strong']};"
        )

    def set_target_band(self, low: float, high: float):
        self.target_band = (float(low), float(high))
        self.update()

    def set_history(self, history):
        self.history = list(history or [])
        self.update()

    def paintEvent(self, event):
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(COLORS["surface"]))

        plot = QRectF(48, 16, max(1, self.width() - 64), max(1, self.height() - 42))
        painter.setPen(QPen(QColor(COLORS["muted"]), 1))
        painter.drawRect(plot)

        low, high = self.target_band
        y_low = self._y_for_value(low, plot)
        y_high = self._y_for_value(high, plot)
        painter.fillRect(
            QRectF(plot.left(), y_high, plot.width(), y_low - y_high),
            QColor(COLORS["green_soft"]),
        )
        painter.setPen(QPen(QColor(COLORS["chart_green"]), 1, Qt.PenStyle.DashLine))
        painter.drawLine(
            int(plot.left()), int(y_low), int(plot.right()), int(y_low)
        )
        painter.drawLine(
            int(plot.left()), int(y_high), int(plot.right()), int(y_high)
        )

        if not self.history:
            painter.end()
            return

        values = [float(item[1]) for item in self.history]
        x_positions = normalized_time_positions(self.history)
        painter.setPen(QPen(QColor(COLORS["chart_blue"]), 2))
        points = []
        for index, value in enumerate(values):
            x = plot.left() + plot.width() * x_positions[index]
            points.append((x, self._y_for_value(value, plot)))
        for first, second in zip(points, points[1:]):
            painter.drawLine(
                int(first[0]), int(first[1]), int(second[0]), int(second[1])
            )

        painter.setPen(QPen(QColor(COLORS["chart_amber"]), 1, Qt.PenStyle.DotLine))
        previous_att = None
        for index, item in enumerate(self.history):
            att = item[2] if len(item) > 2 else None
            if att is not None and att != previous_att:
                x = plot.left() + plot.width() * x_positions[index]
                painter.drawLine(
                    int(x), int(plot.top()), int(x), int(plot.bottom())
                )
            previous_att = att
        painter.end()

    @staticmethod
    def _y_for_value(value: float, plot: QRectF) -> float:
        normalized = max(0.0, min(1.0, float(value)))
        return plot.bottom() - normalized * plot.height()
