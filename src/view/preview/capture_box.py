from enum import Enum, auto
import typing

from PIL.ImageQt import ImageQt
from PyQt6 import QtCore, QtGui

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from typing import TYPE_CHECKING, Any

from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)
from listener.listener_hub import PyTransEvent

from model.capture.capture_node import CapNodeType, CaptureNode
import my_utils.preview_utils as preview_utils

if TYPE_CHECKING:
    from view.preview.preview_hub import PreviewHub

cap_type_color_map = {CapNodeType.IMAGE: (0, 128, 0, 128)}


class CaptureBoxItem(QGraphicsRectItem):
    def bind(self, preview_hub: "PreviewHub", node: CaptureNode):
        self.preview_hub = preview_hub
        self.capture_node = node

        self.preview_item: QGraphicsPixmapItem = QGraphicsPixmapItem()
        # init
        self.setFlag(self.GraphicsItemFlag.ItemIsFocusable, True)
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.page_rect = QRectF(preview_hub.page_item.pixmap().rect())
        self.node_info = node.get_visual_memo()
        self.setRect(
            preview_utils.map_rect_from_ratio(
                QRectF(
                    QPointF(self.node_info.left, self.node_info.top),
                    QPointF(self.node_info.right, self.node_info.bottom),
                ),
                self.page_rect,
            )
        )
        self.resize_icons = [
            ResizeIconItem().bind(self, True, True),
            ResizeIconItem().bind(self, True, False),
            ResizeIconItem().bind(self, False, True),
            ResizeIconItem().bind(self, False, False),
        ]
        for item in self.resize_icons:
            item.setVisible(False)
        return self

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change == self.GraphicsItemChange.ItemSelectedChange and value == 1:
            return super().itemChange(change, self.item_will_selected())
        if change == self.GraphicsItemChange.ItemSelectedChange and value == 0:
            return super().itemChange(change, self.item_will_unselected())
        if self.isSelected():
            if change == self.GraphicsItemChange.ItemPositionChange:
                offset_pos: QPointF = value
                box_rect = self.rect()
                page_rect = QRectF(self.preview_hub.page_item.pixmap().rect())
                x = min(
                    max(0 - box_rect.left(), offset_pos.x()),
                    page_rect.right() - box_rect.right(),
                )
                y = min(
                    max(0 - box_rect.top(), offset_pos.y()),
                    page_rect.bottom() - box_rect.bottom(),
                )
                self.update_box_preview()
                return QPointF(x, y)
        return super().itemChange(change, value)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
            self.delete_me()
        return super().keyPressEvent(event)

    def item_will_selected(self):
        if self.capture_node.node_type in cap_type_color_map:
            self.setBrush(QColor(*cap_type_color_map[self.capture_node.node_type]))
        else:
            self.setBrush(QColor(128, 128, 128, 128))
        for item in self.resize_icons:
            item.setVisible(True)
        self.update_box_preview(mount=True)
        return 1

    def item_will_unselected(self):
        ratio_rect = preview_utils.map_rect_to_ratio(
            QRectF(
                self.rect().topLeft() + self.pos(),
                self.rect().bottomRight() + self.pos(),
            ),
            QRectF(self.preview_hub.page_item.pixmap().rect()),
        )
        self.capture_node.get_visual_memo().update(
            left=ratio_rect.left(),
            top=ratio_rect.top(),
            right=ratio_rect.right(),
            bottom=ratio_rect.bottom(),
        )
        self.update_box_preview(unmount=True)
        # after

        # TODO: Make it to event
        # test_pipe = self.preview_hub.view_hub.main.controller_hub.pipeline_hub.pipeline_nodes[0]
        # test_pipe.process_node(self.capture_node,update_flag=True)

        for item in self.resize_icons:
            item.setVisible(False)
        self.setBrush(QColor(0, 0, 0, 0))
        return 0

    def resize(
        self,
        anchor_pos: QPointF,
        diagnal_pos: QPointF,
        start_pos: QPointF,
        end_pos: QPointF,
    ):
        self.setRect(
            preview_utils.limit_rect(
                preview_utils.rect_from_2point(
                    diagnal_pos, anchor_pos - start_pos + end_pos
                ),
                QRectF(self.preview_hub.page_item.pixmap().rect()),
                offset_pos=self.pos(),
            )
        )
        for item in self.resize_icons:
            item.self_update_pos()
        self.update_box_preview()

    def update_box_preview(self, mount=False, unmount=False):
        if mount:
            for t in self.preview_hub.capture_preview_scene.items():
                self.preview_hub.capture_preview_scene.removeItem(t)
            self.preview_hub.capture_preview_scene.addItem(self.preview_item)
        elif unmount:
            self.preview_hub.capture_preview_scene.removeItem(self.preview_item)
            return
        box_rect = self.rect()
        box_rect = QRectF(
            box_rect.topLeft() + self.pos(), box_rect.bottomRight() + self.pos()
        )
        self.preview_item.setPixmap(
            self.preview_hub.page_item.pixmap().copy(box_rect.toRect())
        )
        self.preview_hub.capture_preview_scene.setSceneRect(
            self.preview_item.boundingRect()
        )
        self.preview_hub.capture_gview.fitInView(
            self.preview_item, Qt.AspectRatioMode.KeepAspectRatio
        )

    def delete_me(self):
        parent_node = self.capture_node.parent
        parent_node.children.remove(self.capture_node)
        self.preview_hub.view_hub.main.listener_hub.post_event(
            PyTransEvent(PyTransEvent.Type.UI_UPDATE)
        )


class ResizeIconItem(QGraphicsEllipseItem):
    def bind(self, box: CaptureBoxItem, left_flag=True, top_flag=True):
        self.box = box
        self.left_flag = left_flag
        self.top_flag = top_flag
        self.setParentItem(box)
        self.setFlag(self.GraphicsItemFlag.ItemIsFocusable, True)
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.self_update_pos()

        self.setBrush(QColor(0, 0, 0, 255))
        return self

    def self_update_pos(self):
        box_rect = self.box.rect()
        gview = self.box.preview_hub.gview
        self.setPos(
            box_rect.left() if self.left_flag else box_rect.right(),
            box_rect.top() if self.top_flag else box_rect.bottom(),
        )
        view_diff = gview.mapToScene(QPoint(5, 5)) - gview.mapToScene(QPoint(0, 0))
        self.setRect(QRectF(-view_diff, view_diff))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.start_pos = event.scenePos()
        self.end_pos = event.scenePos()
        self.anchor_pos = self.pos()
        self.diagnal_pos = None
        for item in self.box.resize_icons:
            if item.left_flag != self.left_flag and item.top_flag != self.top_flag:
                self.diagnal_pos = item.pos()
        event.accept()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.end_pos = preview_utils.limit_point(
            event.scenePos(), QRectF(self.box.preview_hub.page_item.pixmap().rect())
        )
        self.box.resize(self.anchor_pos, self.diagnal_pos, self.start_pos, self.end_pos)
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        return super().mouseReleaseEvent(event)
