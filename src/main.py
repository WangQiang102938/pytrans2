from view.view_hub import ViewHub
from controller.controller_hub import ControllerHub
from typing import TYPE_CHECKING, Callable
from controller.io.local_pdf import LocalPDFOpener
from model.data_hub import ModelHub
from listener.listener_hub import ListenerHub
from view.ui import Ui_MainWindow
from enum import Enum, auto
import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

sys.path.insert(0, os.path.split(__file__)[0])


class PyTransApp:
    def __init__(self) -> None:
        # sys.argv+=['-platform', 'windows:darkmode=2']
        self.app = QApplication(sys.argv)
        self.mainwindow = QMainWindow()

        self.ui = Ui_MainWindow()
        self.app.setStyle("Fusion")

        self.ui.setupUi(self.mainwindow)

        self.controller_hub = ControllerHub(self)
        self.view_hub = ViewHub(self)
        self.listener_hub = ListenerHub(self)
        self.model_hub = ModelHub(self)

        self.resize_callbacks = list[Callable[[QResizeEvent], None]]()
        self.origin_resize_call = self.mainwindow.resizeEvent
        self.mainwindow.resizeEvent = self.g_resize_call

    def start_gui(self):
        self.mainwindow.show()
        QTimer.singleShot(0, self.debug_call)
        self.app.exec()

    def debug_call(self):
        self.controller_hub.io_hub.open_doc(
            LocalPDFOpener('./test.pdf')
        )
        return

    def g_resize_call(self, event: QResizeEvent):
        for callback in self.resize_callbacks:
            callback(event)
        self.origin_resize_call(event)


if __name__ == '__main__':
    app = PyTransApp()

    app.start_gui()
