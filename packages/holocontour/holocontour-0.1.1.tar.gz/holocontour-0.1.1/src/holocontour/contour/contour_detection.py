import cv2
import numpy as np
from skimage import measure
from skimage.draw import polygon2mask
from holocontour.image.structure_forest import generate_mask
from holocontour.contour.toolsbox import contour_mask_union, filter_contours_by_intensity
from holocontour.image.visual import plot_segmentation_result
from holocontour.image.region_growing import region_grow
from holocontour.image.processing import apply_histogram_matching, find_darkest_point


def find_contours(img_org,
                 avg_thresh=81,
                 min_contour_area=30,
                 seed_thresh=45,
                 save_plot=False,
                 median=False,
                 hist_match=False,
                 ref_path=None):

    img = img_org.copy()

    if hist_match and ref_path:
        img = apply_histogram_matching(img_org, ref_path)

    img = cv2.medianBlur(img, 5)
    init_mask = generate_mask(img)

    seed = find_darkest_point(img_org, init_mask > 0)
    seg_mask = region_grow(img, seed)

    contours = measure.find_contours(seg_mask, 0.5)
    filtered_contours = [c for c in contours if len(c) > min_contour_area]

    while True:
        outside = np.where((img < seed_thresh) & ~seg_mask)
        if len(outside[0]) == 0:
            break
        seed = (outside[0][0], outside[1][0])
        new_mask = region_grow(img, seed)
        seg_mask |= new_mask
        new_contours = measure.find_contours(new_mask, 0.5)
        filtered_contours += [c for c in new_contours if len(c) > min_contour_area]

    valid_contours = filter_contours_by_intensity(
        filtered_contours, img_org, avg_thresh, median
    )

    union = contour_mask_union(valid_contours, img_org.shape)
    outer = max(measure.find_contours(init_mask, 0.5), key=len)
    init_mask_poly = polygon2mask(img_org.shape[:2], outer)
    union &= init_mask_poly

    final_mask = np.zeros_like(init_mask, dtype=np.uint8)
    final_contour = []
    for contour in measure.find_contours(union, 0.5):
        if len(contour) > min_contour_area:
            mask = polygon2mask(img_org.shape[:2], contour).astype(np.uint8)
            final_mask += mask
            final_contour.append(contour)

    if save_plot:
        plot = plot_segmentation_result(img_org, outer, final_contour)
    else:
        plot = None

    return final_mask > 0, plot
