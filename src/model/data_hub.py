from model.doc import WorkingDoc
from listener.listener_hub import PyTransEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import PyTransApp
import uuid
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from typing import TYPE_CHECKING


class ModelHub:
    def __init__(self, main: "PyTransApp") -> None:
        self.main = main
        self.working_doc: WorkingDoc = None
        self.opened_docs = list[WorkingDoc]()

        self.appdata_engine = sqlalchemy.create_engine("sqlite:///app_data.db")
        self.session_cls = sessionmaker(bind=self.appdata_engine)

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
