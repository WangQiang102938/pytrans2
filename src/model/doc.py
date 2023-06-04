from enum import Enum, auto
from typing import Type
from PIL.Image import Image

from model.capture.capture_node import CaptureNode
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.io.io_hub import IOMemo

class WorkingDoc:
    def __init__(self, path=None, url=None) -> None:
        self.path = path
        self.url = url
        self.filehash = None
        self.io_memo: IOMemo = None
        self.page_cache = list[Image]()
        self.root_node = CaptureNode(self, CaptureNode.Type.ROOT)
        self.focus_node = self.root_node
        self.status = self.STATUS.NOT_AVALIABLE
        self.page_no = 0

    class STATUS(Enum):
        NOT_AVALIABLE = auto()
        NORMAL = auto()

    def reload(self, pages: list[Image]):
        self.page_cache = pages
        if not isinstance(pages, list) or pages.__len__() == 0:
            self.status = self.STATUS.NOT_AVALIABLE
        else:
            self.status = self.STATUS.NORMAL
        self.page_no = 0
        self.focus_node = self.root_node = CaptureNode(self, CaptureNode.Type.ROOT)
