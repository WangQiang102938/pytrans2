from model.capture.capture_node import CaptureNode


class ImageNode(CaptureNode):
    def node_type(self):
        return self.Type.IMAGE
