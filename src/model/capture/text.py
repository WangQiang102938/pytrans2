from model.capture.capture_node import CaptureNode


class TextNode(CaptureNode):
    def node_type(self):
        return self.Type.TEXT
