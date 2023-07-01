from sqlalchemy import Column, Integer, String, create_engine
import sqlalchemy.orm
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum, auto
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from listener.listener_hub import PyTransEvent
import my_utils
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

T = TypeVar("T")
ModelBase = declarative_base()


class PipelineListRecord(ModelBase):
    __tablename__ = 'PipelineList'

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    type_name = Column(String(length=128))
    uuid = Column(String(length=256))


class LinkRecord(ModelBase):
    __tabname__ = 'PipeLinkList'

    id = Column(Integer, primary_key=True)
    out_uuid = Column(String(length=256))
    out_key = Column(String(length=64))
    in_uuid = Column(String(length=256))
    in_key = Column(String(length=64))


class PipelineHub:
    def __init__(self, ctrl_hub: "ControllerHub") -> None:
        self.ctrl_hub = ctrl_hub
        self.pipeline_node_cls = list[Type[PipelineNode]]()
        self.pipeline_node_ins = list[PipelineNode]()
        self.ui = self.ctrl_hub.ui
        self.pipeline_node_cls = my_utils.scan_class(
            os.path.split(__file__)[0], PipelineNode
        )
        # self.ctrl_hub.ui.pipeOptionCombo.currentIndexChanged.connect(self.option_tab_index_changed)
        # self.option_tab_index_changed(self.ctrl_hub.ui.pipeOptionCombo.currentIndex())
        self.sql_init()

    def sql_init(self):
        self.engine = create_engine("sqlite:///pipeline_configs.db")

        ModelBase.metadata.create_all(self.engine)
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)()

    def config_save(self):
        # remove all record
        old_pipe_records = self.session.query(PipelineListRecord).all()
        old_link_records = self.session.query(LinkRecord).all()
        for rec in old_pipe_records+old_link_records:
            self.session.delete(rec)
        for index, pipenode in enumerate(self.pipeline_node_ins):
            tmp_record = PipelineListRecord(
                type_name=pipenode.name,
                uuid=pipenode.uuid,
                index=index
            )
            self.session.add(tmp_record)
            for key, val in pipenode.link_info.items():
                tmp_link_record = LinkRecord(
                    in_uuid=pipenode.uuid,
                    in_key=key,
                    out_uuid=val[0].uuid,
                    out_key=val[1]
                )
                self.session.add(tmp_link_record)
        self.session.commit()

    def config_load(self):
        pipe_records = self.session.query(PipelineListRecord).all()

        pipe_records.sort(key=lambda x: x.index)
        self.pipeline_node_ins.clear()
        ins_uuid_dict = dict()
        for record in pipe_records:
            for cls in self.pipeline_node_cls:
                if cls.name == record.type_name:
                    tmp_ins = cls(self)
                    tmp_ins.uuid = record.uuid
                    ins_uuid_dict[record.uuid] = tmp_ins
                    break
        for ins in self.pipeline_node_ins:
            links = self.session.query(LinkRecord).filter_by(in_uuid=ins.uuid)
            for link in links:
                if link.out_uuid in ins_uuid_dict:
                    out_ins = ins_uuid_dict[link.out_uuid]
                    ins.set_link(out_ins, link.out_key, link.in_key)
        self.ctrl_hub.main.listener_hub.post_event(
            PyTransEvent(PyTransEvent.Type.UI_UPDATE)
        )

class PipeMemo:
    def __init__(self, pipe_ins: "PipelineNode") -> None:
        self.node: CaptureNode = None
        self.pipe_ins = pipe_ins

    def bind_node(self, node: CaptureNode, overwrite_flag=False):
        self.node = node
        if overwrite_flag or self.pipe_ins not in node.pipeline_memo:
            node.pipeline_memo[self.pipe_ins] = self
        return self


class PipeUpdateMode(Enum):
    BYPASS = auto()
    CAPTURE_NODE_UPDATED = auto()
    FULLY_RUN = auto()


class PipelineNode:
    name = "NAME_NOT_SET"

    def __init__(self, pipe_hub: PipelineHub) -> None:
        self.pipe_hub = pipe_hub
        self.uuid = uuid.uuid1()
        self.link_info = dict[str, Tuple[PipelineNode, str]]()

    def get_ins_name(self):
        return str(f"{self.name}@{id(self)}")

    def option_ui_setup(self, container: QWidget):
        pass

    def capnode_option_ui_setup(self, container: QWidget, node: CaptureNode = None):
        pass

    def find_memo(
        self, node: CaptureNode, cast_type: Type[T] = PipeMemo, new_if_notfound=False
    ) -> T:
        if not isinstance(node, CaptureNode):
            return None
        if self not in node.pipeline_memo:
            return cast_type(self).bind_node(node, True)
        val = node.pipeline_memo[self]
        if isinstance(val, cast_type):
            return val
        else:
            return cast_type(self).bind_node(node, True) if new_if_notfound else None

    def process_start(self):
        pass

    def process_capnode(
        self, node: CaptureNode, mode: PipeUpdateMode = PipeUpdateMode.BYPASS, **input
    ):
        return False

    def process_end(self):
        pass

    def get_output(self, node: CaptureNode, key: str) -> Any:
        return None

    def get_port_keys(self, input_port=True) -> List[str]:
        pass

    def set_link(self, out_ins: "PipelineNode", out_key: str, in_key: str):
        if not isinstance(out_ins, PipelineNode):
            return False
        if out_key not in out_ins.get_port_keys(False):
            return False
        if in_key not in self.get_port_keys():
            return False
        self.link_info[in_key] = (out_ins, out_key)
        return True
