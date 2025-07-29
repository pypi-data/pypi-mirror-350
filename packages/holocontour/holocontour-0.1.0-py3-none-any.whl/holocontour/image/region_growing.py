import numpy as np


def region_grow(image, seed, max_iter=20000, tolerance=25):
    """Simple region growing algorithm from a seed."""
    mask = np.zeros_like(image, dtype=bool)
    region_mean = image[seed]
    stack = [seed]
    iter_count = 0

    while stack and iter_count < max_iter:
        x, y = stack.pop()
        if not mask[x, y]:
            mask[x, y] = True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < image.shape[0] and
                    0 <= ny < image.shape[1] and
                    not mask[nx, ny] and
                    abs(image[nx, ny] - region_mean) < tolerance
                ):
                    stack.append((nx, ny))
        iter_count += 1

    return mask