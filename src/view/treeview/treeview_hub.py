from typing import *

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject
from controller.pipeline.pipeline_hub import PipelineNode
from listener.listener_hub import PyTransEvent
from model.capture.capture_node import CaptureNode
from model.doc import WorkingDoc
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from enum import Enum, auto
from typing import *
from my_utils import qt_utils
from view.pipeline.pipe_link_edit import PipeLinkEditWidget
from view.view_hub import ViewController, ViewHub

if TYPE_CHECKING:
    from view.view_hub import ViewHub
import my_utils


class TreeViewHub(ViewController):
    def __init__(self, view_hub: ViewHub) -> None:
        super().__init__(view_hub)
        old_widget = view_hub.ui.capturedItemTree
        parent: QWidget = old_widget.parent()
        self.tree_widget = DragDropTreeWidget(parent)
        parent.layout().removeWidget(old_widget)
        parent.layout().addWidget(self.tree_widget)
        QObjectCleanupHandler().add(old_widget)

        self.tree_widget.setColumnCount(2)
        self.tree_widget.setHeaderLabels(["Name", "Type"])
        self.tree_widget.setAcceptDrops(True)
        self.tree_widget.setDragEnabled(True)
        self.tree_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.tree_widget.itemSelectionChanged.connect(self.selectionChanged)

    def update(self, signal=ViewController.UpdateSignal.UPDATE_ALL, *args, **kwargs):
        def dfs(node: CaptureNode, tree_item=QTreeWidgetItem(), depth=0):
            for child in node.children:
                child_item = dfs(
                    child,
                    QTreeWidgetItem(tree_item, tree_item.ItemType.Type),
                    depth + 1,
                )
                tree_item.addChild(child_item)
            tree_item.setText(0, node.get_node_name())
            tree_item.setText(1, node.get_node_type().name)
            tree_item.setData(0, Qt.ItemDataRole.UserRole, node)
            return tree_item

        if signal == ViewController.UpdateSignal.UPDATE_ALL:
            working_doc = self.view_hub.main.model_hub.working_doc
            if working_doc == None:
                return
            root_tree_item = dfs(working_doc.root_node)
            self.tree_widget.clear()
            self.tree_widget.addTopLevelItem(root_tree_item)

    def selectionChanged(self):
        selected_items = self.tree_widget.selectedItems()
        if len(selected_items) != 1:
            return
        item = selected_items[0]
        self.view_hub.update_all(
            ViewController.UpdateSignal.UPDATE_FOCUS,
            item.data(0,Qt.ItemDataRole.UserRole),
        )


class DragDropTreeWidget(QTreeWidget):
    pass
