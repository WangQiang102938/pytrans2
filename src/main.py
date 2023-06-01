from my_utils import qt_utils
from view.view_hub import ViewHub
from controller.controller_hub import ControllerHub
from typing import TYPE_CHECKING, Callable
from controller.io.local_pdf import LocalPDFModule
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
        self.mainwindow_event_obj = qt_utils.EventQObj().post_init()
        self.mainwindow.installEventFilter(self.mainwindow_event_obj)

        self.ui = Ui_MainWindow()
        self.app.setStyle("Fusion")

        self.ui.setupUi(self.mainwindow)
        self.resize_callbacks = list[Callable[[QResizeEvent], None]]()

        self.controller_hub = ControllerHub(self)
        self.view_hub = ViewHub(self)
        self.listener_hub = ListenerHub(self)
        self.model_hub = ModelHub(self)

    def start_gui(self):
        self.mainwindow.show()
        QTimer.singleShot(0, self.debug_call)
        self.app.exec()

    def debug_call(self):
        # LocalPDFModule.valid_ins.open('test.pdf')
        pipeline = [
            "Standard Crop",
            "Tesseract OCR",
            "StdFormatter",
            "Google Translate",
            "HTML Gen V1",
        ]
        from controller.pipeline.pipeline_hub import PipelineNode

        ins = dict[str, PipelineNode]()
        for i, item in enumerate(pipeline):
            self.ui.pipeAvaliableCombo.setCurrentText(item)
            self.ui.PipeAddBtn.click()
            self.app.processEvents()
            ins[item] = self.ui.pipeEditList.item(i).data(Qt.ItemDataRole.UserRole)
        from controller.pipeline.translator.google_app_script.google_trans import (
            GoogleTranslate,
        )

        google_trans_ins: GoogleTranslate = ins["Google Translate"]
        google_trans_ins.option_widget.api_key_edit.setText(
            "AIzaSyChnruvHGwwc9s0svK9HgTQd1TL_hG0anQ"
        )
        ins["Tesseract OCR"].link_info["input image"] = (
            ins["Standard Crop"],
            "Image out",
        )
        ins["StdFormatter"].link_info["in:str"] = (ins["Tesseract OCR"], "output text")
        ins["Google Translate"].link_info["in:[[str]]"] = (
            ins["StdFormatter"],
            "out:[[str]]",
        )
        ins["HTML Gen V1"].link_info["image_in:Image"] = (
            ins["Standard Crop"],
            "Image out",
        )
        ins["HTML Gen V1"].link_info["translated_in:[[str]]"] = (
            ins["Google Translate"],
            "out:[[str]]",
        )
        ins["HTML Gen V1"].link_info["origin_in:[[str]]"] = (
            ins["StdFormatter"],
            "out:[[str]]",
        )
        return


if __name__ == "__main__":
    app = PyTransApp()

    app.start_gui()
