from typing import Callable
from listener.listener_hub import PyTransEvent
from model.capture.capture_node import CaptureNode
from model.doc import WorkingDoc
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from typing import TYPE_CHECKING

from view.preview.capture_box import ResizeIconItem

if TYPE_CHECKING:
    from view.view_hub import ViewHub

class PreviewControl:
    def __init__(self) -> None:
        pass