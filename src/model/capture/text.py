from model.capture.capture_node import CaptureNode


class TextNode(CaptureNode):
    def get_node_type(self):
        return self.Type.TEXT
