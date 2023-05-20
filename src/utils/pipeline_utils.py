from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from typing import *

T=TypeVar("T",bound=QWidget)

class FormItem(QGroupBox):
    def setup(self, title: str,layout:QLayout=None):
        self.setTitle(title)

        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)
        self.v_layout.setContentsMargins(2, 2, 2, 2)
        # self.adjustSize()
        # self.setStyleSheet('border:1px solid yellow')

        if isinstance(layout,QLayout):
            layout.addWidget(self)
        return self

    def set_content(self,content:T)->T:
        self.v_layout.addWidget(content)
        return content

def add_to_layout(layout:QLayout,widget:T):
    layout.addWidget(widget)
    return widget
