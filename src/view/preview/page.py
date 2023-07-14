from enum import Enum, auto

from PIL.ImageQt import ImageQt

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from model.doc import WorkingDoc

import my_utils.preview_utils as preview_utils

from typing import TYPE_CHECKING

from view.preview.capture_box import CaptureBoxItem

if TYPE_CHECKING:
    from view.preview.preview_hub import PreviewHub


class PageItem(QGraphicsPixmapItem):
    def bind(self, preview_hub: "PreviewHub", working_doc: WorkingDoc):
        self.working_doc = working_doc
        self.preview_hub = preview_hub
        self.creating_box: QGraphicsRectItem = None
        self.start_pos: QPointF = None
        self.end_pos: QPointF = None
        self.rawuuid2capture = dict[bytes, CaptureBoxItem]()

        self.setFlag(self.GraphicsItemFlag.ItemClipsChildrenToShape, True)
        return self

    def load_page_captures(self, page_index: int):
        visual_orms = (
            self.working_doc.get_orm_query(self.working_doc.ORM.VisualORM)
            .filter_by(page_no=page_index)
            .all()
        )
        for orm in visual_orms:
            self.rawuuid2capture[orm.capture_uuid] = CaptureBoxItem().bind(
                self.preview_hub, None, orm.capture_uuid
            )

    def update_captures(self, *raw_uuids):
        for raw_uuid in raw_uuids:
            orm = self.working_doc.get_visual_info(raw_uuid, True)
            if orm == None:
                if raw_uuid not in self.rawuuid2capture:  # no orm, no item -> pass
                    continue
                item = self.rawuuid2capture[raw_uuid]  # no orm, have item -> remove
                if isinstance(item, QGraphicsItem):
                    item.setParentItem(None)
                del self.rawuuid2capture[raw_uuid]  # remove record
            else:
                if raw_uuid not in self.rawuuid2capture:  # have orm, no item-> create
                    self.rawuuid2capture[raw_uuid] = CaptureBoxItem().bind(
                        self.preview_hub, None, raw_uuid
                    )
                else:  # have orm, have item -> self update
                    self.rawuuid2capture[raw_uuid].self_update()

    def mousePressEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.setSelected(True)
        for item in self.childItems():
            item.setSelected(False)
        if self.preview_hub.preview_control.create_btn.isChecked():  # TODO:MODE SELECT
            self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.creating_box = QGraphicsRectItem(
                preview_utils.limit_rect(
                    preview_utils.rect_from_2point(self.start_pos, self.end_pos),
                    self.preview_hub.page_item.boundingRect(),
                ),
                self,
            )
            preview_utils.update_box_preview(
                self.preview_hub, self.creating_box.rect(), True
            )
        else:
            event.setAccepted(False)

    def mouseMoveEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.end_pos = event.pos()
        self.creating_box.setRect(
            preview_utils.limit_rect(
                preview_utils.rect_from_2point(self.start_pos, self.end_pos),
                self.preview_hub.page_item.boundingRect(),
            )
        )
        preview_utils.update_box_preview(
            self.preview_hub, self.creating_box.rect(), True
        )
        event.accept()

    def mouseReleaseEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        page_size = self.pixmap().rect()
        box_rect = preview_utils.rect_from_2point(self.start_pos, self.end_pos)
        ratio_rect = preview_utils.map_rect_to_ratio(box_rect, page_size)
        if ratio_rect.width() > 0.01 and ratio_rect.height() > 0.01:
            self.preview_hub.add_capture_box(
                ratio_rect.left(),
                ratio_rect.top(),
                ratio_rect.right(),
                ratio_rect.bottom(),
                second_selection=event.button() == Qt.MouseButton.RightButton,
            )
        preview_utils.update_box_preview(
            self.preview_hub, self.creating_box.rect(), unmount=True
        )
        self.preview_hub.scene.removeItem(self.creating_box)
        self.creating_box = None
        event.accept()
