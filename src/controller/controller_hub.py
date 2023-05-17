from controller.io.io_hub import IOHub


from typing import TYPE_CHECKING

from controller.pipeline.pipeline_hub import PipelineHub
if TYPE_CHECKING:
    from main import PyTransApp

class ControllerHub:
    def __init__(self,main:'PyTransApp') -> None:
        self.main=main
        self.ui=main.ui
        self.io_hub=IOHub(self)
        self.pipeline_hub=PipelineHub(self)








