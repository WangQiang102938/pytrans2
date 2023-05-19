from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class FormItem(QFrame):
    def setup(self, title: str, content: QWidget):
        self.h_layout = QHBoxLayout(self)
        self.title_label = QLabel(title, self)
        self.content = content
        self.content.setParent(self)

        self.h_layout.addWidget(self.title_label)
        self.h_layout.addWidget(self.content)

        self.title_label.setSizePolicy(
            QSizePolicy(
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Minimum
            )
        )
        self.content.setSizePolicy(
            QSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum
            )
        )
        self.h_layout.setContentsMargins(2, 2, 2, 2)
        # self.setStyleSheet('border:1px solid red')
        return self
