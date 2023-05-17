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
from typing import TYPE_CHECKING, List, Type
import uuid
if TYPE_CHECKING:
    from controller.controller_hub import ControllerHub


class PipelineHub:
    def __init__(self, ctrl_hub: 'ControllerHub') -> None:
        self.ctrl_hub = ctrl_hub
        self.pipeline_nodes = list[Type[PipelineNode]]()
        self.pipeline_node_ins = list[PipelineNode]()
        self.ui=self.ctrl_hub.ui
        self.scan_pipline_node(os.path.split(__file__)[0])

        for node in self.pipeline_nodes:
            ui=self.ctrl_hub.ui
            ui.pipeAvaliableCombo.addItem(node.name,node)
            # ui.pipeOptionCombo.addItem(node.get_title(),node)

        # self.ctrl_hub.ui.pipeOptionCombo.currentIndexChanged.connect(self.option_tab_index_changed)
        # self.option_tab_index_changed(self.ctrl_hub.ui.pipeOptionCombo.currentIndex())
        self.ui.PipeAddBtn.clicked.connect(lambda x:self.pipeline_edit(PipelineEditFlag.ADD_NODE))
        self.ui.PipeUpBtn.clicked.connect(lambda x:self.pipeline_edit(PipelineEditFlag.BRING_UP))
        self.ui.PipeDownBtn.clicked.connect(lambda x:self.pipeline_edit(PipelineEditFlag.BRING_DOWN))
        self.ui.PipeRemoveBtn.clicked.connect(lambda x:self.pipeline_edit(PipelineEditFlag.REMOVE_NODE))
        self.ui.pipelineList.currentRowChanged.connect(self.pipe_edit_changed)

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

    def pipeline_edit(self,flag:'PipelineEditFlag'):
        pipelineList_widget=self.ui.pipelineList
        if(flag not in PipelineEditFlag):
            return
        if(flag==PipelineEditFlag.ADD_NODE):
            curr_pipenode_cls:Type[PipelineNode]=self.ui.pipeAvaliableCombo.currentData()
            tmp_pipenode_cls=curr_pipenode_cls(self)
            tmp_listwidget=QListWidgetItem(tmp_pipenode_cls.get_ins_name())
            tmp_listwidget.setData(Qt.ItemDataRole.UserRole,tmp_pipenode_cls)
            pipelineList_widget.addItem(tmp_listwidget)
        elif(flag==PipelineEditFlag.BRING_UP):
            curr_row=pipelineList_widget.currentRow()
            if(curr_row==None):
                return
            curr_data=pipelineList_widget.item(curr_row)
            prev_data=pipelineList_widget.item(curr_row-1)
            if(curr_data==None or prev_data==None):
                return
            pipelineList_widget.takeItem(curr_row-1)
            pipelineList_widget.takeItem(curr_row-1)
            pipelineList_widget.insertItem(curr_row-1,prev_data)
            pipelineList_widget.insertItem(curr_row-1,curr_data)
            pipelineList_widget.setCurrentRow(curr_row-1)
        elif(flag==PipelineEditFlag.BRING_DOWN):
            curr_row=pipelineList_widget.currentRow()
            if(curr_row==None):
                return
            curr_data=pipelineList_widget.item(curr_row)
            next_data=pipelineList_widget.item(curr_row+1)
            if(curr_data==None or next_data==None):
                return
            pipelineList_widget.takeItem(curr_row)
            pipelineList_widget.takeItem(curr_row)
            pipelineList_widget.insertItem(curr_row,curr_data)
            pipelineList_widget.insertItem(curr_row,next_data)
            pipelineList_widget.setCurrentRow(curr_row+1)
        elif(flag==PipelineEditFlag.REMOVE_NODE):
            curr_row=pipelineList_widget.currentRow()
            if(curr_row==None):
                return
            pipelineList_widget.takeItem(curr_row)

    def pipe_edit_changed(self,row:int):
        pipe_option_con=self.ui.pipeOptionContainer
        pipe_node_option_con=self.ui.pipeOptionContainer
        curr=self.ui.pipelineList.currentItem()
        if(curr!=None):
            pipe_node:PipelineNode=curr.data(Qt.ItemDataRole.UserRole)
            pytrans_utils.qwidget_cleanup(pipe_option_con)
            self.ui.pipeOptionTab.layout().addWidget(pipe_option_con)
            pipe_node.option_ui_setup(pipe_option_con)
        else:
            pytrans_utils.qwidget_cleanup(pipe_option_con)
            pytrans_utils.qwidget_cleanup(pipe_node_option_con)


class PipelineEditFlag(Enum):
    ADD_NODE=auto()
    REMOVE_NODE=auto()
    BRING_UP=auto()
    BRING_DOWN=auto()


class PipelineNode:
    name="NAME_NOT_SET"

    def __init__(self, pipe_hub: PipelineHub) -> None:
        self.pipe_hub = pipe_hub
        self.uuid=uuid.uuid1()
        self.tags=[self.Tag.NOP]

    def get_ins_name(self):
        return str(f"{self.name}_{self.uuid}")

    def option_ui_setup(self,container:QWidget) -> QWidget:
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

    def get_memo(self,node:CaptureNode)->'PipeMemo':
        return None

    def run_pipe(self,node:CaptureNode,**input):
        return False

    def get_output(self,node:CaptureNode,key:str):
        pass

    def get_port_keys(self,input_port=True)->List[str]:
        pass


class PipeMemo:
    def __init__(self,pipe_ins:PipelineNode) -> None:
        self.node:CaptureNode=None
        self.pipe_ins=pipe_ins
        self.data=None

    def bind_node(self,node:CaptureNode):
        self.node=node
        return self

    def get_pipenode_name(self):
        return "NAIVE_NODE"

    def set_data(self,data):
        self.data=data

    def get_result(self):
        return None


