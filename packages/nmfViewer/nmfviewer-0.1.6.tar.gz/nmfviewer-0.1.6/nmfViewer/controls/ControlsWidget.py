from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSignal

from .ViewControls import ViewControls
from .NMFTreeView import NMFFeatureMatrixItem, NMFModelItem, NMFTreeView


class ControlsWidget(QWidget):
    featureMatrixChanged = pyqtSignal(NMFFeatureMatrixItem)
    nmfModelChanged = pyqtSignal(NMFModelItem)
    show_value = pyqtSignal(bool)
    show_crosshair = pyqtSignal(bool)
    show_channel_info = pyqtSignal(bool)

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.init_ui()
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

    def init_ui(self):
        self.view_controls = ViewControls()
        self.view_controls.show_crosshair.connect(self.show_crosshair.emit)
        self.view_controls.show_channel_info.connect(self.show_channel_info.emit)
        self.view_controls.show_value.connect(self.show_value.emit)

        self.load_nmf_button = QPushButton("Load NMF Results")
        self.load_nmf_button.clicked.connect(self._load_nmf_clicked)

        self.nmf_tree_view = NMFTreeView()
        self.nmf_tree_view.featureMatrixChanged.connect(self.featureMatrixChanged.emit)
        self.nmf_tree_view.nmfModelChanged.connect(self.nmfModelChanged.emit)

        layout = QVBoxLayout()
        layout.addWidget(self.load_nmf_button)
        layout.addWidget(self.nmf_tree_view)
        layout.addWidget(self.view_controls)
        self.setLayout(layout)

    def _load_nmf_clicked(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Load NMF(s)", ".", "*.h5")
        for file_name in file_names:
            self.nmf_tree_view.add_nmf_file(file_name)
