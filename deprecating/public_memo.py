from enum import Enum, auto
from controller.pipeline.pipeline_hub import PipeMemo

from typing import *

class PublicMemo(PipeMemo):
    def get_pipenode_name(self):
        return "PUBLIC_MEMO"

class PublicMemoType(Enum):
    IMAGE=auto()
    TEXT=auto()
    FILE_CONTENT=auto()

class PublicMemoTag(Enum):
    ORIGINAL=auto()
    MODIFIED=auto()

    IMG_CROP=auto()
    IMG2TEXT=auto()
    FORMATTED=auto()
    TRANSLATED=auto()
    ALIGNED=auto()

