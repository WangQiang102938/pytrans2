from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from typing import TYPE_CHECKING, Any
from view.preview.capture_box import CapNodeType
from my_utils import qt_utils

if TYPE_CHECKING:
    from view.preview.preview_hub import PreviewHub


class PreviewControl:
    def __init__(self, preview_hub: "PreviewHub") -> None:
        self.preview_hub = preview_hub
        self.container = preview_hub.view_hub.ui.captureControlCon
        qt_utils.qwidget_cleanup(self.container)
        self.container.setLayout(
            QHBoxLayout()
            if self.container.layout() == None
            else self.container.layout()
        )
        self.selected_nodetype = CapNodeType.TEXT
        self.selected_nodetype_second = CapNodeType.IMAGE

        main_layout = self.container.layout()
        main_layout.setContentsMargins(2, 2, 2, 2)

        # create btn
        self.create_btn = qt_utils.add_to_layout(main_layout, QPushButton())
        self.create_btn.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Expanding)
        self.create_btn.setCheckable(True)
        self.create_btn.setText("+ Create +")

        # type btns
        self.type_btns = dict[CapNodeType, CapnodeSelectBtn]()
        self.type_btn_con = qt_utils.add_to_layout(main_layout, QGroupBox())
        self.type_btn_con.setLayout(QHBoxLayout())
        self.type_btn_con.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Expanding)
        type_btn_layout = self.type_btn_con.layout()
        type_btn_layout.setContentsMargins(2, 2, 2, 2)

        # self.type_btn_con.setStyleSheet("padding:10px")
        for node_type in CapNodeType:
            if node_type == node_type.ROOT:
                continue
            type_btn = qt_utils.add_to_layout(
                type_btn_layout, CapnodeSelectBtn().bind(self, node_type)
            )
            type_btn.update_selection()
            # type_btn.setText(node_type.name)
            # func = lambda clicked, node_type=node_type: self.node_type_changed(
            #     node_type
            # )
            # type_btn.clicked.connect(func)
            # type_btn.setCheckable(True)
            self.type_btns[node_type] = type_btn
        type_btn_layout.addItem(qt_utils.gen_spacer(False))

        # post init
        self.create_btn.clicked.connect(
            lambda checked: (
                self.type_btn_con.setEnabled(self.create_btn.isChecked()),
                self.create_btn.setStyleSheet(
                    "background-color: rgba(0,128,0,128)" if checked else ""
                ),
            )
        )

        self.create_btn.clicked.emit()
        # self.node_type_changed(self.selected_nodetype)

    # def node_type_changed(self, node_type: CapNodeType):
    #     self.selected_nodetype = node_type
    #     for key, btn in self.type_btns.items():
    #         if key == node_type:
    #             btn.setChecked(True)
    #             btn.setStyleSheet("background-color: rgba(0,128,0,128)")
    #         else:
    #             btn.setChecked(False)
    #             btn.setStyleSheet("")

    def get_create_status(self):
        return self.create_btn.isChecked()


class CapnodeSelectBtn(QToolButton):
    def bind(self, control: PreviewControl, node_type: CapNodeType):
        self.node_type = node_type
        self.setText(node_type.name)
        self.control = control
        self.left_selected = False
        self.right_selected = False
        self.setCheckable(True)
        return self

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.control.selected_nodetype = self.node_type
        elif a0.button() == Qt.MouseButton.RightButton:
            self.control.selected_nodetype_second = self.node_type
        for item in self.control.type_btns.values():
            item.update_selection()
        return super().mousePressEvent(a0)

    def update_selection(self):
        left = self.control.selected_nodetype == self.node_type
        right = self.control.selected_nodetype_second == self.node_type
        if not left and not right:
            self.setChecked(False)
            self.setStyleSheet("")
        elif left and right:
            self.setChecked(True)
            self.setStyleSheet("background-color: rgba(0,128,128,128)")
        elif left:
            self.setChecked(True)
            self.setStyleSheet("background-color: rgba(0,128,0,128)")
        elif right:
            self.setChecked(True)
            self.setStyleSheet("background-color: rgba(0,0,128,128)")
