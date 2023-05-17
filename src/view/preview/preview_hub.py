from typing import Callable
from listener.listener_hub import PyTransEvent
from model.capture.capture_node import CaptureNode
from model.doc import WorkingDoc
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from typing import TYPE_CHECKING

from view.preview.capture_box import ResizeIconItem

if TYPE_CHECKING:
    from view.view_hub import ViewHub


class PreviewHub:
    def __init__(self, view_hub: 'ViewHub') -> None:
        self.view_hub = view_hub
        self.working_doc: WorkingDoc = None

        self.scene = QGraphicsScene()
        self.capture_preview_scene = QGraphicsScene()
        self.page_item: QGraphicsPixmapItem = None
        self.gview = self.view_hub.ui.previewImage
        self.capture_gview = self.view_hub.ui.capturePreviewImage
        # init
        self.gview.setScene(self.scene)
        self.capture_gview.setScene(self.capture_preview_scene)
        ui = self.view_hub.ui
        ui.zoomFitButton.clicked.connect(lambda x: self.zoom())
        ui.zoomInButton.clicked.connect(lambda x: self.zoom(True))
        ui.zoomOutButton.clicked.connect(lambda x: self.zoom(False))
        ui.previewPrevButton.clicked.connect(lambda x: self.change_page(False))
        ui.previewNextButton.clicked.connect(lambda x: self.change_page(True))
        self.scale_factor = 1.25

        self.working_status_checking()

    def add_capture_box(self, left, top, right, bottom):
        # TODO: COMPLETE THIS
        tmp_node = self.working_doc.curr_node_cls().link_parent(
            self.working_doc.focus_node
        )
        tmp_node.set_visual_memo(
            tmp_node.VisualMemo(
                left=left,
                top=top,
                right=right,
                bottom=bottom,
                page_no=self.working_doc.page_no
            )
        )
        self.view_hub.main.listener_hub.event_inqueue(
            PyTransEvent(PyTransEvent.Type.UI_UPDATE)
        )

    def zoom(self, zoom_in: bool = None):
        if zoom_in == None:
            self.scene.setSceneRect(self.page_item.boundingRect())
            self.gview.fitInView(self.page_item.boundingRect(
            ), mode=Qt.AspectRatioMode.KeepAspectRatio)
        elif zoom_in == True:
            self.gview.scale(self.scale_factor, self.scale_factor)
        elif zoom_in == False:
            self.gview.scale(1/self.scale_factor, 1/self.scale_factor)

        for item in [x for x in self.scene.items() if isinstance(x, ResizeIconItem)]:
            item.self_update_pos()

    def change_page(self, forward=True):
        if forward:
            self.working_doc.page_no += 1
        else:
            self.working_doc.page_no -= 1
        self.working_doc.page_no = max(
            0, min(self.working_doc.page_cache.__len__()-1, self.working_doc.page_no))
        self.view_hub.main.listener_hub.event_inqueue(
            PyTransEvent(PyTransEvent.Type.UI_UPDATE)
        )

    def page_indic_update(self):
        if (self.working_doc == None):
            self.view_hub.ui.previewPageMeter.setText("")
        else:
            self.view_hub.ui.previewPageMeter.setText(
                f"{self.working_doc.page_no+1}/{self.working_doc.page_cache.__len__()}")

    def working_status_checking(self):
        ui = self.view_hub.ui
        valid_flag_1 = (self.working_doc != None and self.working_doc.status !=
                        self.working_doc.STATUS.NOT_AVALIABLE)

        ui.zoomFitButton.setEnabled(valid_flag_1)
        ui.zoomInButton.setEnabled(valid_flag_1)
        ui.zoomOutButton.setEnabled(valid_flag_1)
        ui.previewPrevButton.setEnabled(valid_flag_1)
        ui.previewNextButton.setEnabled(valid_flag_1)

        return valid_flag_1
