from sqlalchemy import Column, Integer, String, BINARY, Double, DateTime, text
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session
import sqlalchemy
from enum import Enum, auto
from typing import Type, Union
from PIL.Image import Image
import uuid
from model.capture.capture_node import CaptureNode
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from controller.io.io_hub import IOMemo
import datetime

ORMBase: DeclarativeMeta = declarative_base()

T = TypeVar("T", bound=DeclarativeMeta)


class KeyValORM(ORMBase):
    __tablename__ = "PyTransDoc"

    key = Column(String, unique=True, primary_key=True)
    str_val = Column(String, nullable=True)
    raw_val = Column(BINARY, nullable=True)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(DateTime(), onupdate=datetime.datetime.now)

    @classmethod
    def get_valid_ins(cls, session: Session, key: str, strict=True):
        ins = session.query(cls).filter_by(key=key).first()
        if ins == None:
            if strict:
                return None
            ins = cls(key=key)
            session.merge(ins)
        return ins


class CaptureORM(ORMBase):
    __tablename__ = "PyTransCapture"

    _uuid = Column(BINARY, primary_key=True)
    parent_uuid = Column(BINARY)
    node_type = Column(String)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(DateTime(), onupdate=datetime.datetime.now)

    @classmethod
    def get_valid_ins(cls, session: Session, uuid: uuid.UUID, strict=True):
        ins = session.query(cls).filter_by(_uuid=uuid.bytes).first()
        if ins == None:
            if strict:
                return None
            ins = cls(_uuid=uuid.bytes)
            session.merge(ins)
        return ins


class VisualORM(ORMBase):
    __tablename__ = "PyTransVisual"

    _uuid = Column(BINARY, primary_key=True)
    capture_uuid = Column(BINARY)
    page_no = Column(Integer)
    top = Column(Double)
    bottom = Column(Double)
    left = Column(Double)
    right = Column(Double)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(DateTime(), onupdate=datetime.datetime.now)

    @classmethod
    def get_valid_ins(cls, session: Session, uuid: uuid.UUID, strict=True):
        ins = session.query(cls).filter_by(_uuid=uuid.bytes).first()
        if ins == None:
            if strict:
                return None
            ins = cls(_uuid=uuid.bytes)
            session.merge(ins)
        return ins


class MemoORM(ORMBase):
    __tablename__ = "PyTransMemo"

    _uuid = Column(BINARY, primary_key=True, default=lambda: uuid.uuid1().bytes)
    capture_uuid = Column(BINARY, nullable=True)
    memo_identifier = Column(String)
    memo_key = Column(String)
    str_val = Column(String, nullable=True)
    raw_val = Column(BINARY, nullable=True)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(DateTime(), onupdate=datetime.datetime.now)

    @classmethod
    def get_valid_ins(
        cls,
        session: Session,
        memo_identifier: str,
        memo_key: str,
        cap_uuid: uuid.UUID = None,
        strict=True,
    ):
        ins = (
            session.query(cls)
            .filter_by(
                memo_identifier=memo_identifier,
                memo_key=memo_key,
                capture_uuid=(cap_uuid.bytes if cap_uuid != None else None),
            )
            .first()
        )
        if ins == None:
            if strict:
                return None
            ins = cls(
                memo_identifier=memo_identifier,
                memo_key=memo_key,
                capture_uuid=(cap_uuid.bytes if cap_uuid != None else None),
            )
            session.merge(ins)
        return ins


class WorkingDoc:
    class ORM:
        KeyVal = KeyValORM
        Memo = MemoORM
        Visual = VisualORM
        Capture = CaptureORM

    class ConfigKeys(Enum):
        DocTitle = "DocTitle"

    def default_doc():
        return WorkingDoc(db_path=f"./tmp/{uuid.uuid1().__str__()}.db")

    def __init__(self, path=None, url=None, db_path="") -> None:
        self.path = path
        self.url = url
        self.filehash = None
        self.io_memo: IOMemo = None
        self.page_cache = list[Image]()
        self.root_node = CaptureNode(self, CaptureNode.Type.ROOT)
        self.focus_node = self.root_node
        self.status = self.STATUS.NOT_AVALIABLE
        self.page_no = 0

        self.db_path = db_path
        self.db_engine = sqlalchemy.create_engine(f"sqlite:///{self.db_path}")
        self.sessionmaker = sessionmaker(bind=self.db_engine)

        ORMBase.metadata.create_all(self.db_engine)
        self.session = self.gen_session()

    def gen_session(self):
        return self.sessionmaker()

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

    def set_orm(self, orm_obj: DeclarativeMeta):
        try:
            self.session.merge(orm_obj)
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_orm_session(self, orm_cls: Type[T]):
        try:
            return self.session.query(orm_cls)
        except Exception:
            return None

    def sync_kv(self, key, str_val: str = None, raw_val: bytes = None):
        read_flag = str_val == None and raw_val == None
        kv_ins = self.ORM.KeyVal.get_valid_ins(self.session, key, strict=read_flag)
        if not read_flag:
            kv_ins.str_val = str_val if str_val != None else kv_ins.str_val
            kv_ins.raw_val = raw_val if raw_val != None else kv_ins.raw_val
            self.session.merge(kv_ins)
            self.session.commit()
        return kv_ins

    def sync_memo(
        self,
        memo_identifier: str,
        memo_key: str,
        cap_uuid: uuid.UUID = None,
        str_val: str = None,
        raw_val: bytes = None,
    ):
        read_flag = str_val == None and raw_val == None
        orm_ins = self.ORM.Memo.get_valid_ins(
            self.session, memo_identifier, memo_key, cap_uuid, read_flag
        )
        if not read_flag:
            orm_ins.str_val = str_val if str_val != None else orm_ins.str_val
            orm_ins.raw_val = raw_val if raw_val != None else orm_ins.raw_val
            self.session.merge(orm_ins)
            self.session.commit()
        return orm_ins

    def sync_doc_title(self, set_new_title: str = None) -> str:
        title_kv = self.sync_kv(self.ConfigKeys.DocTitle.value, str_val=set_new_title)
        return None if title_kv == None else title_kv.str_val

    def delete_me(self):
        try:
            import os

            os.remove(self.db_path, dir_fd=None)
        except:
            pass
