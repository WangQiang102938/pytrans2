import io
from model.capture.capture_node import CaptureNode
from listener.listener_hub import Listener, PyTransEvent
from view.preview.capture_box import CaptureBoxItem
from view.preview.page import PageItem
from PIL.Image import Image
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from view.view_hub import ViewController


# def find_render_node(curr_node: CaptureNode, page_no: int, res_list: list = None):
#     if res_list == None:
#         res_list = list()
#     if (
#         curr_node.get_visual_memo() != None
#         and curr_node.get_visual_memo().page_no == page_no
#     ):
#         res_list.append(curr_node)
#     for node in curr_node.children:
#         find_render_node(node, page_no, res_list)
#     return res_list


# def PIL2QPixmap(pil: Image):
#     buffer = io.BytesIO()
#     pil.save(buffer, format="JPEG")
#     img = QImage()
#     img.loadFromData(buffer.getvalue())
#     return QPixmap(img)


class DefaultUIUpdate(Listener):
    def listened_event(self, event: PyTransEvent) -> PyTransEvent:
        if event.args.__len__() != 0 or event.kwargs.__len__() != 0:
            return False
        return event.type == event.Type.UI_UPDATE

    def event_handler(self, event: PyTransEvent):
        self.main.view_hub.update_all()
        self.main.mainwindow_event_obj.force_run(QResizeEvent(QSize(), QSize()))

        return super().event_handler(event)


class SignalUIUpdate_WithCapNode(Listener):
    def listened_event(self, event: PyTransEvent) -> bool:
        if event.type != event.Type.UI_UPDATE:
            return False
        if event.args.__len__() != 2:
            return False
        signal_type_check = event.args[0] in ViewController.UpdateSignal
        node_type_check = isinstance(event.args[1], (CaptureNode, type(None)))
        return signal_type_check and node_type_check

    def event_handler(self, event: PyTransEvent):
        working_doc = self.listener_hub.main.model_hub.working_doc
        if working_doc == None:
            return
        self.main.view_hub.update_all(event.args[0], event.args[1])
        self.main.mainwindow_event_obj.force_run(QResizeEvent(QSize(), QSize()))

        return super().event_handler(event)


class SignalUIUpdate(Listener):
    def listened_event(self, event: PyTransEvent) -> bool:
        if event.type != event.Type.UI_UPDATE:
            return False
        if event.args.__len__() != 1:
            return False
        signal_type_check = event.args[0] in ViewController.UpdateSignal
        return signal_type_check

    def event_handler(self, event: PyTransEvent):
        self.main.view_hub.update_all(event.args[0])
        self.main.mainwindow_event_obj.force_run(QResizeEvent(QSize(), QSize()))

        return super().event_handler(event)
