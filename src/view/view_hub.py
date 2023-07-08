from enum import Enum, auto
import os
import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import my_utils

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import PyTransApp


class ViewController:
    class UpdateSignal(Enum):
        DEFAULT = auto()
        UPDATE_FOCUS = auto()
        CONFIG_RELOAD = auto()

    def __init__(self, view_hub: "ViewHub") -> None:
        self.view_hub = view_hub
        self.passive_mode = False

    def update(self, signal=UpdateSignal.DEFAULT, *args, **kwargs):
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

    def update_all(self, signal=ViewController.UpdateSignal.DEFAULT, *args, **kwargs):
        for view_ctrler in self.view_controllers:
            view_ctrler.passive_mode = True
            view_ctrler.update(signal, *args, **kwargs)
            view_ctrler.passive_mode = False
