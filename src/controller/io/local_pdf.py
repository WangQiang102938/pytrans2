import os
import shutil
from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget
from pypdfium2 import PdfDocument
from model.doc import WorkingDoc
from controller.io.io_hub import IOMemo, IOModule
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import pypdfium2
from typing import *

import my_utils
from my_utils import io_utils
import my_utils.qt_utils

if TYPE_CHECKING:
    from controller.io.io_hub import IOHub


class ModuleMemo(IOMemo):
    def __init__(self, module: IOModule) -> None:
        super().__init__(module)
        self.path = None


class LocalPDFModule(IOModule):
    valid_ins: "LocalPDFModule" = None

    def __init__(self, io_hub: "IOHub") -> None:
        super().__init__(io_hub)
        self.widget = ModuleWidget().bind(self)
        if io_hub != None:
            LocalPDFModule.valid_ins = self

    def open(self, path_list: list[str]):
        if not isinstance(path_list, list):
            return
        self.io_hub.ui_lock_update(False)
        self.widget.doc_progress_bar.setRange(0, len(path_list))
        for i, path in enumerate(path_list):
            self.widget.doc_progress_bar.setValue(i)
            rendered_pages = io_utils.load_local_pdf(
                path, self.widget.progress_call, self.widget.scale_spin.value()
            )
            if rendered_pages == None:
                print("Load PDF Failed")
                continue
            tmp_doc = WorkingDoc()
            tmp_memo = ModuleMemo(self)
            tmp_memo.path = path
            tmp_doc.io_memo = tmp_memo
            tmp_doc.reload(rendered_pages)
            self.io_hub.add_doc(tmp_doc)
            self.widget.doc_progress_bar.setValue(i + 1)
            self.io_hub.ui_lock_update()
        self.io_hub.ui_lock_update(True)

    def get_widget(self) -> QWidget:
        return self.widget

    def get_doc_title(self, working_doc: WorkingDoc, with_id=False):
        if not isinstance(working_doc.io_memo, ModuleMemo):
            return super().get_doc_title(working_doc)
        memo = working_doc.io_memo
        return f"{my_utils.split_filename(memo.path)}{'' if not with_id else f' @ {id(memo)}'}"

    def save_source_to(self, path: str, working_doc: WorkingDoc):
        try:
            memo: ModuleMemo = working_doc.io_memo
            shutil.copy2(memo.path, f"{path}/{os.path.split(memo.path)[1]}")
            return True
        except Exception as e:
            return False


class ModuleWidget(QFrame):
    def bind(self, module: LocalPDFModule):
        self.module = module
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.main_btn = my_utils.qt_utils.add_to_layout(
            main_layout, ModuleBtn("Open PDFs or drop PDFs file here", self)
        )
        self.main_btn.set_open_call(self.module.open)
        self.main_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.scale_spin = (
            my_utils.qt_utils.FormItem()
            .setup(
                "scale",
                main_layout,
            )
            .add_content(QSpinBox())
        )
        self.scale_spin.setRange(1, 10)
        self.scale_spin.setValue(5)
        self.doc_progress_bar = my_utils.qt_utils.add_to_layout(
            main_layout, QProgressBar()
        )
        self.page_progress_bar = my_utils.qt_utils.add_to_layout(
            main_layout, QProgressBar()
        )

        return self

    def progress_call(self, page_i, page_len):
        self.page_progress_bar.setRange(0, page_len)
        self.page_progress_bar.setValue(page_i)
        self.module.io_hub.ui_lock_update()


class ModuleBtn(QPushButton):
    def set_open_call(self, call: Callable[[list[str]], None]):
        self.open_call = call
        self.setAcceptDrops(True)
        self.clicked.connect(self.on_click)

    def on_click(self):
        paths = my_utils.qt_utils.qt_file_io(QFileDialog.FileMode.ExistingFiles)
        if paths != None:
            self.open_call(paths)

    def dragEnterEvent(self, a0: QDragEnterEvent) -> None:
        a0.accept()

    def dropEvent(self, event: QDropEvent) -> None:
        if not event.mimeData().hasUrls():
            return event.setAccepted(False)
        self.open_call([x.toLocalFile() for x in event.mimeData().urls()])
        event.accept()
