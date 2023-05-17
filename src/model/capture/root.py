from model.capture.capture_node import CaptureNode
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.doc import WorkingDoc


class RootNode(CaptureNode):
    def __init__(self,doc:'WorkingDoc') -> None:
        super().__init__()
        self.parent=doc
        self.working_doc=doc

    def node_type(self):
        return self.Type.ROOT

    def get_visual_memo(self):
        return None
