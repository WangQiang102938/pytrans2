from typing import List
from PyQt6.QtWidgets import QWidget
from controller.pipeline.pipeline_hub import PipeMemo, PipeUpdateMode, PipelineHub, PipelineNode
from enum import Enum,auto
from PIL.Image import Image
import my_utils.preview_utils as preview_utils
from model.capture.capture_node import CaptureNode
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
class PortEnum(Enum):
    OUT_IMAGE='Image out'

class Memo(PipeMemo):
    def __init__(self, pipe_ins: PipelineNode) -> None:
        super().__init__(pipe_ins)
        self.croped_image:Image=None

class StandardCrop(PipelineNode):
    name="Standard Crop"

    def __init__(self, pipe_hub: PipelineHub) -> None:
        super().__init__(pipe_hub)

    def option_ui_setup(self, container: QWidget):
        return super().option_ui_setup(container)

    def process_capnode(self, node: CaptureNode, mode: PipeUpdateMode = PipeUpdateMode.BYPASS, **input):
        memo=self.find_memo(node,Memo,True)
        visual_memo = node.get_visual_memo()

        if visual_memo==None:
            return

        img = node.working_doc.page_cache[visual_memo.page_no]
        node_rect = preview_utils.map_rect_from_ratio(
            QRectF(visual_memo.left, visual_memo.top,
                   visual_memo.right, visual_memo.bottom),
            QRectF(0, 0, img.size[0], img.size[1])
        )
        node_img = img.crop(
            (node_rect.left(), node_rect.top(), node_rect.width(), node_rect.height()))
        memo.croped_image=node_img

    def get_output(self, node: CaptureNode, key: str):
        memo=self.find_memo(node,Memo)
        if(key==PortEnum.OUT_IMAGE.value and memo !=None):
            return memo.croped_image
        return super().get_output(node, key)

    def get_port_keys(self, input_port=True) -> List[str]:
        return [] if input_port else [PortEnum.OUT_IMAGE.value]
