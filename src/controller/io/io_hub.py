from enum import Enum, auto
from typing import Callable
from model.doc import WorkingDoc

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.controller_hub import ControllerHub

class IOHub:
    class OPEN_MODE(Enum):
        RAW=auto()
        LOCAL_PDF=auto()
        ONLINE_PDF=auto()

    def __init__(self,main_hub:'ControllerHub') -> None:
        self.main_hub=main_hub

    def open_doc(self,opener:'OpenModule'):
        self.main_hub.main.model_hub.add_doc(opener.open())

class OpenModule:
    def open(self)->WorkingDoc:
        return WorkingDoc()

    def set_callback(self,callback:Callable[[float,float],None]):
        self.callback=callback
