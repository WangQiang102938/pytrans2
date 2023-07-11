from enum import Enum, auto
import os
import sys
import inspect
import importlib
import importlib.machinery
from typing import Any, TYPE_CHECKING, Callable
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from listener.listener_hub import PyTransEvent

import my_utils


if TYPE_CHECKING:
    from main import PyTransApp


class ListenerHub:
    def __init__(self, main: "PyTransApp") -> None:
        self.main = main
        self.listener_set = list[Listener]()
        self.prev_queue = list[PyTransEvent]()
        self.curr_queue = list[PyTransEvent]()
        self.nest_queue = list[PyTransEvent]()
        self.active_flag = False
        self.callback_set_flag = False
        self.scan_listeners()

    def scan_listeners(self):
        listener_clses = my_utils.scan_class(os.path.split(__file__)[0], Listener)
        for cls in listener_clses:
            self.listener_set.append(cls(self))

    def post_event(self, event: "PyTransEvent"):
        if not self.callback_set_flag:
            QTimer.singleShot(0, self.process_event)
            self.callback_set_flag = True
        if self.active_flag:
            self.nest_queue.append(event)
        else:
            self.curr_queue.append(event)

    def process_event(self):
        self.active_flag = True
        event_queue = self.prev_queue + self.curr_queue
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

    def post_callback(self, callback: Callable[[]]):
        self.post_event(PyTransEvent(PyTransEvent.Type.CALLBACK, callback))


class Listener:
    def __init__(self, l_hub: ListenerHub) -> None:
        self.listener_hub = l_hub
        self.main = l_hub.main

    def listened_event(self, event: "PyTransEvent") -> bool:
        return PyTransEvent.Type.NOP == event.type

    def event_handler(self, event: "PyTransEvent"):
        pass


class PyTransEvent:
    def __init__(self, type: "PyTransEvent.Type", *args, **kwargs) -> None:
        self.type = type
        self.args = args
        self.kwargs = kwargs

    class Type(Enum):
        NOP = auto()
        UI_UPDATE = auto()
        NODE_UPDATE = auto()
        PIPELINE_RUN = auto()
        CALLBACK = auto()


class CallbackListener(Listener):
    def listened_event(self, event: PyTransEvent) -> bool:
        return event.type == PyTransEvent.Type.CALLBACK

    def event_handler(self, event: PyTransEvent):
        try:
            event.args[0]()
        except Exception as e:
            print(e.with_traceback())
