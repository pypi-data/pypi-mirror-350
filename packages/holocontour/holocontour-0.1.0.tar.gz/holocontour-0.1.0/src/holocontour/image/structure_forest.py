from pathlib import Path
import numpy as np
import cv2
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.feature import canny
from skimage.morphology import binary_closing, disk, remove_small_objects, convex_hull_image
from skimage.measure import label, regionprops
from scipy.ndimage import binary_fill_holes
import importlib.resources as pkg_resources
from holocontour import model


def structured_forest_edges(gray_img, model_path):
    rgb_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)
    sed = cv2.ximgproc.createStructuredEdgeDetection(model_path)
    edges = sed.detectEdges(np.float32(rgb_img) / 255.0)
    return edges


def region_refining(binary_image, area_thresh=25):
    cleaned = remove_small_objects(binary_image.astype(bool), min_size=area_thresh)
    filled = binary_fill_holes(cleaned)
    return filled.astype(np.uint8)


def canny_edge(image):
    if image.ndim == 3:
        image = rgb2gray(image)
    edges = canny(image)
    closed = binary_closing(edges, disk(3))
    filled = binary_fill_holes(closed)
    return region_refining(filled)


def sobel_edge(image):
    if image.ndim == 3:
        image = rgb2gray(image)
    edges = sobel(image)
    binary = edges > 0.05
    closed = binary_closing(binary, disk(3))
    filled = binary_fill_holes(closed)
    return region_refining(filled)


def region_methods():
    return {
        'structuredForest': None,  # handled separately
        'cannyEdge': canny_edge,
        'sobelEdge': sobel_edge
    }


def reg_props(mask, name_props):
    labeled_mask = label(mask)
    all_props = regionprops(labeled_mask)
    results = []
    for region in all_props:
        props = {name: getattr(region, name, None) for name in name_props}
        results.append(props)
    return results


def particle_sizer(code_dir, data_dir, im_format, save_dir, method_key, model_path, name_props, use_convex_hull):
    mask_dir = Path(save_dir) / "masks"
    mask_dir.mkdir(parents=True, exist_ok=True)

    image_paths = list(Path(data_dir).rglob(f'*{im_format}'))
    print(f"Found {len(image_paths)} images")

    methods = region_methods()
    method_func = methods.get(method_key)

    for img_path in image_paths:
        image = io.imread(img_path)
        gray = image[:, :, 0]
        # gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image

        if method_key == 'structuredForest':
            edges = structured_forest_edges(gray, model_path)
            binary = edges > 0.05
        elif method_func:
            binary = method_func(gray)
        else:
            raise ValueError(f"Unknown method: {method_key}")

        binary = remove_small_objects(binary, min_size=50)
        if use_convex_hull:
            binary = convex_hull_image(binary)

        mask_path = mask_dir / (img_path.stem + "_mask.png")
        io.imsave(mask_path, (binary * 255).astype(np.uint8))

        props_list = reg_props(binary, name_props)
        for props in props_list:
            print(f"{img_path.name} → {props}")


def generate_mask(img, use_convex_hull=False):
    with pkg_resources.path(model, "model.yml") as model_path:
        edges = structured_forest_edges(img, str(model_path))

    binary = edges > 0.05
    binary = remove_small_objects(binary, min_size=50)

    if use_convex_hull:
        binary = convex_hull_image(binary)

    return binary

