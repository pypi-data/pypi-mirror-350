import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import numpy as np


def plot_segmentation_result(img_org, initial_contour, refined_contours, title="Segmentation Result"):
    """
    Plot the initial and refined contours on the original image,
    and return the plot as a NumPy array (RGB image).
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img_org, cmap='gray')

    if initial_contour is not None:
        ax.plot(initial_contour[:, 1], initial_contour[:, 0], '--r', label='Initial')

    for i, contour in enumerate(refined_contours):
        label = "Refined" if i == 0 else None
        ax.plot(contour[:, 1], contour[:, 0], '-b', linewidth=2, label=label)

    ax.set_title(title)
    ax.legend()
    plt.tight_layout()

    # Save figure to buffer
    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)  # Close the figure to avoid GUI issues

    # Convert buffer to NumPy array
    buf.seek(0)
    image = Image.open(buf).convert('RGB')
    image_np = np.array(image)

    return image_np


