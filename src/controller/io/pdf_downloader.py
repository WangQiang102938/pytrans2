from io import BytesIO
import os
from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget
from pypdfium2 import PdfDocument
from model.doc import WorkingDoc
from controller.io.io_hub import IOHub, IOMemo, IOModule
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PIL.Image import Image
import pypdfium2
from typing import *

import my_utils
from my_utils import io_utils, qt_utils
import my_utils.qt_utils

import requests

if TYPE_CHECKING:
    from controller.io.io_hub import IOHub


class ModuleWidget(QFrame):
    def bind(self, module: "PDFDownloader"):
        self.module = module
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.url_edit, self.url_con = (
            qt_utils.FormItem(self)
            .setup("URL", main_layout, True)
            .add_content_chain(QLineEdit())
        )
        self.download_btn = self.url_con.add_content(QPushButton("↓"))
        self.url_edit.sizePolicy().setHorizontalStretch(1)

        main_layout.addItem(qt_utils.gen_spacer())

        self.download_progress = (
            qt_utils.FormItem(self)
            .setup("Download Progress", main_layout, True)
            .add_content(QProgressBar())
        )
        self.render_progress = (
            qt_utils.FormItem(self)
            .setup("Render Progress", main_layout, True)
            .add_content(QProgressBar())
        )

        return self


class ModuleMemo(IOMemo):
    def __init__(self, module: IOModule) -> None:
        super().__init__(module)
        self.url: str = None
        self.buffer: BytesIO = None


class PDFDownloader(IOModule):
    def __init__(self, io_hub: IOHub) -> None:
        super().__init__(io_hub)
        self.widget = ModuleWidget().bind(self)

        self.widget.download_btn.clicked.connect(self.download)

    def get_widget(self) -> QWidget:
        return self.widget

    def get_title(self):
        return super().get_title()

    def download(self):
        try:
            self.io_hub.ui_lock_update(False)
            response = requests.get(self.widget.url_edit.text(), stream=True)
            total_size = int(response.headers.get("content-length", 0))
            block_size = 1024
            byte_received = 0
            buffer = BytesIO()

            self.widget.download_progress.setRange(0, total_size)
            self.widget.download_progress.setValue(0)
            self.widget.download_progress.setEnabled(True)
            for data in response.iter_content(block_size):
                buffer.write(data)
                byte_received += len(data)
                self.widget.download_progress.setValue(byte_received)
                self.io_hub.ui_lock_update()

            rendered_pages = list[Image]()
            pdf = PdfDocument(buffer.getvalue())
            page_count = len(pdf)
            self.widget.render_progress.setRange(0, page_count)
            self.widget.render_progress.setValue(0)
            for index in range(page_count):
                page = pdf.get_page(index)
                rendered_pages.append(page.render(scale=5).to_pil())
                self.widget.render_progress.setValue(index + 1)
                self.io_hub.ui_lock_update()
            tmp_doc = WorkingDoc()
            tmp_memo = ModuleMemo(self)
            tmp_doc.io_memo = tmp_memo
            tmp_doc.reload(rendered_pages)
            tmp_memo.url = self.widget.url_edit.text()
            tmp_memo.buffer = buffer
            self.io_hub.add_doc(tmp_doc)
        except Exception as e:
            pass
        finally:
            self.io_hub.ui_lock_update(True)

    def save_source_to(self, path: str, working_doc: WorkingDoc):
        try:
            memo: ModuleMemo = working_doc.io_memo
            filepath = f"{path}/{self.get_doc_title(working_doc)}.pdf"
            with open(filepath, "wb") as f:
                f.write(memo.buffer.getvalue())
            return True
        except Exception as e:
            return False

    def get_doc_title(self, working_doc: WorkingDoc, with_id=False):
        try:
            memo: ModuleMemo = working_doc.io_memo
            name = os.path.split(memo.url)[1]
            return name if not with_id else f"{name} @ {id(memo)}"
        except Exception as e:
            return None
