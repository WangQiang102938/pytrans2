from typing import Callable
from controller.pipeline.pipeline_hub import PipelineNode
from listener.listener_hub import PyTransEvent
from model.capture.capture_node import CaptureNode
from model.doc import WorkingDoc
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from enum import Enum,auto
from typing import *
if TYPE_CHECKING:
    from view.view_hub import ViewHub
import utils as pytrans_utils


class PipelineEditFlag(Enum):
    ADD_NODE=auto()
    REMOVE_NODE=auto()
    BRING_UP=auto()
    BRING_DOWN=auto()

class PipelineViewhub:
    def __init__(self, view_hub: 'ViewHub') -> None:
        self.view_hub = view_hub
        self.pipeline_ctrlhub=view_hub.main.controller_hub.pipeline_hub
        self.ui=view_hub.ui

        for node in self.pipeline_ctrlhub.pipeline_nodes:
            self.ui.pipeAvaliableCombo.addItem(node.name,node)

        self.ui.PipeAddBtn.clicked.connect(lambda x:self.pipeline_edit(PipelineEditFlag.ADD_NODE))
        self.ui.PipeUpBtn.clicked.connect(lambda x:self.pipeline_edit(PipelineEditFlag.BRING_UP))
        self.ui.PipeDownBtn.clicked.connect(lambda x:self.pipeline_edit(PipelineEditFlag.BRING_DOWN))
        self.ui.PipeRemoveBtn.clicked.connect(lambda x:self.pipeline_edit(PipelineEditFlag.REMOVE_NODE))
        self.ui.pipeEditList.currentRowChanged.connect(self.pipe_edit_changed)


    def pipeline_edit(self,flag:'PipelineEditFlag'):
        pipelineList_widget=self.ui.pipeEditList
        if(flag not in PipelineEditFlag):
            return
        if(flag==PipelineEditFlag.ADD_NODE):
            curr_pipenode_cls:Type[PipelineNode]=self.ui.pipeAvaliableCombo.currentData()
            tmp_pipenode_cls=curr_pipenode_cls(self.pipeline_ctrlhub)
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
        curr=self.ui.pipeEditList.currentItem()
        if(curr!=None):
            pipe_node:PipelineNode=curr.data(Qt.ItemDataRole.UserRole)
            pytrans_utils.qwidget_cleanup(pipe_option_con)
            self.ui.pipeOptionTab.layout().addWidget(pipe_option_con)
            pipe_node.option_ui_setup(pipe_option_con)
        else:
            pytrans_utils.qwidget_cleanup(pipe_option_con)
            pytrans_utils.qwidget_cleanup(pipe_node_option_con)


