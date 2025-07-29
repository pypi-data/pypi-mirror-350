from morphocut import Node, Output, ReturnOutputs
import numpy as np
from morphocut.image import RegionProperties


class DummyRegionProps:
    def __init__(self, shape):
        small = 1e-6

        self.area = 1
        self.perimeter = small
        self.filled_area = 1
        self.min_intensity = 0
        self.max_intensity = 0
        self.mean_intensity = 0
        self.image = np.zeros(shape, dtype=bool)
        self.bbox = (0, 0, 1, 1)
        self.bbox_area = 1
        self.centroid = (0.0, 0.0)
        self.equivalent_diameter = small
        self.major_axis_length = small
        self.minor_axis_length = small
        self.orientation = 0.0
        self.solidity = small
        self.extent = small
        self.eccentricity = small
        self.convex_area = 1
        self.image_filled = np.zeros(shape, dtype=bool)
        self.coords = np.empty((0, 2))
        self.label = -1
        self.euler_number = 0
        self.local_centroid = (0.0, 0.0)


@ReturnOutputs
@Output("regionprops")
class SafeImageProperties(Node):
    def __init__(self, mask, image):
        super().__init__()
        self.mask = mask
        self.image = image

    def transform(self, mask: np.ndarray, image: np.ndarray):
        if np.count_nonzero(mask) == 0:
            print("[WARNING] Empty mask — returning DummyRegionProps.")
            return DummyRegionProps(mask.shape)
        else:
            return RegionProperties(
                tuple(slice(0, s) for s in mask.shape),
                True,
                mask,
                image,
                True,
            )
