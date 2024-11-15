from enum import Enum, auto
import os
import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from view.file_io.io_viewhub import IOViewhub
from view.pipeline.pipeline_viewhub import PipelineViewhub
from view.preview.preview_hub import PreviewHub

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import PyTransApp


class ViewHub:
    def __init__(self, main: 'PyTransApp') -> None:
        self.main = main
        self.ui = main.ui
        self.preview_hub = PreviewHub(self)
        self.pipe_viewhub=PipelineViewhub(self)
        self.io_viewhub=IOViewhub(self)
