import cv2
import numpy as np
from skimage.exposure import match_histograms


def normalize(mask, range_val=255):
    """Normalize an image to a given range."""
    return (range_val * (mask - np.min(mask)) / np.ptp(mask)).astype(np.uint8)


def find_darkest_point(image, mask):
    """Find the darkest pixel within a mask."""
    return np.unravel_index(np.argmin(image[mask]), image.shape)


def apply_histogram_matching(img, ref_path):
    """Match histogram of image to reference."""
    ref = cv2.imread(ref_path, 0)
    matched = match_histograms(img, ref)
    matched = np.clip(matched, img.min(), img.max())
    return matched.astype(img.dtype)