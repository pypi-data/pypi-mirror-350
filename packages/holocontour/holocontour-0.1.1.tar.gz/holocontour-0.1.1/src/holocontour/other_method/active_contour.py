import os
import matplotlib.pyplot as plt
from skimage import io, color, filters, measure
from skimage.segmentation import active_contour
from skimage.draw import polygon2mask
from holocontour.image.structure_forest import generate_mask

# --- Config ---
# data_dir = r'D:\mojmas\files\Projects\Holo_contour\data\data1'
data_dir = r'/data/data2'
output_dir = data_dir + r'\seg'
os.makedirs(output_dir, exist_ok=True)

gaussian_sigma = 1.3


image_files = sorted([f for f in os.listdir(data_dir) if f.endswith(('.png',))])

for i, img_name in enumerate(image_files):
    print(f"[{i}] Processing {img_name}...")

    image_path = os.path.join(data_dir, img_name)
    image = io.imread(image_path)
    image = image[:, :, 0]
    if image.ndim == 3:
        image_gray = color.rgb2gray(image)
    elif image.ndim == 2:

        image_gray = image
    else:
        image_gray = image

    initial_mask = generate_mask(image_gray) > 0

    contours = measure.find_contours(initial_mask.astype(float), 0.5)
    if not contours:
        print(f"  Skipping {img_name} (no contours found).")
        continue
    init_snake = max(contours, key=len)

    image_smooth = filters.gaussian(image_gray, sigma=gaussian_sigma)

    snake = active_contour(
        image_smooth,
        init_snake,
        alpha=0.001,
        beta=1.0,
        gamma=0.001,
    )

    refined_mask = polygon2mask(image.shape[:2], snake)

    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray')
    ax.plot(init_snake[:, 1], init_snake[:, 0], '--r', label='Initial')
    ax.plot(snake[:, 1], snake[:, 0], '-b', label='Refined')
    ax.legend()
    ax.set_title(f"Refined Contour - {img_name}")
    plt.tight_layout()

    # Save figure
    fig_path = os.path.join(output_dir, f"{os.path.splitext(img_name)[0]}_contour.png")
    plt.savefig(fig_path)
    print(f"  Saved figure: {fig_path}")
    plt.show()

    # # --- Optional: Save refined mask as binary image ---
    # mask_path = os.path.join(output_dir, f"{os.path.splitext(img_name)[0]}_refined_mask.png")
    # io.imsave(mask_path, img_as_ubyte(refined_mask))
    # print(f"  Saved refined mask: {mask_path}")


