from enum import Enum, auto
from typing import Type
from PIL.Image import Image

from model.capture.capture_node import CaptureNode

class WorkingDoc:
    def __init__(self, path=None, url=None) -> None:
        self.path = path
        self.url = url
        self.filehash = None
        self.page_cache = list[Image]()
        self.root_node = CaptureNode(self,CaptureNode.Type.ROOT)
        self.curr_node_cls:Type[CaptureNode]=CaptureNode
        self.focus_node = self.root_node
        self.status = self.STATUS.NOT_AVALIABLE
        self.page_no = 0

    class STATUS(Enum):
        NOT_AVALIABLE = auto()
        NORMAL = auto()
