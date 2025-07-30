from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from .ControlsWidget import ControlsWidget
from .MetricsWidget import MetricsWidget
from .EvaluationWidget import EvaluationWidget


class Tabs(QTabWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.controls_widget = ControlsWidget()
        self.metrics_widget = MetricsWidget()
        self.evaluation_widget = EvaluationWidget()

        controls = QVBoxLayout()
        controls.addWidget(self.controls_widget)
        controls.addWidget(self.metrics_widget)

        controls_widget = QWidget()
        controls_widget.setLayout(controls)

        self.addTab(controls_widget, "Controls")
        self.addTab(self.evaluation_widget, "Evaluation")

        self.setMaximumWidth(230)
