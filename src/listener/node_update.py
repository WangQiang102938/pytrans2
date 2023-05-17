from enum import Enum,auto

from listener.listener_hub import Listener, PyTransEvent

class NodeUpdateType(Enum):
    TYPE_CHANGE=auto()
    MEMO_UPDATE=auto()

class DefaultNodeUpdate(Listener):
    def listened_event(self, event: PyTransEvent) -> bool:
        return event.type==event.Type.NODE_UPDATE
    
    def event_handler(self, event: PyTransEvent):
        return super().event_handler(event)