from model.doc import WorkingDoc
from listener.listener_hub import PyTransEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import PyTransApp
import uuid
import sqlalchemy
import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session
from typing import TYPE_CHECKING, TypeVar


ORMBase: DeclarativeMeta = declarative_base()

T = TypeVar("T", bound=DeclarativeMeta)


class AppConfigMemo(ORMBase):
    __tablename__ = "AppConfigMemo"

    _id = sqla.Column(sqla.BINARY, primary_key=True)
    ins_id = sqla.Column(sqla.String)
    ins_key = sqla.Column(sqla.String)
    seq = sqla.Column(sqla.Integer, nullable=True)
    str_val = sqla.Column(sqla.String, nullable=True)
    bin_val = sqla.Column(sqla.BINARY, nullable=True)

    @classmethod
    def get_valid_ins(
        cls,
        session: Session,
        ins_id: str,
        ins_key: str,
        seq: int = None,
        ignore_seq=True,
        new_when_not_exist=True,
    ):
        query = session.query(cls).filter_by(ins_id=ins_id, ins_key=ins_key)
        query = query if not ignore_seq else query.filter_by(seq=seq)
        result = query.first()
        if result == None and new_when_not_exist:
            result = AppConfigMemo(
                _id=uuid.uuid1().bytes, ins_id=ins_id, ins_key=ins_key
            )
            session.merge(result)
        return result

    def get_valid_ins_list(
        cls,
        session: Session,
        ins_id: str,
        ins_key: str,
        asc=True,
    ):
        query = session.query(cls).filter_by(ins_id=ins_id, ins_key=ins_key)
        result = query.order_by(cls.seq.asc() if asc else cls.seq.desc()).all()
        return result


class ModelHub:
    def __init__(self, main: "PyTransApp") -> None:
        self.main = main
        self.working_doc: WorkingDoc = None
        self.opened_docs = list[WorkingDoc]()

        self.appdata_engine = sqlalchemy.create_engine("sqlite:///app_data.db")
        self.session_cls = sessionmaker(bind=self.appdata_engine)
        self.session = self.session_cls()
        self.sync_appdata_tables(ORMBase)

    def gen_appdata_session(self):
        return self.session_cls()

    def sync_appdata_tables(self, base: DeclarativeMeta):
        base.metadata.create_all(self.appdata_engine)

    def add_doc(self, doc: WorkingDoc, background=False):
        if not isinstance(doc, WorkingDoc):
            return
        self.opened_docs.append(doc)
        if not background:
            self.working_doc = doc
            self.main.listener_hub.post_event(PyTransEvent(PyTransEvent.Type.UI_UPDATE))

    def get_config_with_sync(
        self,
        ins_id: str,
        key: str,
        val_str: str = None,
        val_bin: bytes = None,
    ):
        orm_ins = AppConfigMemo.get_valid_ins(self.session, ins_id, key)
        if val_str != None or val_bin != None:
            orm_ins.str_val = orm_ins.str_val if not val_str else val_str
            orm_ins.bin_val = orm_ins.bin_val if not val_bin else val_bin
            self.session.merge(orm_ins)
            self.session.commit()
        return orm_ins
