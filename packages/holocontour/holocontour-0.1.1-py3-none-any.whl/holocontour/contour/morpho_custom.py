from morphocut import Node, Output, ReturnOutputs
from holocontour.contour.contour_detection import find_contours

@ReturnOutputs
class HoloContourNode(Node):
    mask = Output("mask")
    plot = Output("plot")
    outputs = (mask, plot)

    def __init__(self, img, contour_params):
        super().__init__()
        self.img = img
        self.contour_params = contour_params

    def transform(self, img):
        return find_contours(img, **self.contour_params)
