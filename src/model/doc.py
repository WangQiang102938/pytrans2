from sqlalchemy import Column, Integer, String, BINARY, Double, DateTime
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String)
    str_val = Column(String, nullable=True)
    raw_val = Column(BINARY, nullable=True)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(DateTime(), onupdate=datetime.datetime.now)


class CaptureORM(ORMBase):
    __tablename__ = "PyTransCapture"

    uuid = Column(BINARY, primary_key=True)
    parent_uuid = Column(BINARY)
    node_type = Column(String)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(DateTime(), onupdate=datetime.datetime.now)


class VisualORM(ORMBase):
    __tablename__ = "PyTransVisual"

    uuid = Column(BINARY, primary_key=True)
    capture_uuid = Column(BINARY)
    page_no = Column(Integer)
    top = Column(Double)
    bottom = Column(Double)
    left = Column(Double)
    right = Column(Double)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(DateTime(), onupdate=datetime.datetime.now)


class MemoORM(ORMBase):
    __tablename__ = "PyTransMemo"

    uuid = Column(BINARY, primary_key=True, default=lambda: uuid.uuid1().bytes)
    capture_uuid = Column(BINARY, nullable=True)
    memo_identifier = Column(String)
    memo_key = Column(String)
    str_val = Column(String, nullable=True)
    raw_val = Column(BINARY, nullable=True)
    date_c = Column(DateTime(), default=datetime.datetime.now)
    date_m = Column(DateTime(), onupdate=datetime.datetime.now)


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

    def set_kv(self, key: str, val: Union[str, bytes]):
        is_str = isinstance(val, str)
        is_bin = isinstance(val, bytes)
        return self.set_orm(
            KeyValORM(
                key=key,
                str_val=val if is_str else None,
                raw_val=val if is_bin else None,
            )
        )

    def get_kv_orm(self, key, all=False):
        query = self.get_orm_session(KeyValORM).filter_by(key=key)
        return query.all() if all else query.first()

    def set_memo(
        self,
        memo_identifier: str,
        memo_key: str,
        cap_uuid: uuid.UUID = None,
        str_val="",
        raw_val: bytes = None,
    ):
        return self.set_orm(
            self.ORM.Memo(
                memo_identifier=memo_identifier,
                memo_key=memo_key,
                str_val=str_val,
                raw_val=raw_val,
            )
        )

    def get_memo(
        self,
        memo_identifier: str,
        memo_key: str,
        cap_uuid: uuid.UUID = None,
        str_mode=False,
        both_mode=False,
    ):
        result = (
            self.get_orm_session(self.ORM.Memo)
            .filter_by(
                memo_identifier=memo_identifier, memo_key=memo_key, cap_uuid=cap_uuid
            )
            .first()
        )
        if result == None or (str_mode == False and both_mode == False):
            return None
        if both_mode:
            return result.str_val, result.raw_val
        return result.str_val if str_mode else result.raw_val

    def doc_title(self, set_new_title: str = None) -> str:
        if isinstance(set_new_title, str):
            self.set_kv(self.ConfigKeys.DocTitle.value, set_new_title)
        return self.get_kv_orm(self.ConfigKeys.DocTitle.value).str_val

    def delete_me(self):
        try:
            import os

            os.remove(self.db_path, dir_fd=None)
        except:
            pass
