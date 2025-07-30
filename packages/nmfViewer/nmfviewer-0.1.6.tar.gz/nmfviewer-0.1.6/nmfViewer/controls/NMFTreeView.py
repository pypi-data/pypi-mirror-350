from __future__ import annotations

import os
from PyQt6.QtCore import QModelIndex, pyqtSignal
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView, QTreeView, QWidget
import typing

from spidet.save.nmf_data import NMFRoot, FeatureMatrixGroup, NMFModel


class NMFFeatureMatrixItem(QStandardItem):
    def __init__(self, fm_group: FeatureMatrixGroup, start_timestamp) -> None:
        super().__init__(fm_group.name)
        self.feature_matrix_group = fm_group
        self.start_timestamp = start_timestamp


class NMFModelItem(QStandardItem):
    def __init__(self, nmf: NMFModel) -> None:
        super().__init__(nmf.name)
        self.nmf = nmf


class NMFTreeView(QTreeView):
    featureMatrixChanged = pyqtSignal(NMFFeatureMatrixItem)
    nmfModelChanged = pyqtSignal(NMFModelItem)

    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        model = QStandardItemModel()
        self.rootItem = model.invisibleRootItem()
        self.setModel(model)
        self.clicked[QModelIndex].connect(self._on_click)
        self.header().hide()

    def add_nmf_file(self, path: str) -> None:
        filename = os.path.basename(path)
        fileItem = QStandardItem(filename)
        fileItem.setSelectable(False)
        self.rootItem.appendRow(fileItem)

        data = NMFRoot(path)
        for dset in data.datasets():
            for fm_group in dset.feature_matrices():
                start_timestamp = dset.meta().start_timestamp

                fmItem = NMFFeatureMatrixItem(fm_group, start_timestamp)
                fileItem.appendRow(fmItem)

                for rank_group in fm_group.ranks():
                    rankItem = QStandardItem(rank_group.name)
                    rankItem.setSelectable(False)
                    fmItem.appendRow(rankItem)

                    for model in rank_group.models():
                        modelItem = NMFModelItem(model)
                        rankItem.appendRow(modelItem)

    def _on_click(self, index):
        item = self.model().itemFromIndex(index)
        if isinstance(item, NMFFeatureMatrixItem):
            self.featureMatrixChanged.emit(item)
        elif isinstance(item, NMFModelItem):
            self.nmfModelChanged.emit(item)
