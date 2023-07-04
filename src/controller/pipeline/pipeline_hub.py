from enum import Enum, auto
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sqlalchemy
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

from view.view_hub import ViewController

if TYPE_CHECKING:
    from controller.controller_hub import ControllerHub

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey

Base: DeclarativeMeta = declarative_base()
T = TypeVar("T")


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

        self.ctrl_hub.sync_appdata_table(Base)
        self.appdata_session = self.ctrl_hub.main.model_hub.gen_appdata_session()

    def save_pipe_config(self):
        self.appdata_session.query(PipelineNodeRecord).delete()
        self.appdata_session.query(PipeNodeLinkRecord).delete()
        for i, pipe_ins in enumerate(self.pipeline_node_ins):
            pipe_record = PipelineNodeRecord(
                uuid=pipe_ins.uuid.__str__(),
                seq_id=i,
                cls_name=pipe_ins.name,
                configs="".encode(),
            )
            self.appdata_session.merge(pipe_record)
        for pipe_ins in self.pipeline_node_ins:
            for in_key, out in pipe_ins.link_info.items():
                link_record = PipeNodeLinkRecord(
                    out_uuid=out[0].uuid.__str__(),
                    out_key=out[1],
                    in_key=in_key,
                    in_uuid=pipe_ins.uuid.__str__(),
                )
                self.appdata_session.merge(link_record)
        self.appdata_session.commit()

    def load_pipe_config(self):
        # load pipes
        pipe_infos = (
            self.appdata_session.query(PipelineNodeRecord)
            .order_by(sqlalchemy.asc(PipelineNodeRecord.seq_id))
            .all()
        )
        self.pipeline_node_ins.clear()
        ins_uuid_kw = dict[str, PipelineNode]()
        for info in pipe_infos:
            cls = None
            for pipe_cls in self.pipeline_node_cls:
                if pipe_cls.name == info.cls_name:
                    cls = pipe_cls
                    break
            if cls == None:
                continue
            ins = cls(self)
            ins.uuid = info.uuid
            ins.load_config(info.configs)
            ins_uuid_kw[ins.uuid] = ins
            self.pipeline_node_ins.append(ins)
        # load links
        link_infos = self.appdata_session.query(PipeNodeLinkRecord).all()
        for info in link_infos:
            if info.in_uuid not in ins_uuid_kw or info.out_uuid not in ins_uuid_kw:
                continue
            in_ins = ins_uuid_kw[info.in_uuid]
            out_ins = ins_uuid_kw[info.out_uuid]
            in_ins.set_link(out_ins, info.out_key, info.in_key)
        self.ctrl_hub.main.listener_hub.post_event(
            PyTransEvent(
                PyTransEvent.Type.UI_UPDATE, ViewController.UpdateSignal.CONFIG_RELOAD
            )
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

    def load_config(self, config: bytes):
        pass


class PipelineNodeRecord(Base):
    __tablename__ = "PipelineHub_Nodes"

    uuid = Column(String(192), primary_key=True)
    seq_id = Column(Integer, unique=True, nullable=False)
    cls_name = Column(String(256), nullable=False)
    configs = Column(LargeBinary)


class PipeNodeLinkRecord(Base):
    __tablename__ = "PipelineHub_Links"

    id = Column(Integer, primary_key=True, autoincrement=True)

    out_uuid = Column(String(256), ForeignKey("PipelineHub_Nodes.uuid"))
    out_key = Column(String(256), nullable=False)
    in_uuid = Column(String(256), ForeignKey("PipelineHub_Nodes.uuid"))
    in_key = Column(String(256), nullable=False)
