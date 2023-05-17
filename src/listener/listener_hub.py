from enum import Enum, auto
import os
import sys
import inspect
import importlib
import importlib.machinery
from typing import Any, TYPE_CHECKING
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


if TYPE_CHECKING:
    from main import PyTransApp


class ListenerHub:
    def __init__(self, main: 'PyTransApp') -> None:
        self.main = main
        self.listener_set = list[Listener]()
        self.prev_queue = list[PyTransEvent]()
        self.curr_queue = list[PyTransEvent]()
        self.nest_queue = list[PyTransEvent]()
        self.active_flag = False
        self.callback_set_flag = False
        self.scan_listeners(os.path.split(__file__)[0])

    def scan_listeners(self, path):
        sys.path.append(path) if path not in sys.path else None
        for root, dirs, files in os.walk(path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if (ext != '.py' or __file__ == f"{root}/{file}"):
                    continue
                module = importlib.machinery.SourceFileLoader(
                    filename, f"{root}/{file}").load_module()
                for clsname, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, Listener):
                        if (obj != Listener and obj not in [x.__class__ for x in self.listener_set]):
                            self.listener_set.append(obj(self))

    def event_inqueue(self, event: 'PyTransEvent'):
        if not self.callback_set_flag:
            QTimer.singleShot(0, self.process_event)
            self.callback_set_flag = True
        if self.active_flag:
            self.nest_queue.append(event)
        else:
            self.curr_queue.append(event)

    def process_event(self):
        self.active_flag = True
        event_queue = self.prev_queue+self.curr_queue
        self.prev_queue.clear()
        self.curr_queue.clear()
        while event_queue.__len__() > 0:
            for event in event_queue:
                for listener in self.listener_set:
                    if listener.listened_event(event):
                        try:
                            listener.event_handler(event)
                        except Exception as e:
                            print(f"Exception happened at event:{event.type}")
            event_queue = self.nest_queue.copy()
            self.nest_queue.clear()
        self.active_flag = False
        self.callback_set_flag = False


class Listener:
    def __init__(self, l_hub: ListenerHub) -> None:
        self.listener_hub = l_hub
        self.main = l_hub.main

    def listened_event(self, event: 'PyTransEvent') -> bool:
        return PyTransEvent.Type.NOP == event.type

    def event_handler(self, event: 'PyTransEvent'):
        pass


class PyTransEvent:
    def __init__(self, type: 'PyTransEvent.Type', *args, **kwargs) -> None:
        self.type = type
        self.args = args
        self.kwargs = kwargs

    class Type(Enum):
        NOP = auto()
        UI_UPDATE = auto()
        NODE_UPDATE = auto()
