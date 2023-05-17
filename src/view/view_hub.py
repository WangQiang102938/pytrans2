from enum import Enum, auto
import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from view.preview.preview_hub import PreviewHub

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import PyTransApp


class ViewHub:
    def __init__(self, main: 'PyTransApp') -> None:
        self.main = main
        self.ui = main.ui
        self.preview_hub = PreviewHub(self)
