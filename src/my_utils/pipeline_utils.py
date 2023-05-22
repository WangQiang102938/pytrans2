from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from typing import *

T=TypeVar("T",bound=QWidget)

class FormItem(QGroupBox):
    def setup(self, title: str,layout:QLayout=None,horizon_flag=False):
        self.setTitle(title)

        self.this_layout =QHBoxLayout() if horizon_flag else QVBoxLayout()
        self.setLayout(self.this_layout)
        self.this_layout.setContentsMargins(2, 2, 2, 2)
        # self.adjustSize()
        # self.setStyleSheet('border:1px solid yellow')
        self.contents=list[QWidget]()

        if isinstance(layout,QLayout):
            layout.addWidget(self)
        return self

    def add_content(self,content:T)->T:
        self.contents.append(content)
        self.this_layout.addWidget(content)
        return content

    def add_content_chain(self,content:T):
        self.contents.append(content)
        self.this_layout.addWidget(content)
        return content,self

def add_to_layout(layout:QLayout,widget:T)->T:
    layout.addWidget(widget)
    return widget

def gen_vert_spacer():
    return QSpacerItem(1,1,
        QSizePolicy.Policy.Minimum,
        QSizePolicy.Policy.Expanding,
    )
