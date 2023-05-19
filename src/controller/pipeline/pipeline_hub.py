from enum import Enum, auto
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import utils as pytrans_utils
import os
import sys
import importlib
import importlib.machinery
import inspect
from model.capture.capture_node import CaptureNode
from model.doc import WorkingDoc
from typing import *
import uuid

if TYPE_CHECKING:
    from controller.controller_hub import ControllerHub

T=TypeVar("T")

class PipelineHub:
    def __init__(self, ctrl_hub: 'ControllerHub') -> None:
        self.ctrl_hub = ctrl_hub
        self.pipeline_nodes = list[Type[PipelineNode]]()
        self.pipeline_node_ins = list[PipelineNode]()
        self.ui=self.ctrl_hub.ui
        self.scan_pipline_node(os.path.split(__file__)[0])

        # self.ctrl_hub.ui.pipeOptionCombo.currentIndexChanged.connect(self.option_tab_index_changed)
        # self.option_tab_index_changed(self.ctrl_hub.ui.pipeOptionCombo.currentIndex())

    def scan_pipline_node(self, path):
        sys.path.append(path) if path not in sys.path else None
        for root, dirs, files in os.walk(path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if (ext != '.py' or __file__ == f"{root}/{file}"):
                    continue
                module = importlib.machinery.SourceFileLoader(filename, f"{root}/{file}").load_module()
                for clsname, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, PipelineNode):
                        if (obj != PipelineNode and obj not in [x.__class__ for x in self.pipeline_nodes]):
                            self.pipeline_nodes.append(obj)




class PipeMemo:
    def __init__(self,pipe_ins:'PipelineNode') -> None:
        self.node:CaptureNode=None
        self.pipe_ins=pipe_ins

    def bind_node(self,node:CaptureNode,overwrite_flag=False):
        self.node=node
        if (overwrite_flag or self.pipe_ins not in node.pipeline_memo):
            node.pipeline_memo[self.pipe_ins]=self
        return self

class PipeUpdateMode(Enum):
    BYPASS=auto()
    CAPTURE_NODE_UPDATED=auto()
    FULLY_RUN=auto()

class PipelineNode:
    name="NAME_NOT_SET"

    def __init__(self, pipe_hub: PipelineHub) -> None:
        self.pipe_hub = pipe_hub
        self.uuid=uuid.uuid1()
        self.link_info=dict[str,Tuple[PipelineNode,str]]()

    def get_ins_name(self):
        return str(f"{self.name}@{id(self)}")

    def option_ui_setup(self,container:QWidget):
        pass

    def capnode_option_ui_setup(self,container:QWidget,node:CaptureNode=None):
        pass

    def get_text_output(self,node:CaptureNode=None):
        pass

    def process_node(self, node: CaptureNode, dfs_mode=False,update_flag=False):
        pass

    def process_doc(self, doc: WorkingDoc, node: CaptureNode = None):
        node = node if node != None else doc.root_node
        for child in node.children:
            self.process_doc(self, doc, child)
        self.process_node(node, dfs_mode=True)

    def find_my_memo(self,node:CaptureNode,cast_type:Type[T]=PipeMemo,)->T:
        if (not isinstance(node,CaptureNode)
            or self not in node.pipeline_memo):
            return None
        val= node.pipeline_memo[self]
        return val if isinstance(val,cast_type) else None

    def run_pipe(self,node:CaptureNode,mode:PipeUpdateMode=PipeUpdateMode.BYPASS,**input):
        return False

    def get_output(self,node:CaptureNode,key:str)-> Any:
        return None

    def get_port_keys(self,input_port=True)->List[str]:
        pass

    def set_link(self,out_ins:'PipelineNode',out_key:str,in_key:str):
        if not isinstance(out_ins,PipelineNode):
            return False
        if out_key not in out_ins.get_port_keys(False):
            return False
        if in_key not in self.get_port_keys():
            return False
        self.link_info[in_key]=(out_ins,out_key)
        return True





