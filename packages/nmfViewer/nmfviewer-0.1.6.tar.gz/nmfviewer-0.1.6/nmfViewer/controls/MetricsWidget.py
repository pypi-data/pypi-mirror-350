from PyQt6.QtWidgets import QGroupBox, QLabel, QScrollArea
from PyQt6.QtWidgets import QVBoxLayout
import numpy as np
from pyqtgraph import colormap
from pyqtgraph.imageview.ImageView import ImageView

from spidet.save.nmf_data import NMFMetrics


class MetricsWidget(QGroupBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent, title="Metrics")

        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setDirection(QVBoxLayout.Direction.BottomToTop)
        self.setLayout(self.layout)

    def set_metrics(self, metrics: NMFMetrics):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for name in metrics.children():
            values = None
            try:
                values = metrics.load_dset(name)
            except:
                print(f"Should be dataset or attribute: {name} at {metrics.path()}")
            if values is not None:
                self._add_dataset(name, values)

        for name in metrics.attributes():
            self._add_single_value(name, metrics.load_attr(name))

    def _add_single_value(self, name: str, value) -> None:
        value_label = QLabel()
        if value - int(value) > 0:
            value_label.setText(f"{name}: {value:.4}")
        else:
            value_label.setText(f"{name}: {value}")
        self.layout.addWidget(value_label)

    def _add_dataset(self, name: str, dset: np.ndarray) -> None:
        imv = ImageView()
        imv.setColorMap(colormap.getFromMatplotlib("YlGn_r"))
        imv.setImage(dset)
        imv.ui.histogram.hide()
        imv.ui.roiBtn.hide()
        imv.ui.menuBtn.hide()

        box = QGroupBox(title=f"{name}:")
        layout = QVBoxLayout()
        layout.addWidget(imv)
        box.setLayout(layout)

        self.layout.addWidget(box)
