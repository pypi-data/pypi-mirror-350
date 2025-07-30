from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QCheckBox, QGroupBox, QVBoxLayout


class ViewControls(QGroupBox):
    show_crosshair = pyqtSignal(bool)
    show_channel_info = pyqtSignal(bool)
    show_value = pyqtSignal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__(parent, title="Display")

        self._init_ui()

    def _init_ui(self):
        self.crosshair_checkbox = QCheckBox("Crosshair")
        self.crosshair_checkbox.setChecked(True)
        self.crosshair_checkbox.checkStateChanged.connect(
            self._on_crosshair_checkbox_clicked
        )

        self.channel_info_checkbox = QCheckBox("Channel name")
        self.channel_info_checkbox.setChecked(True)
        self.channel_info_checkbox.checkStateChanged.connect(
            self._on_channel_info_checkbox_clicked
        )

        self.value_checkbox = QCheckBox("Cell value")
        self.value_checkbox.setChecked(True)
        self.value_checkbox.checkStateChanged.connect(self._on_value_checkbox_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.crosshair_checkbox)
        layout.addWidget(self.channel_info_checkbox)
        layout.addWidget(self.value_checkbox)
        self.setLayout(layout)

    def _on_crosshair_checkbox_clicked(self):
        self.show_crosshair.emit(self.crosshair_checkbox.isChecked())

    def _on_channel_info_checkbox_clicked(self):
        self.show_channel_info.emit(self.channel_info_checkbox.isChecked())

    def _on_value_checkbox_clicked(self):
        self.show_value.emit(self.value_checkbox.isChecked())
