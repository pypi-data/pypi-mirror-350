import numpy as np
from skimage import measure
from skimage.draw import polygon2mask


def contour_mask_union(contours, shape):
    """Create a union mask from multiple contours."""
    union_mask = np.zeros(shape, dtype=bool)
    for contour in contours:
        union_mask |= measure.grid_points_in_poly(shape, contour)
    return union_mask


def filter_contours_by_intensity(contours, image, threshold, use_median=False):
    """Filter contours by intensity threshold."""
    filtered = []
    for contour in contours:
        req_mask = polygon2mask(image.shape[:2], contour).astype(bool)
        region_values = image[req_mask]
        stat = np.median(region_values) if use_median else np.mean(region_values)

        # contour_coords = np.array(list(zip(contour[:, 0].astype(int), contour[:, 1].astype(int))))
        # stat = np.mean(image[contour_coords[:, 0], contour_coords[:, 1]])

        if stat <= threshold:
            filtered.append(contour)
    return filtered