from skimage.io import imread, imsave
import numpy as np

def read_image(path, is_gray=False):
    image = imread(path, as_gray=is_gray)

    if image is None:
        raise FileNotFoundError(f"Image not found at path: {path}")

    if np.issubdtype(image.dtype, np.integer):
        image = image / 255.0

    return image

def save_image(image, path):
    if np.issubdtype(image.dtype, np.floating):
        image = np.clip(image, 0, 1)
        image = (image * 255).astype(np.uint8)

    image = np.squeeze(image)

    imsave(path, image)