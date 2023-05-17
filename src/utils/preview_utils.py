from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from view.preview.preview_hub import PreviewHub


def map_rect_to_ratio(rect: QRectF, page_rect: QRectF):
    return QRectF(
        QPointF(rect.left()/page_rect.width(), rect.top()/page_rect.height()),
        QPointF(rect.right()/page_rect.width(), rect.bottom()/page_rect.height()),
    )


def map_rect_from_ratio(ratio_rect: QRectF, page_rect: QRectF):
    return QRectF(
        QPointF(ratio_rect.left()*page_rect.width(), ratio_rect.top()*page_rect.height()),
        QPointF(ratio_rect.right()*page_rect.width(), ratio_rect.bottom()*page_rect.height()),
    )


def rect_from_2point(p1: QPointF, p2: QPointF):
    return QRectF(
        QPointF(min(p1.x(), p2.x()), min(p1.y(), p2.y())),
        QPointF(max(p1.x(), p2.x()), max(p1.y(), p2.y())),
    )


def limit_rect(rect: QRectF, bounding: QRectF, offset_pos: QPointF = None):
    offset_pos = QPointF(0, 0) if offset_pos == None else offset_pos
    bounding = QRectF(bounding.topLeft()-offset_pos, bounding.bottomRight()-offset_pos)
    return QRectF(
        QPointF(max(rect.left(), bounding.left()), max(rect.top(), bounding.top())),
        QPointF(min(rect.right(), bounding.right()), min(rect.bottom(), bounding.bottom()))
    )


def limit_point(point: QPointF, bounding: QRectF, offset_pos: QPointF = QPointF(0, 0)):
    bounding = QRectF(bounding.topLeft()-offset_pos, bounding.bottomRight()-offset_pos)
    return QPointF(
        min(max(point.x(), bounding.left()), bounding.right()),
        min(max(point.y(), bounding.top()), bounding.bottom())
    )


def update_box_preview(preview_hub: 'PreviewHub', rect: QRectF, mount=False, unmount=False):
    items = preview_hub.capture_preview_scene.items()
    if mount:
        for t in items:
            preview_hub.capture_preview_scene.removeItem(t)
        preview_hub.capture_preview_scene.addItem(QGraphicsPixmapItem())
        items = preview_hub.capture_preview_scene.items()
    elif unmount:
        for t in items:
            preview_hub.capture_preview_scene.removeItem(t)
        return
    if(items.__len__() == 0 or not isinstance(items[0], QGraphicsPixmapItem)):
        return
    preview_item = items[0]
    preview_item.setPixmap(preview_hub.page_item.pixmap().copy(rect.toRect()))
    preview_hub.capture_preview_scene.setSceneRect(preview_item.boundingRect())
    preview_hub.capture_gview.fitInView(
        preview_item, Qt.AspectRatioMode.KeepAspectRatio)
