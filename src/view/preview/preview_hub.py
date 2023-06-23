from typing import Callable
from listener.listener_hub import Listener, ListenerHub, PyTransEvent
from model.capture.capture_node import CapNodeType, CaptureNode
from model.doc import WorkingDoc
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from typing import TYPE_CHECKING
from my_utils.utils import PIL2QPixmap, find_render_node

from view.preview.capture_box import CaptureBoxItem, ResizeIconItem
from view.preview.page import PageItem
from view.preview.preview_control import PreviewControl
from view.view_hub import ViewHub, ViewController

if TYPE_CHECKING:
    from view.view_hub import ViewHub


class PreviewHub(ViewController):
    def __init__(self, view_hub: ViewHub) -> None:
        super().__init__(view_hub)

        self.working_doc: WorkingDoc = None

        self.scene = QGraphicsScene()
        self.capture_preview_scene = QGraphicsScene()
        self.page_item: QGraphicsPixmapItem = None
        self.gview = self.view_hub.ui.previewImage
        self.capture_gview = self.view_hub.ui.capturePreviewImage
        self.current_select_capmode = CapNodeType.TEXT
        # init
        self.static_init()
        self.preview_control = PreviewControl(self)
        self.working_status_checking()

    def static_init(self):
        self.gview.setScene(self.scene)
        self.capture_gview.setScene(self.capture_preview_scene)
        ui = self.view_hub.ui

        ui.zoomFitButton.clicked.connect(lambda x: self.zoom())
        ui.zoomInButton.clicked.connect(lambda x: self.zoom(True))
        ui.zoomOutButton.clicked.connect(lambda x: self.zoom(False))
        self.view_hub.main.mainwindow_event_obj.add_callback(
            QResizeEvent, lambda x: self.zoom()
        )
        ui.zoomFitButton.setChecked(True)

        ui.previewPrevButton.clicked.connect(lambda x: self.change_page(False))
        ui.previewNextButton.clicked.connect(lambda x: self.change_page(True))

        for cap_type in CapNodeType:
            if cap_type == cap_type.ROOT:
                continue
            ui.captureSelectCombo.addItem(cap_type.name, cap_type)
        ui.captureSelectCombo.setCurrentText(CapNodeType.TEXT.name)

        self.scale_factor = 1.25

    def add_capture_box(self, left, top, right, bottom, second_selection=False):
        tmp_node = CaptureNode(
            self.working_doc,
            self.preview_control.selected_nodetype
            if not second_selection
            else self.preview_control.selected_nodetype_second,
        ).link_parent(self.working_doc.focus_node)
        tmp_node.set_visual_memo(
            tmp_node.VisualMemo(
                left=left,
                top=top,
                right=right,
                bottom=bottom,
                page_no=self.working_doc.page_no,
            )
        )
        self.view_hub.main.listener_hub.post_event(
            PyTransEvent(PyTransEvent.Type.UI_UPDATE)
        )

    def zoom(self, zoom_in: bool = None):
        if self.page_item == None:
            return
        fit_in_view_btn = self.view_hub.ui.zoomFitButton
        if zoom_in == None and fit_in_view_btn.isChecked():
            self.scene.setSceneRect(self.page_item.boundingRect())
            self.gview.fitInView(
                self.page_item.boundingRect(), mode=Qt.AspectRatioMode.KeepAspectRatio
            )
        elif zoom_in == True:
            fit_in_view_btn.setChecked(False)
            self.gview.scale(self.scale_factor, self.scale_factor)
        elif zoom_in == False:
            fit_in_view_btn.setChecked(False)
            self.gview.scale(1 / self.scale_factor, 1 / self.scale_factor)

        for item in [x for x in self.scene.items() if isinstance(x, ResizeIconItem)]:
            item.self_update_pos()

    def change_page(self, forward=True):
        if forward:
            self.working_doc.page_no += 1
        else:
            self.working_doc.page_no -= 1
        self.working_doc.page_no = max(
            0, min(self.working_doc.page_cache.__len__() - 1, self.working_doc.page_no)
        )
        self.view_hub.main.listener_hub.post_event(
            PyTransEvent(PyTransEvent.Type.UI_UPDATE)
        )

    def page_indic_update(self):
        if self.working_doc == None:
            self.view_hub.ui.previewPageMeter.setText("")
        else:
            self.view_hub.ui.previewPageMeter.setText(
                f"{self.working_doc.page_no+1}/{self.working_doc.page_cache.__len__()}"
            )

    def working_status_checking(self):
        ui = self.view_hub.ui
        valid_flag_1 = (
            self.working_doc != None
            and self.working_doc.status != self.working_doc.STATUS.NOT_AVALIABLE
        )

        ui.zoomFitButton.setEnabled(valid_flag_1)
        ui.zoomInButton.setEnabled(valid_flag_1)
        ui.zoomOutButton.setEnabled(valid_flag_1)
        ui.previewPrevButton.setEnabled(valid_flag_1)
        ui.previewNextButton.setEnabled(valid_flag_1)

        return valid_flag_1

    def update(self, signal=ViewController.UpdateSignal.UPDATE_ALL, *args, **kwargs):
        if signal == ViewController.UpdateSignal.UPDATE_ALL:
            working_doc = self.view_hub.main.model_hub.working_doc
            # preview cleanup
            for item in self.scene.items():
                self.scene.removeItem(item)
            self.working_doc = working_doc
            if self.working_status_checking():
                self.page_indic_update()
                # page
                page_img = working_doc.page_cache[working_doc.page_no]
                self.page_item = PageItem(PIL2QPixmap(page_img), None).bind(self)
                self.scene.addItem(self.page_item)
                # capture node
                root_node = working_doc.root_node
                render_nodes = find_render_node(root_node, working_doc.page_no)
                for item in render_nodes:
                    CaptureBoxItem(self.page_item).bind(self, item)
                self.working_status_checking()
        elif signal == ViewController.UpdateSignal.UPDATE_FOCUS:
            try:
                node: CaptureNode = args[0]
                for item in self.scene.items():
                    item.setSelected(False)
                memo = node.get_visual_memo()
                working_doc = self.view_hub.main.model_hub.working_doc
                working_doc.page_no = memo.page_no
                self.update()
                for item in self.scene.items():
                    if isinstance(item, CaptureBoxItem):
                        item.setSelected(node == item.capture_node)
            finally:
                return
