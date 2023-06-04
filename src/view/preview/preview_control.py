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
        self.current_nodetype = CapNodeType.TEXT

        main_layout = self.container.layout()
        main_layout.setContentsMargins(2, 2, 2, 2)

        # create btn
        self.create_btn = qt_utils.add_to_layout(main_layout, QPushButton())
        self.create_btn.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Expanding)
        self.create_btn.setCheckable(True)
        self.create_btn.setText("+ Create +")

        # type btns
        self.type_btns = dict[CapNodeType, QToolButton]()
        self.type_btn_con = qt_utils.add_to_layout(main_layout, QGroupBox())
        self.type_btn_con.setLayout(QHBoxLayout())
        self.type_btn_con.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Expanding)
        type_btn_layout = self.type_btn_con.layout()
        type_btn_layout.setContentsMargins(2, 2, 2, 2)

        # self.type_btn_con.setStyleSheet("padding:10px")
        for node_type in CapNodeType:
            if node_type == node_type.ROOT:
                continue
            type_btn = qt_utils.add_to_layout(type_btn_layout, QToolButton())
            type_btn.setText(node_type.name)
            func = lambda clicked, node_type=node_type: self.node_type_changed(
                node_type
            )
            type_btn.clicked.connect(func)
            type_btn.setCheckable(True)
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
        self.node_type_changed(self.current_nodetype)

    def node_type_changed(self, node_type: CapNodeType):
        self.current_nodetype = node_type
        for key, btn in self.type_btns.items():
            if key == node_type:
                btn.setChecked(True)
                btn.setStyleSheet("background-color: rgba(0,128,0,128)")
            else:
                btn.setChecked(False)
                btn.setStyleSheet("")

    def get_create_status(self):
        return self.create_btn.isChecked()
