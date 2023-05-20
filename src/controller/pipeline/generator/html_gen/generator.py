from enum import Enum
from typing import Any, List
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PIL.Image import Image
from controller.pipeline.pipeline_hub import PipeMemo, PipeUpdateMode, PipelineHub, PipelineNode
from model.capture.capture_node import CaptureNode
import utils.pipeline_utils as pipeline_utils
import utils

class PortEnum(Enum):
    IN_ORIGIN='origin_in:[[str]]'
    IN_TRANS='translated'
