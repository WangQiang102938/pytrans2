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

from view.pipeline.pipe_link_edit import PipeLinkEditWidget
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
        self.ui.pipeOptionViewList.currentRowChanged.connect(self.pipe_option_changed)
        self.ui.pipeEditList.currentRowChanged.connect(self.pipe_edit_changed)
        self.ui.pipeRunBtn.clicked.connect(self.pipeline_run)
        self.current_link_widget=PipeLinkEditWidget().bind(self)

    def pipeline_edit(self,flag:'PipelineEditFlag'):
        pipeEditList_widget=self.ui.pipeEditList
        pipeline_node_ins_list=self.pipeline_ctrlhub.pipeline_node_ins
        if(flag not in PipelineEditFlag):
            return
        curr_edit_listitem=pipeEditList_widget.currentItem()
        curr_option_listitem=self.ui.pipeOptionViewList.currentItem()

        if(flag==PipelineEditFlag.ADD_NODE):
            curr_pipenode_cls:Type[PipelineNode]=self.ui.pipeAvaliableCombo.currentData()
            tmp_pipenode_cls=curr_pipenode_cls(self.pipeline_ctrlhub)
            pipeline_node_ins_list.append(tmp_pipenode_cls)
        else:
            if(curr_edit_listitem==None):
                return
            curr_ins:PipelineNode=pipeEditList_widget.currentItem().data(Qt.ItemDataRole.UserRole)
            assert curr_ins in pipeline_node_ins_list
            if(flag==PipelineEditFlag.REMOVE_NODE):
                pipeline_node_ins_list.remove(curr_ins)
            elif(flag==PipelineEditFlag.BRING_UP):
                curr_index=pipeline_node_ins_list.index(curr_ins)
                pytrans_utils.swap_list_item(pipeline_node_ins_list,curr_index,curr_index-1)
            elif(flag==PipelineEditFlag.BRING_DOWN):
                curr_index=pipeline_node_ins_list.index(curr_ins)
                pytrans_utils.swap_list_item(pipeline_node_ins_list,curr_index,curr_index+1)

        def index_from_item(item:QListWidgetItem):
            ins=None if item==None else item.data(Qt.ItemDataRole.UserRole)
            return -1 if ins not in pipeline_node_ins_list else pipeline_node_ins_list.index(ins)

        curr_edit_index=index_from_item(curr_edit_listitem)
        curr_option_index=index_from_item(curr_option_listitem)

        self.ui.pipeEditList.clear()
        self.ui.pipeOptionViewList.clear()
        for item in pipeline_node_ins_list:
            tmp_listitem=QListWidgetItem(item.get_ins_name())
            tmp_listitem.setData(Qt.ItemDataRole.UserRole,item)
            self.ui.pipeEditList.addItem(tmp_listitem)
            self.ui.pipeOptionViewList.addItem(QListWidgetItem(tmp_listitem))
        self.ui.pipeEditList.setCurrentRow(curr_edit_index)
        self.ui.pipeOptionViewList.setCurrentRow(curr_option_index)

    def pipe_option_changed(self,row:int):
        pipe_option_con=self.ui.pipeOptionContainer
        pipe_node_option_con=self.ui.pipeOptionContainer
        curr=self.ui.pipeOptionViewList.currentItem()
        if(curr!=None):
            pipe_node:PipelineNode=curr.data(Qt.ItemDataRole.UserRole)
            pytrans_utils.qwidget_cleanup(pipe_option_con)
            self.ui.pipeOptionTab.layout().addWidget(pipe_option_con)
            pipe_node.option_ui_setup(pipe_option_con)
        else:
            pytrans_utils.qwidget_cleanup(pipe_option_con)
            pytrans_utils.qwidget_cleanup(pipe_node_option_con)

    def pipe_edit_changed(self,row:int):
        pass

    def pipeline_run(self):
        self.view_hub.main.listener_hub.event_inqueue(
            PyTransEvent(PyTransEvent.Type.PIPELINE_RUN)
        )


