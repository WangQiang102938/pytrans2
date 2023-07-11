from enum import Enum
import pickle
from typing import Any, List
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from PIL.Image import Image
from controller.pipeline.pipeline_hub import (
    PipeMemo,
    PipeUpdateMode,
    PipelineHub,
    PipelineNode,
)
from model.capture.capture_node import CaptureNode
import my_utils.qt_utils as qt_utils
import my_utils
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters


class PortEnum(Enum):
    IN_TEXT = "in:str"
    OUT_TEXT_SET = "out:[[str]]"


class Memo(PipeMemo):
    def __init__(self, pipe_ins: PipelineNode) -> None:
        super().__init__(pipe_ins)
        self.origin_txt: str = None
        self.formatted: list[list[str]] = None


class StandardFormatter(PipelineNode):
    name = "StdFormatter"

    def __init__(self, pipe_hub: PipelineHub) -> None:
        super().__init__(pipe_hub)
        self.option_widget = StdFormatterWidget().bind()
        self.sent_tokenizer: PunktSentenceTokenizer = None

    def activate_tokenizer(self):
        if self.sent_tokenizer == None:
            params = PunktParameters()
            params.abbrev_types = set(["et al", "fig", "Fig"])
            self.sent_tokenizer = PunktSentenceTokenizer(params)

    def option_ui_setup(self, container: QWidget):
        container_layout = (
            QHBoxLayout(container) if container.layout() == None else container.layout()
        )
        container_layout.setContentsMargins(2, 2, 2, 2)
        container_layout.addWidget(self.option_widget)
        container.setVisible(True)
        container.show()

    def get_port_keys(self, input_port=True) -> List[str]:
        return [PortEnum.IN_TEXT.value] if input_port else [PortEnum.OUT_TEXT_SET.value]

    def process_capnode(
        self, node: CaptureNode, mode: PipeUpdateMode = PipeUpdateMode.BYPASS, **input
    ):
        txt_in = my_utils.safe_get_dict_val(input, PortEnum.IN_TEXT.value, str)
        if txt_in == None:
            return None
        sections = list[str]()

        if self.option_widget.split_section_check.isChecked():
            sections = txt_in.split("\n\n")
        else:
            sections = [txt_in]

        if self.option_widget.remove_hyphen_check.isChecked():
            for i, section in enumerate(sections.copy()):
                sections[i] = section.replace("-\n", "")

        if self.option_widget.split_sent_check.isChecked():
            self.activate_tokenizer()
            for i, section in enumerate(sections.copy()):
                section = section.replace("\n", " ")
                sections[i] = self.sent_tokenizer.tokenize(section)
        else:
            for i, section in enumerate(sections.copy()):
                sections[i] = [section]

        if self.option_widget.print_check.isChecked():
            print(sections)
        node.working_doc.get_memo_with_update(
            self.uuid.hex,
            PortEnum.OUT_TEXT_SET.value,
            node.uuid.bytes,
            raw_val=pickle.dumps(sections),
        )

    def get_output(self, node: CaptureNode, key: str) -> Any:
        try:
            binary = node.working_doc.get_memo_with_update(
                self.uuid.hex, key, node.uuid.bytes
            ).raw_val
            return pickle.loads(binary)
        except Exception as e:
            print(e)
            return None


class StdFormatterWidget(QFrame):
    def bind(self):
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.split_section_check = qt_utils.add_to_layout(
            self.main_layout, QCheckBox("Split section(\\n\\n)")
        )
        self.split_section_check.setChecked(True)

        self.remove_hyphen_check = qt_utils.add_to_layout(
            self.main_layout, QCheckBox("Remove word warp '-'")
        )
        self.remove_hyphen_check.setChecked(True)

        self.split_sent_check = qt_utils.add_to_layout(
            self.main_layout, QCheckBox("Remove \\n & Split sentences(nltk)")
        )
        self.split_sent_check.setChecked(True)

        self.print_check = qt_utils.add_to_layout(
            self.main_layout, QCheckBox("Print output")
        )

        self.main_layout.addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )
        return self
