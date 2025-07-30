from PyQt6.QtWidgets import QGridLayout, QVBoxLayout
from .threshold_slider.ThresholdSlider import ThresholdSlider
from .MatrixView import MatrixHighlightView
from PyQt6.QtWidgets import QWidget

from functools import partial


class ThresholdBox(QWidget):
    grid: QGridLayout
    matrix_view: MatrixHighlightView

    thresholds: list[ThresholdSlider] = []

    def __init__(self, matrix_view: MatrixHighlightView) -> None:
        super(ThresholdBox, self).__init__()

        self.grid = QVBoxLayout()
        self.grid.setContentsMargins(1, 1, 1, 1)
        self.grid.setSpacing(0)
        self.setLayout(self.grid)

        self.matrix_view = matrix_view
        self.matrix_view.matrixSet.connect(self._on_matrix_set)

    def _on_matrix_set(self):
        self._clear_thresholds()
        self._create_thresholds()

    def _create_thresholds(self):
        n_rows = self.matrix_view.n_rows
        row_height = self.matrix_view.row_height
        matrix = self.matrix_view.matrix
        for i in range(n_rows):
            height = int(self.matrix_view.height() / n_rows)
            threshold_slider = ThresholdSlider(matrix[:, i * row_height])
            threshold_slider.setMaximumHeight(height)
            self.thresholds.append(threshold_slider)

            threshold_slider.newEvents.connect(partial(self._on_new_threshold, i))
            self.grid.addWidget(threshold_slider)

            threshold_slider.newEvents.emit()

    def _on_new_threshold(self, row):
        threshold_slider = self.sender()
        self.matrix_view.set_highlight(threshold_slider.event_mask(), row)

    def _clear_thresholds(self):
        for i in reversed(range(len(self.thresholds))):
            self.grid.itemAt(i).widget().setParent(None)
        self.thresholds.clear()
