from enum import Enum
import os
import pickle
import shutil
from PIL.Image import Image
from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget
from pypdfium2 import PdfDocument
from model.doc import WorkingDoc
from controller.io.io_hub import IOHub, IOMemo, IOModule, Renderer
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import pypdfium2
from typing import *

import my_utils
from my_utils import io_utils, qt_utils


class ConfigKeys(Enum):
    RENDER_CACHE = "RENDER_CACHE"


class PDFRenderer(Renderer):
    def __init__(self, io_hub: IOHub) -> None:
        super().__init__(io_hub)
        self.widget = SettingWidget().bind(self)
        self.progress_bar = self.io_hub.ctrl_hub.main.ui.rendererProgressbar

    def render(
        self, working_doc: WorkingDoc, binary: bytes, use_cache=True
    ) -> list[Image]:
        if use_cache:
            return self.load_cache(working_doc)

        ui_lock_status_before = self.io_hub.ctrl_hub.main.mainwindow.isEnabled()
        try:
            self.io_hub.ui_lock_update(False)
            rendered_pages = list[Image]()
            pdf = PdfDocument(binary)
            page_count = len(pdf)

            self.progress_bar.setRange(0, page_count)
            self.io_hub.ui_lock_update()
            for index in range(page_count):
                self.progress_bar.setValue(index)
                self.io_hub.ui_lock_update()

                page = pdf.get_page(index)
                rendered_pages.append(
                    page.render(scale=self.widget.scale_spin.value()).to_pil()
                )

                self.progress_bar.setValue(index + 1)
                self.io_hub.ui_lock_update()
            if self.widget.cache_check.isChecked():
                self.save_cache(working_doc, rendered_pages)
            return rendered_pages
        except Exception:
            return None
        finally:
            self.io_hub.ui_lock_update(ui_lock_status_before)

    def popup_setting(self):
        self.widget.show()

    def save_cache(self, working_doc: WorkingDoc, img_list: List[Image]):
        try:
            binary = pickle.dumps(img_list)
            return working_doc.set_memo(
                self.get_title(), ConfigKeys.RENDER_CACHE, raw_val=binary
            )
        except Exception as e:
            print(e)
            return False

    def load_cache(self, working_doc: WorkingDoc):
        try:
            binary = working_doc.get_memo(self.get_title(), ConfigKeys.RENDER_CACHE)
            loaded: List[Image] = pickle.loads(binary)
            return loaded
        except Exception as e:
            print(e)
            return None


class SettingWidget(QFrame):
    def bind(self, owner: PDFRenderer):
        self.owner = owner
        self.setLayout(QVBoxLayout())

        self.scale_spin = (
            qt_utils.FormItem()
            .setup("Render Scale", self.layout())
            .add_content(QSpinBox())
        )
        self.scale_spin.setValue(5)
        self.scale_spin.setRange(1, 9)

        self.cache_check = qt_utils.add_to_layout(
            self.layout(), QCheckBox("keep rendered cache")
        )
        return self
