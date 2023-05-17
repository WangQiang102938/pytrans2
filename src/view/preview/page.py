from enum import Enum, auto
import typing

from PIL.ImageQt import ImageQt

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import view.preview.preview_hub as preview_hub_m
import utils.preview_utils as preview_utils


class PageItem(QGraphicsPixmapItem):
    def bind(self, preview_hub: preview_hub_m.PreviewHub):
        self.preview_hub = preview_hub
        self.creating_box: QGraphicsRectItem = None
        self.start_pos: QPointF = None
        self.end_pos: QPointF = None
        self.setFlag(self.GraphicsItemFlag.ItemClipsChildrenToShape, True)
        return self

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.setSelected(True)
        for item in self.childItems():
            item.setSelected(False)
        if(True):  # TODO:MODE SELECT
            self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.creating_box = QGraphicsRectItem(
                preview_utils.limit_rect(
                    preview_utils.rect_from_2point(
                        self.start_pos, self.end_pos
                    ), self.preview_hub.page_item.boundingRect()
                ), self
            )
            preview_utils.update_box_preview(self.preview_hub,self.creating_box.rect(),True)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.end_pos = event.pos()
        self.creating_box.setRect(
            preview_utils.limit_rect(
                preview_utils.rect_from_2point(
                    self.start_pos, self.end_pos
                ), self.preview_hub.page_item.boundingRect()
            )
        )
        preview_utils.update_box_preview(self.preview_hub,self.creating_box.rect(),True)
        event.accept()

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        page_size = self.pixmap().rect()
        box_rect = preview_utils.rect_from_2point(self.start_pos, self.end_pos)
        ratio_rect = preview_utils.map_rect_to_ratio(box_rect, page_size)
        if(ratio_rect.width() > 0.01 and ratio_rect.height() > 0.01):
            self.preview_hub.add_capture_box(
                ratio_rect.left(),
                ratio_rect.top(),
                ratio_rect.right(),
                ratio_rect.bottom()
            )
        preview_utils.update_box_preview(self.preview_hub,self.creating_box.rect(),unmount=True)
        self.preview_hub.scene.removeItem(self.creating_box)
        self.creating_box = None
        event.accept()
