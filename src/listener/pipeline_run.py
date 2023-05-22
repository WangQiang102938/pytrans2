import io
from controller.pipeline.pipeline_hub import PipeUpdateMode
from model.capture.capture_node import CaptureNode
from listener.listener_hub import Listener, PyTransEvent
from view.preview.capture_box import CaptureBoxItem
from view.preview.page import PageItem
from PIL.Image import Image
from PyQt6.QtGui import *
import my_utils as PyTransUtils

class DefaultPipelineRunListener(Listener):
    def listened_event(self, event: PyTransEvent) -> bool:
        return event.type==event.Type.PIPELINE_RUN

    def event_handler(self, event: PyTransEvent):
        working_doc = self.main.model_hub.working_doc
        preview_hub = self.main.view_hub.preview_hub
        pipeline_hub= self.main.controller_hub.pipeline_hub
        ui=self.main.ui
        process_events=lambda:self.main.app.processEvents()

        self.main.mainwindow.setEnabled(False)
        ui.pipeProgress.setRange(0,pipeline_hub.pipeline_node_ins.__len__())
        ui.pipeProgress.reset()
        process_events()
        for p_i,pipenode in enumerate(pipeline_hub.pipeline_node_ins):
            node_count=PyTransUtils.count_node(working_doc.root_node)
            ui.pipeCapNodeProgress.setRange(0,node_count)
            ui.pipeCapNodeProgress.reset()
            def dfs(node:CaptureNode,count=0):
                for child in node.children:
                    count=dfs(child,count)
                input_dict={}
                for in_key,(out_ins,out_key) in pipenode.link_info.items():
                    input_dict[in_key]=out_ins.get_output(node,out_key)
                pipenode.process_capnode(node,PipeUpdateMode.FULLY_RUN,**input_dict)
                ui.pipeCapNodeProgress.setValue(count+1)
                process_events()
                return count+1
            pipenode.process_start()
            dfs(working_doc.root_node)
            pipenode.process_end()
            ui.pipeProgress.setValue(p_i+1)
        self.main.mainwindow.setEnabled(True)



