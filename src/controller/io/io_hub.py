from enum import Enum, auto
from typing import Callable
from model.doc import WorkingDoc
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from typing import TYPE_CHECKING

import my_utils

if TYPE_CHECKING:
    from controller.controller_hub import ControllerHub


class IOHub:
    class OPEN_MODE(Enum):
        RAW = auto()
        LOCAL_PDF = auto()
        ONLINE_PDF = auto()

    def __init__(self, ctrl_hub: "ControllerHub") -> None:
        self.ctrl_hub = ctrl_hub
        ui=self.ctrl_hub.ui
        io_module_clses = my_utils.scan_class(my_utils.split_dir_from_file(__file__),IOModule)
        self.io_modules=[x(self) for x in io_module_clses]
        for module in self.io_modules:
            ui.ioModuleTab.addTab(module.get_widget(),module.get_title())

    def add_doc(self, doc: WorkingDoc, set_to_work_flag=True):
        self.ctrl_hub.main.model_hub.add_doc(doc)

    def ui_lock(self,enable=True):
        main=self.ctrl_hub.main
        main.mainwindow.setEnabled(enable)
        main.app.processEvents()


class IOModule:
    def __init__(self, io_hub: IOHub) -> None:
        self.io_hub = io_hub

    def get_widget(self) -> QWidget:
        pass

    def get_pdf_path(self, working_doc: WorkingDoc):
        return None

    def get_title(self):
        return self.__class__.__name__


class IOMemo:
    def __init__(self, module: IOModule) -> None:
        self.io_module = module
