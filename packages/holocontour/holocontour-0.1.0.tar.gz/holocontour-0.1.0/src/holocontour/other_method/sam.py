import os
import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt
from glob import glob
from skimage.measure import label, regionprops
from matplotlib.colors import hsv_to_rgb
from segment_anything import sam_model_registry, SamPredictor


def load_sam_model(model_type, checkpoint_dir="model"):
    os.makedirs(checkpoint_dir, exist_ok=True)
    checkpoints = {
        "vit_b": "sam_vit_b_01ec64.pth",
        "vit_l": "sam_vit_l_0b3195.pth",
        "vit_h": "sam_vit_h_4b8939.pth",
    }

    if model_type not in checkpoints:
        raise ValueError(f"Unsupported model_type: {model_type}. Choose from 'vit_b', 'vit_l', or 'vit_h'.")

    ckpt_path = os.path.join(checkpoint_dir, checkpoints[model_type])
    if not os.path.exists(ckpt_path):
        print(f"Downloading checkpoint for {model_type}...")
        import urllib.request
        url = f"https://dl.fbaipublicfiles.com/segment_anything/{checkpoints[model_type]}"
        urllib.request.urlretrieve(url, ckpt_path)

    sam = sam_model_registry[model_type](checkpoint=ckpt_path)
    sam.to("cuda" if torch.cuda.is_available() else "cpu")
    return SamPredictor(sam)


def filter_regions_by_intensity(mask, gray_image, threshold=128):
    filtered = np.zeros_like(mask, dtype=bool)
    labeled = label(mask)

    for region in regionprops(labeled, intensity_image=gray_image):
        mean_intensity = region.mean_intensity
        if mean_intensity < threshold:
            filtered[labeled == region.label] = True
    return filtered


def generate_colored_overlay(union_mask):
    labeled_union = label(union_mask)
    num_regions = labeled_union.max()

    # Random Hues for each region
    hsv_img = np.zeros((*union_mask.shape, 3), dtype=np.float32)
    for i in range(1, num_regions + 1):
        mask = labeled_union == i
        hue = np.random.rand()
        hsv_img[mask] = [hue, 1.0, 1.0]  # HSV color: random hue, full sat/val

    rgb_overlay = hsv_to_rgb(hsv_img)
    return rgb_overlay


def run_sam_on_folder(folder_path, model_type="vit_b", intensity_thresh=128):
    predictor = load_sam_model(model_type)

    image_paths = glob(os.path.join(folder_path, "*.png")) + \
                  glob(os.path.join(folder_path, "*.jpg")) + \
                  glob(os.path.join(folder_path, "*.jpeg"))

    for img_path in image_paths:
        print(f"Processing: {img_path}")
        gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            print(f"Could not read: {img_path}")
            continue

        rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        predictor.set_image(rgb)

        h, w = rgb.shape[:2]
        input_point = np.array([[w // 2, h // 2]])
        input_label = np.array([1])  # foreground

        masks, scores, _ = predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
        )

        union_mask = np.zeros_like(gray, dtype=bool)

        for i in range(len(masks)):
            # We process both foreground and background
            mask = masks[i]
            # Invert to also allow high-intensity regions if desired
            union_mask |= filter_regions_by_intensity(mask, gray, intensity_thresh)
            union_mask |= filter_regions_by_intensity(~mask, gray, intensity_thresh)

        colored_mask = generate_colored_overlay(union_mask)

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(gray, cmap='gray')
        plt.title("Original Image")
        plt.axis("off")

        plt.subplot(1, 2, 2)
        plt.imshow(gray, cmap='gray')
        plt.imshow(colored_mask, alpha=0.6)
        plt.title("Filtered Regions (Colored)")
        plt.axis("off")

        plt.suptitle(os.path.basename(img_path))
        plt.tight_layout()
        plt.show()


# === Entry Point ===
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SAM + intensity-based mask filtering")
    parser.add_argument("--folder", type=str, required=False, help="Path to folder with images")
    parser.add_argument("--model", type=str, default="vit_b", choices=["vit_b", "vit_l", "vit_h"],
                        help="SAM model variant")
    parser.add_argument("--threshold", type=int, default=128, help="Intensity threshold for region filtering")
    args = parser.parse_args()


    args.folder = r'D:\mojmas\files\Projects\Holo_contour\data\data1'
    # args.folder = r'D:\mojmas\files\Projects\Holo_contour\data\data2'
    args.model = "vit_l"
    args.threshold = 95
    # args.threshold = 70

    run_sam_on_folder(args.folder, args.model, args.threshold)
