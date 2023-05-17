from enum import Enum, auto


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.doc import WorkingDoc


class CaptureNode:
    def __init__(self) -> None:
        self.parent: CaptureNode = None
        self.children = list[CaptureNode]()
        self.kwargs = dict()
        self.visual_memo: CaptureNode.VisualMemo = None
        self.working_doc: WorkingDoc = None
        self.pipeline_memo = dict()

    def link_parent(self, parent: 'CaptureNode'):
        self.parent = parent
        self.working_doc = parent.working_doc
        if(self not in parent.children):
            parent.children.append(self)
        return self

    def link_children(self, child: 'CaptureNode'):
        if child not in self.children:
            self.children.append(child)
        child.link_parent(self)
        return self

    def node_type(self):
        return self.Type.NOT_IMPLIMENTED

    def get_visual_memo(self):
        return self.visual_memo

    def set_visual_memo(self, info: 'VisualMemo'):
        self.visual_memo = info

    class Type(Enum):
        NOT_IMPLIMENTED = auto()
        ROOT = auto()
        CONTAINER = auto()
        TEXT = auto()
        IMAGE = auto()
        STRUCTURE=auto()

    class VisualMemo:
        def __init__(self, left: float, top: float, right: float, bottom: float, page_no: int, *args, **kwargs) -> None:
            self.left = left
            self.right = right
            self.top = top
            self.bottom = bottom
            self.page_no = page_no
            self.args = args
            self.kwargs = kwargs

        def update(self, left: float = None, top: float = None, right: float = None, bottom: float = None, page_no: int = None, *args, **kwargs) -> None:
            self.left = left if left != None else self.left
            self.right = right if right != None else self.right
            self.top = top if top != None else self.top
            self.bottom = bottom if bottom != None else self.bottom
            self.page_no = page_no if page_no != None else self.page_no
            self.args = args if args != None else self.args
            self.kwargs = kwargs if kwargs != None else self.kwargs
