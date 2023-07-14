import pickle
from sqlalchemy import Column, Integer, String, BINARY, Double, DateTime, text
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session
import sqlalchemy
from enum import Enum, auto
from typing import Any, Callable, Type, Union
from PIL.Image import Image
import uuid
from model.capture.capture_node import CaptureNode
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from controller.io.io_hub import IOMemo
import datetime

ORMBase: DeclarativeMeta = declarative_base()

T = TypeVar("T", bound=DeclarativeMeta)


class RawDataORM(ORMBase):
    __tablename__ = "RawData"

    raw_uuid = Column(BINARY, unique=True, primary_key=True)
    raw_data = Column(BINARY, nullable=True)


class KeyValORM(ORMBase):
    __tablename__ = "PyTransDoc"

    key = Column(String, unique=True, primary_key=True)
    str_val = Column(String, nullable=True)
    data_rawuuid = Column(BINARY, nullable=True)
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
    parent_uuid = Column(BINARY, nullable=True)
    node_type = Column(String)
    seq = Column(Integer, autoincrement=True)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(
        DateTime(), onupdate=datetime.datetime.now, default=datetime.datetime.now
    )

    @classmethod
    def get_valid_ins(cls, session: Session, _uuid: bytes, strict=True):
        ins = session.query(cls).filter_by(_uuid=_uuid).first()
        if ins == None:
            if strict:
                return None
            ins = cls(_uuid=_uuid)
            session.merge(ins)
        return ins


class VisualORM(ORMBase):
    __tablename__ = "PyTransVisual"

    capture_uuid = Column(BINARY, primary_key=True)
    page_no = Column(Integer)
    top = Column(Double)
    bottom = Column(Double)
    left = Column(Double)
    right = Column(Double)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(DateTime(), onupdate=datetime.datetime.now)

    @classmethod
    def get_valid_ins(cls, session: Session, _uuid: bytes, strict=True):
        ins = session.query(cls).filter_by(capture_uuid=_uuid).first()
        if ins == None:
            if strict:
                return None
            ins = cls(capture_uuid=_uuid)
            session.merge(ins)
        return ins


class MemoORM(ORMBase):
    __tablename__ = "PyTransMemo"

    _uuid = Column(BINARY, primary_key=True, default=lambda: uuid.uuid1().bytes)
    capture_uuid = Column(BINARY, nullable=True)
    memo_identifier = Column(String)
    memo_key = Column(String)
    str_val = Column(String, nullable=True)
    data_rawuuid = Column(BINARY, nullable=True)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(DateTime(), onupdate=datetime.datetime.now)

    @classmethod
    def get_valid_ins(
        cls,
        session: Session,
        memo_identifier: str,
        memo_key: str,
        cap_uuid: bytes = None,
        strict=True,
    ):
        ins = (
            session.query(cls)
            .filter_by(
                memo_identifier=memo_identifier,
                memo_key=memo_key,
                capture_uuid=cap_uuid,
            )
            .first()
        )
        if ins == None:
            if strict:
                return None
            ins = cls(
                _uuid=uuid.uuid1().bytes,
                memo_identifier=memo_identifier,
                memo_key=memo_key,
                capture_uuid=cap_uuid,
            )
            session.merge(ins)
        return ins


class CapNodeType(Enum):
    RAW = auto()
    ROOT = auto()
    CONTAINER = auto()
    TEXT = auto()
    IMAGE = auto()
    STRUCTURE = auto()


class WorkingDoc:
    class ORM:
        KeyValORM = KeyValORM
        MemoORM = MemoORM
        VisualORM = VisualORM
        CaptureORM = CaptureORM
        RawDataORM=RawDataORM

    class ConfigKeys(Enum):
        DocTitle = "DocTitle"
        CaptureRootUUID = "CaptureRootUUID"
        FocusUUID = "FocusUUID"
        PageCache = "PageCache"

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

        self.doc_cache = dict[str, Any]()

        self.db_path = db_path
        self.db_engine = sqlalchemy.create_engine(f"sqlite:///{self.db_path}")
        self.sessionmaker = sessionmaker(bind=self.db_engine)

        ORMBase.metadata.create_all(self.db_engine)
        self.session = self.gen_session()

        root_node_orm = self.get_capture_node()
        root_node_orm.node_type = CapNodeType.ROOT.name
        self.commit_orm(root_node_orm)
        self.get_kv_with_update(
            self.ConfigKeys.CaptureRootUUID.value, raw_val=root_node_orm._uuid
        )
        self.get_kv_with_update(
            self.ConfigKeys.FocusUUID.value, raw_val=root_node_orm._uuid
        )

    def get_cap_root_uuid(self):
        return uuid.UUID(
            self.get_kv_with_update(self.ConfigKeys.CaptureRootUUID.value).data_rawuuid
        )

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

    def get_orm_query(self, orm_cls: Type[T]):
        try:
            return self.session.query(orm_cls)
        except Exception:
            return None

    def get_kv_with_update(self, key: str, str_val: str = None, raw_val: bytes = None):
        read_flag = str_val == None and raw_val == None
        kv_ins = self.ORM.KeyValORM.get_valid_ins(self.session, key, strict=read_flag)
        if not read_flag:
            kv_ins.str_val = str_val if str_val != None else kv_ins.str_val
            kv_ins.data_rawuuid = raw_val if raw_val != None else kv_ins.data_rawuuid
            self.session.merge(kv_ins)
            self.session.commit()
        return kv_ins

    def get_memo_with_update(
        self,
        memo_identifier: str,
        memo_key: str,
        cap_uuid: bytes = None,
        str_val: str = None,
        raw_val: bytes = None,
    ):
        read_flag = str_val == None and raw_val == None
        orm_ins = self.ORM.MemoORM.get_valid_ins(
            self.session, memo_identifier, memo_key, cap_uuid, read_flag
        )
        if not read_flag:
            orm_ins.str_val = str_val if str_val != None else orm_ins.str_val
            orm_ins.data_rawuuid = raw_val if raw_val != None else orm_ins.data_rawuuid
            self.commit_orm(orm_ins)
        return orm_ins

    def get_capture_node(self, _uuid: bytes = None, read_mode=False):
        _uuid = _uuid if _uuid != None else uuid.uuid1().bytes
        orm_ins = self.ORM.CaptureORM.get_valid_ins(self.session, _uuid, read_mode)
        return orm_ins

    def get_visual_info(self, capture_uuid: bytes, read_mode=False):
        orm_ins = self.ORM.VisualORM.get_valid_ins(self.session, capture_uuid, read_mode)
        return orm_ins

    def commit_orm(self, *orm_ins: DeclarativeMeta):
        for ins in orm_ins:
            try:
                self.session.merge(ins)
            except Exception as e:
                print(e)
        self.session.commit()

    def get_doctitle_with_update(self, set_new_title: str = None) -> str:
        title_kv = self.get_kv_with_update(
            self.ConfigKeys.DocTitle.value, str_val=set_new_title
        )
        return None if title_kv == None else title_kv.str_val

    def delete_me(self):
        try:
            import os

            os.remove(self.db_path, dir_fd=None)
        except:
            pass

    def walk_cap_tree(
        self,
        parent_uuid: bytes,
        callback: Callable[[CaptureORM], None],
        parent_orm: CaptureORM = None,
    ):
        parent_orm = (
            self.get_capture_node(parent_uuid) if parent_orm == None else parent_orm
        )
        children = (
            self.get_orm_query(CaptureORM)
            .filter_by(parent_uuid=parent_orm._uuid)
            .order_by(CaptureORM.seq.asc())
            .all()
        )
        for child in children:
            self.walk_cap_tree(callback=callback, parent_orm=child)
        callback(parent_orm)

    def save_doc(self):
        self.get_kv_with_update(
            self.ConfigKeys.PageCache.value, raw_val=pickle.dumps(self.page_cache)
        )

    def load_doc(self):
        self.page_cache = pickle.loads(
            self.get_kv_with_update(self.ConfigKeys.PageCache.value).data_rawuuid
        )

    def put_raw_data(self,data:bytes):
        tmp_data_orm=
