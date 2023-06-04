from typing import *

from PyQt6 import QtGui
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
import my_utils.qt_utils
from view.pipeline.pipe_link_edit import PipeLinkEditWidget

if TYPE_CHECKING:
    from view.view_hub import ViewHub
import my_utils


class IOViewhub:
    def __init__(self, view_hub: "ViewHub") -> None:
        self.view_hub = view_hub
        self.ui = view_hub.ui

        self.ui.openedDocList.currentRowChanged.connect(self.working_doc_change_event)
        self.ui.docCloseButton.clicked.connect(self.opened_doc_close)

    def update_opened_doc(self):
        self.model = self.view_hub.main.model_hub
        opened_doc_list = self.ui.openedDocList
        opened_doc_list.clear()
        for doc in self.model.opened_docs:
            listitem = QListWidgetItem()
            listitem.setText(doc.io_memo.io_module.get_doc_title(doc))
            listitem.setData(Qt.ItemDataRole.UserRole, doc)
            opened_doc_list.addItem(listitem)
            if doc == self.model.working_doc:
                opened_doc_list.setCurrentItem(listitem)

    def working_doc_change_event(self,row:int):
        if(row==-1):
            return
        self.model = self.view_hub.main.model_hub
        opened_doc_list = self.ui.openedDocList
        new_working_doc = opened_doc_list.currentItem().data(Qt.ItemDataRole.UserRole)
        if new_working_doc == self.model.working_doc:
            return
        if isinstance(new_working_doc, WorkingDoc):
            self.model.working_doc = new_working_doc
            self.view_hub.main.listener_hub.post_event(
                PyTransEvent(PyTransEvent.Type.UI_UPDATE)
            )

    def opened_doc_close(self):
        working_doc=self.model.working_doc
        doc_list=self.model.opened_docs
        working_i=doc_list.index(working_doc)
        doc_list.remove(working_doc)
        if working_i>=doc_list.__len__():
            working_i-=1
        if working_i<0:
            self.model.working_doc=None
        else:
            self.model.working_doc=doc_list[working_i]
        self.view_hub.main.listener_hub.post_event(
            PyTransEvent(PyTransEvent.Type.UI_UPDATE)
        )

