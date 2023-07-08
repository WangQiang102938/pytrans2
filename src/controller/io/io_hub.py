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

    class ConfigKey(Enum):
        VALID_IOMODULE = "VALID_IOMODULE"
        VALID_RENDERER = "VALID_RENDERER"

    def __init__(self, ctrl_hub: "ControllerHub") -> None:
        self.ctrl_hub = ctrl_hub
        ui = self.ctrl_hub.ui
        # iomodule
        io_module_clses = my_utils.scan_class(
            my_utils.split_dir_from_file(__file__), IOModule
        )
        self.io_modules = [x(self) for x in io_module_clses]
        self.io_modules_uuid = {x.uuid: x for x in self.io_modules}
        # renderer
        renderer_clses = my_utils.scan_class(
            my_utils.split_dir_from_file(__file__), Renderer
        )
        self.renderes = [x(self) for x in renderer_clses]
        self.renderes_uuid = {x.uuid: x for x in self.renderes}
        # ui setup
        for module in self.io_modules:
            ui.ioModuleTab.addTab(module.get_widget(), module.get_title())
        for renderer in self.renderes:
            ui.rendererSelectCombo.addItem(renderer.get_title(), renderer)
        ui.rendererSelectCombo.setCurrentIndex(0)

    def add_doc(self, doc: WorkingDoc, set_to_work_flag=True):
        self.ctrl_hub.main.model_hub.add_doc(doc)

    def ui_lock_update(self, enable: bool = None):
        main = self.ctrl_hub.main
        if enable is not None:
            main.mainwindow.setEnabled(enable)
        main.app.processEvents()

    def set_valid_iomodule(self, working_doc: WorkingDoc, io_module: "IOModule"):
        working_doc.set_orm(
            working_doc.ORM.KeyVal(
                key=self.ConfigKey.VALID_IOMODULE.value, str_val=io_module.get_title()
            )
        )

    def get_valid_iomodule(self, working_doc: WorkingDoc):
        result = (
            working_doc.get_orm_query(working_doc.ORM.KeyVal)
            .filter_by(key=self.ConfigKey.VALID_IOMODULE.value)
            .first()
        )
        if result == None:
            return None
        for io_module in self.io_modules:
            if io_module.get_title() == result.str_val:
                return io_module
        return None


class IOModule:
    class ConfigKeys(Enum):
        IO_BINARY = "IO_BINARY"

    def __init__(self, io_hub: IOHub) -> None:
        self.io_hub = io_hub
        self.uuid = uuid.uuid1()

    def get_widget(self) -> QWidget:
        pass

    def get_title(self):
        return self.__class__.__name__

    def get_doc_title(self, working_doc: WorkingDoc, with_id=False):
        return "NO TITLE"

    def export_binary(self, path: str, working_doc: WorkingDoc):
        try:
            f = open(path, "wb")
            f.write(self.get_binary(working_doc))
            return True
        except Exception as e:
            return False

    def get_binary(self, working_doc: WorkingDoc):
        memo_ins = self.sync_binary(working_doc)
        if memo_ins == None:
            return None
        raw: bytes = memo_ins.raw_val
        return raw

    def sync_binary(self, working_doc: WorkingDoc, binary: bytes = None):
        return working_doc.get_memo_with_update(
            self.get_title(), IOModule.ConfigKeys.IO_BINARY.value, raw_val=binary
        )


class Renderer:
    def __init__(self, io_hub: IOHub) -> None:
        self.io_hub = io_hub
        self.uuid = uuid.uuid1()

    def get_title(self):
        return self.__class__.__name__

    def render(
        self, working_doc: WorkingDoc, binary: bytes, use_cache=True
    ) -> list[Image]:
        pass

    def popup_setting(self):
        pass


class IOMemo:
    def __init__(self, module: IOModule) -> None:
        self.io_module = module
