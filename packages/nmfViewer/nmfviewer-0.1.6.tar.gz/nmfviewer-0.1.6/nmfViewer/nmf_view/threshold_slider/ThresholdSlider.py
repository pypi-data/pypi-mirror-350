from PyQt6.QtWidgets import QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

import numpy as np

from spidet.spike_detection.thresholding import ThresholdGenerator

from .DoubleSlider import DoubleSlider

class ThresholdSlider(QFrame):
    newEvents = pyqtSignal()

    def __init__(self, h_row):
        super().__init__()
        # Initialize label
        self.value_label = QLabel(alignment=Qt.AlignmentFlag.AlignVCenter)
        self.value_label.setMinimumWidth(40)

        # Initialize and connect slider
        self.slider = DoubleSlider(orientation=Qt.Orientation.Horizontal)
        self.slider.setMinimum(np.min(h_row))
        self.slider.setMaximum(np.max(h_row))
        self.slider.doubleValueChanged.connect(self.value_label.setNum)
        self.slider.doubleValueChanged.connect(self.threshold_changed)

        # Initialize threshold generator and set default threshold
        self.threshold_generator = ThresholdGenerator(h_row)
        default_threshold = self.threshold_generator.generate_threshold()
        self.slider.setValue(default_threshold)

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.value_label)
        layout.addWidget(self.slider)

        self.setFrameStyle(QFrame.Shape.Panel)

    def threshold_changed(self, value):
        self.events = self.threshold_generator.find_events(value)[0]
        self.newEvents.emit()

    def value(self):
        return self.slider.value()

    def emitNewEvents(self):
        self.newEvents.emit()

    def event_mask(self):
        return self.events['event_mask']

    def events_on(self):
        return self.events['events_on']

    def events_off(self):
        return self.events['events_off']


    def setMaximumHeight(self, h: int) -> None:
        self.value_label.setMaximumHeight(h)
        self.slider.setMaximumHeight(h)
        return super().setMaximumHeight(h)
