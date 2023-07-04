import pickle
from enum import Enum, auto
from typing import Callable
import uuid
from model.doc import MemoORM, WorkingDoc
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PIL.Image import Image
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
        ui = self.ctrl_hub.ui
        io_module_clses = my_utils.scan_class(
            my_utils.split_dir_from_file(__file__), IOModule
        )
        self.io_modules = [x(self) for x in io_module_clses]
        renderer_clses = my_utils.scan_class(
            my_utils.split_dir_from_file(__file__), IOModule
        )
        self.renderes = [x(self) for x in renderer_clses]
        for module in self.io_modules:
            ui.ioModuleTab.addTab(module.get_widget(), module.get_title())

    def add_doc(self, doc: WorkingDoc, set_to_work_flag=True):
        self.ctrl_hub.main.model_hub.add_doc(doc)

    def ui_lock_update(self, enable: bool = None):
        main = self.ctrl_hub.main
        if enable is not None:
            main.mainwindow.setEnabled(enable)
        main.app.processEvents()


class IOModule:
    def __init__(self, io_hub: IOHub) -> None:
        self.io_hub = io_hub

    def get_widget(self) -> QWidget:
        pass

    def get_title(self):
        return self.__class__.__name__

    def get_doc_title(self, working_doc: WorkingDoc, with_id=False):
        return "NO TITLE"

    def save_source_to(self, path: str, working_doc: WorkingDoc):
        pass

    def get_binary(self):
        pass

    def save_memo(self,working_doc:WorkingDoc,identifier:str,raw_data:bytes):
        session=working_doc.sessionmaker()
        tmp_memo_orm=MemoORM(
            uuid=uuid.uuid1()
        )

class Renderer:
    def __init__(self, io_hub: IOHub) -> None:
        self.io_hub = io_hub

    def render(self, binary: bytes) -> list[Image]:
        pass


class IOMemo:
    def __init__(self, module: IOModule) -> None:
        self.io_module = module
