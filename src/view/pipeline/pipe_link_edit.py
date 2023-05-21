from enum import Enum, auto
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from controller.pipeline.pipeline_hub import PipelineNode
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
import PyQt6.sip as sip
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from view.pipeline.pipeline_viewhub import PipelineViewhub

class PipeLinkEditWidget(QFrame):
    def bind(self,pipe_hub:'PipelineViewhub'):
        self.pipe_hub=pipe_hub
        self.container=pipe_hub.ui.pipeLinkEditCon

        self.working_pipelist_widget=self.pipe_hub.ui.pipeEditList
        self.pipe_node_ins_list=pipe_hub.pipeline_ctrlhub.pipeline_node_ins

        self.main_layout=QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)

        # self.setStyleSheet("border:1px solid red")

        self.container.setLayout(QVBoxLayout())
        self.container.layout().setContentsMargins(0,0,0,0)
        self.container.layout().addWidget(self)
        self.current_ins_changed(-1)
        self.working_pipelist_widget.currentItemChanged.connect(self.current_ins_changed)
        return self

    def get_current_ins(self) -> PipelineNode:
        curr_item=self.working_pipelist_widget.currentItem()
        return None if not (
            isinstance(curr_item,QListWidgetItem)
            and isinstance(curr_item.data(Qt.ItemDataRole.UserRole),PipelineNode)
        ) else curr_item.data(Qt.ItemDataRole.UserRole)

    def current_ins_changed(self,row:int):
        # Cleanup layout
        # while self.main_layout.itemAt(0)!=None:
        #     QObjectCleanupHandler().add(self.main_layout.itemAt(0).widget())
        #     self.main_layout.removeItem(self.main_layout.itemAt(0))
        for item in self.children():
            QObjectCleanupHandler().add(item)
        current_ins=self.get_current_ins()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        scroll_area=QScrollArea(self)
        self.layout().addWidget(scroll_area)
        scroll_area.setLayout(QVBoxLayout())
        self.main_layout=scroll_area.layout()
        if current_ins==None:
            return
        for key in current_ins.get_port_keys(input_port=True):
            self.main_layout.addWidget(PipeLinkItem().bind(self,key))
        self.main_layout.addItem(QSpacerItem(1,1,QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Expanding))


class PipeLinkItem(QGroupBox):
    def bind(self,container:PipeLinkEditWidget,input_key:str):
        self.container=container
        self.input_key=input_key

        self.main_layout=QHBoxLayout(self)
        self.output_ins_combo=QComboBox(self)
        self.output_key_combo=QComboBox(self)
        self.setTitle(input_key)

        self.main_layout.addWidget(self.output_ins_combo)
        self.main_layout.addWidget(self.output_key_combo)
        self.main_layout.setContentsMargins(4,4,4,4)

        self.output_ins_combo.addItem('N/A','N/A')
        curr_ins=self.container.get_current_ins()
        for ins in self.container.pipe_node_ins_list:
            if ins is curr_ins:
                continue
            self.output_ins_combo.addItem(
                ins.get_ins_name(),ins
            )

        self.output_ins_combo.activated.connect(self.output_ins_changed)
        self.output_key_combo.activated.connect(self.output_key_changed)

        self.output_ins_combo.setMaximumWidth(100)

        rec_ins=self.get_rec_ins_key()[0]
        if(rec_ins!=None):
            index=self.output_ins_combo.findData(rec_ins)
            self.output_ins_combo.setCurrentIndex(index)
            self.output_ins_changed(0)
        return self

    def get_rec_ins_key(self):
        curr_in_ins=self.container.get_current_ins()
        if self.input_key in curr_in_ins.link_info:
            return curr_in_ins.link_info[self.input_key]
        return (None,None)

    def output_ins_changed(self,row:int):
        curr_out_ins=self.output_ins_combo.currentData()
        if(curr_out_ins=='N/A'):
            self.output_key_combo.clear()
            self.output_key_changed(-1)
        elif(curr_out_ins in self.container.pipe_node_ins_list):
            curr_out_ins:PipelineNode=curr_out_ins
            output_keys=curr_out_ins.get_port_keys(False)
            self.output_key_combo.clear()
            for key in output_keys:
                self.output_key_combo.addItem(key)
            rec_key=self.get_rec_ins_key()[1]
            if(rec_key!=None):
                self.output_key_combo.setCurrentIndex(
                    self.output_key_combo.findText(rec_key)
                )
            else:
                self.output_key_changed(0)


    def output_key_changed(self,row:int):
        output_ins:PipelineNode=self.output_ins_combo.currentData()
        output_portkey:str=self.output_key_combo.currentText()
        input_ins=self.container.get_current_ins()
        if input_ins==None:
            return
        if row==-1 and self.input_key in input_ins.link_info:
            del input_ins.link_info[self.input_key]
            return
        input_ins.set_link(output_ins,output_portkey,self.input_key)
