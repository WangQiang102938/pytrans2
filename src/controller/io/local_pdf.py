from enum import Enum
import os
import shutil
from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget
from pypdfium2 import PdfDocument
from model.doc import WorkingDoc
from controller.io.io_hub import IOMemo, IOModule, Renderer
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import pypdfium2
from typing import *

import my_utils
from my_utils import io_utils, qt_utils

if TYPE_CHECKING:
    from controller.io.io_hub import IOHub


class ModuleMemo(IOMemo):
    def __init__(self, module: IOModule) -> None:
        super().__init__(module)
        self.path = None
        self.binary: bytes = None


class ConfigKeys(Enum):
    PATH = "PATH"


class LocalPDFModule(IOModule):
    valid_ins: "LocalPDFModule" = None

    def __init__(self, io_hub: "IOHub") -> None:
        super().__init__(io_hub)
        self.widget = ModuleWidget().bind(self)
        if io_hub != None:
            LocalPDFModule.valid_ins = self

    def open_multi(self, path_list: list[str]):
        if not isinstance(path_list, list):
            return
        self.io_hub.ui_lock_update(False)
        self.widget.doc_progress_bar.setRange(0, len(path_list))
        for i, path in enumerate(path_list):
            self.widget.doc_progress_bar.setValue(i)
            self.io_hub.ui_lock_update()
            # rendered_pages = io_utils.load_local_pdf(
            #     path, self.widget.progress_call, self.widget.scale_spin.value()
            # )
            # if rendered_pages == None:
            #     print("Load PDF Failed")
            #     continue
            # tmp_doc = WorkingDoc()
            # tmp_memo = ModuleMemo(self)
            # tmp_memo.path = path
            # tmp_doc.io_memo = tmp_memo
            # tmp_doc.reload(rendered_pages)
            # self.io_hub.add_doc(tmp_doc)

            # tmp_doc.set_memo(
            #     memo_identifier=self.get_title(),
            #     memo_key=ConfigKeys.RAW_DATA,
            #     str_val=path,
            #     raw_val=open(path, mode="rb").read(),
            # )

            if not self.open(path):
                print(f"Fail to open local PDF: {path}")

            self.widget.doc_progress_bar.setValue(i + 1)
            self.io_hub.ui_lock_update()
        self.io_hub.ui_lock_update(True)

    def open(self, path: str):
        ui = self.io_hub.ctrl_hub.ui
        try:
            binary_data = open(path, "rb").read()
            renderer: Renderer = ui.rendererSelectCombo.currentData(
                Qt.ItemDataRole.UserRole
            )
            tmp_doc = WorkingDoc.default_doc()
            rendered_pages = renderer.render(tmp_doc, binary_data, False)

            self.io_hub.set_valid_iomodule(tmp_doc, self)
            self.sync_binary(tmp_doc,binary_data)
            tmp_doc.sync_memo(self.get_title(), ConfigKeys.PATH.value, str_val=path)

            tmp_doc.sync_doc_title(set_new_title=f"{my_utils.split_filename(path)}")
            tmp_doc.reload(rendered_pages)
            self.io_hub.add_doc(tmp_doc)
            return True
        except Exception as e:
            print(e)
            tmp_doc.delete_me()
            return False

    def get_widget(self) -> QWidget:
        return self.widget

    def get_doc_title(self, working_doc: WorkingDoc, with_id=False):
        orm_ins = working_doc.sync_memo(self.get_title(), ConfigKeys.PATH.value)
        path: str = "Unknown.Local" if orm_ins else orm_ins.str_val
        if not isinstance(path, str):
            return super().get_doc_title()
        return f"{my_utils.split_filename(path)}{'' if not with_id else f' @ {id(working_doc)}'}"


class ModuleWidget(QFrame):
    def bind(self, module: LocalPDFModule):
        self.module = module
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        setting_con = QWidget()
        setting_con.setLayout(QHBoxLayout())
        setting_layout = setting_con.layout()
        main_layout.addWidget(setting_con)

        self.main_btn = qt_utils.add_to_layout(
            setting_layout, ModuleBtn("Open PDFs or drop PDFs file here", self)
        )
        self.main_btn.set_open_call(self.module.open_multi)
        self.main_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.scale_spin = (
            qt_utils.FormItem()
            .setup(
                "scale",
                setting_layout,
            )
            .add_content(QSpinBox())
        )
        self.scale_spin.setRange(1, 10)
        self.scale_spin.setValue(5)
        self.doc_progress_bar = (
            qt_utils.FormItem()
            .setup("Files Progress", main_layout)
            .add_content(QProgressBar())
        )
        self.render_progress_bar = (
            qt_utils.FormItem()
            .setup("Render Progress", main_layout)
            .add_content(QProgressBar())
        )

        return self

    def progress_call(self, page_i, page_len):
        self.render_progress_bar.setRange(0, page_len)
        self.render_progress_bar.setValue(page_i)
        self.module.io_hub.ui_lock_update()


class ModuleBtn(QPushButton):
    def set_open_call(self, call: Callable[[list[str]], None]):
        self.open_call = call
        self.setAcceptDrops(True)
        self.clicked.connect(self.on_click)

    def on_click(self):
        paths = qt_utils.qt_file_io(QFileDialog.FileMode.ExistingFiles)
        if paths != None:
            self.open_call(paths)

    def dragEnterEvent(self, a0: QDragEnterEvent) -> None:
        a0.accept()

    def dropEvent(self, event: QDropEvent) -> None:
        if not event.mimeData().hasUrls():
            return event.setAccepted(False)
        self.open_call([x.toLocalFile() for x in event.mimeData().urls()])
        event.accept()
