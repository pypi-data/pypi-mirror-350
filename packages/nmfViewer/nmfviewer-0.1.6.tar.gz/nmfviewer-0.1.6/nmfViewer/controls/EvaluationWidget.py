from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
)


class EvaluationWidget(QWidget):
    newTimeGradePath = pyqtSignal(str)
    newTriggersPath = pyqtSignal(str)

    clearTimeGrades = pyqtSignal()
    clearTriggers = pyqtSignal()

    showVPrime = pyqtSignal(bool)
    showTimeGrades = pyqtSignal(bool)
    showTriggers = pyqtSignal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.load_time_grades_button = QPushButton("Time Grades")
        self.load_time_grades_button.clicked.connect(self._on_load_time_grades_clicked)

        self.load_triggers_button = QPushButton("Triggers")
        self.load_triggers_button.clicked.connect(self._on_load_triggers_clicked)

        self.toggle_v_prime_button = QCheckBox("V' = V - WH")
        self.toggle_v_prime_button.clicked.connect(self._on_difference_toggled)

        self.clear_time_grades = QPushButton("Time Grades")
        self.clear_time_grades.clicked.connect(self._on_clear_time_grades_clicked)
        self.clear_triggers = QPushButton("Triggers")
        self.clear_triggers.clicked.connect(self._on_clear_triggers_clicked)

        self.show_time_grades = QCheckBox("Time Grades")
        self.show_time_grades.clicked.connect(self._on_show_time_grades)

        self.show_triggers = QCheckBox("Triggers")
        self.show_triggers.clicked.connect(self._on_show_triggers)

        load_layout = QVBoxLayout()
        load_layout.addWidget(self.load_time_grades_button)
        load_layout.addWidget(self.load_triggers_button)

        load_box = QGroupBox(title="Load")
        load_box.setLayout(load_layout)

        clear_layout = QVBoxLayout()
        clear_layout.addWidget(self.clear_time_grades)
        clear_layout.addWidget(self.clear_triggers)

        clear_box = QGroupBox(title="Clear")
        clear_box.setLayout(clear_layout)

        display_layout = QVBoxLayout()
        display_layout.addWidget(self.show_time_grades)
        display_layout.addWidget(self.show_triggers)
        display_layout.addWidget(self.toggle_v_prime_button)

        display_box = QGroupBox(title="Display")
        display_box.setLayout(display_layout)

        layout = QVBoxLayout()
        layout.addWidget(load_box)
        layout.addWidget(display_box)
        layout.addWidget(clear_box)

        layout.insertStretch(-1)
        self.setLayout(layout)

    def _on_load_time_grades_clicked(self):
        time_grades_path = QFileDialog.getOpenFileName(
            self, "Load Time Grades", ".", "*.csv *.h5"
        )[0]
        self.newTimeGradePath.emit(time_grades_path)

    def _on_load_triggers_clicked(self):
        triggers_path = QFileDialog.getOpenFileName(self, "Load Triggers", ".", "*.h5")[
            0
        ]
        self.newTriggersPath.emit(triggers_path)

    def _on_difference_toggled(self):
        self.showVPrime.emit(self.toggle_v_prime_button.isChecked())

    def _on_clear_time_grades_clicked(self):
        self.clearTimeGrades.emit()

    def _on_clear_triggers_clicked(self):
        self.clearTriggers.emit()

    def _on_show_time_grades(self):
        self.showTimeGrades.emit(self.show_time_grades.isChecked())

    def _on_show_triggers(self):
        self.showTriggers.emit(self.show_triggers.isChecked())
