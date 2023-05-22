from model.doc import WorkingDoc
from listener.listener_hub import PyTransEvent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import PyTransApp

class ModelHub:
    def __init__(self,main:'PyTransApp') -> None:
        self.main=main
        self.working_doc:WorkingDoc=None
        self.opened_docs=list[WorkingDoc]()

    def add_doc(self,doc:WorkingDoc,background=False):
        if not isinstance(doc,WorkingDoc):
            return
        self.opened_docs.append(doc)
        if not background:
            self.working_doc=doc
            self.main.listener_hub.post_event(
                PyTransEvent(PyTransEvent.Type.UI_UPDATE)
            )

