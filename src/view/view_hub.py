from enum import Enum, auto
import os
import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from model.capture.capture_node import CaptureNode
import my_utils

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import PyTransApp


class ViewController:
    class UpdateSignal(Enum):
        UPDATE_ALL = auto()
        UPDATE_FOCUS = lambda x: x if isinstance(x, CaptureNode) else None

    def __init__(self, view_hub: "ViewHub") -> None:
        self.view_hub = view_hub

    def update(self, signal=UpdateSignal.UPDATE_ALL, *args, **kwargs):
        pass


class ViewHub:
    def __init__(self, main: "PyTransApp") -> None:
        self.main = main
        self.ui = main.ui
        self.view_controllers = [
            x(self)
            for x in my_utils.scan_class(os.path.split(__file__)[0], ViewController)
        ]
        # self.preview_hub = PreviewHub(self)
        # self.pipe_viewhub = PipelineViewhub(self)
        # self.io_viewhub = IOViewhub(self)

    def update_all(
        self, signal=ViewController.UpdateSignal.UPDATE_ALL, *args, **kwargs
    ):
        for view_ctrler in self.view_controllers:
            view_ctrler.update(signal,*args, **kwargs)
