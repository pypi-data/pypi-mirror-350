from skimage.transform import resize
import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

def find_difference(image1, image2):
    if image1.shape != image2.shape:
        print("Shapes diferentes. Redimensionando image2 para o tamanho de image1.")
        image2 = resize(image2, image1.shape[:2], anti_aliasing=True)

    gray_image1 = rgb2gray(image1) if len(image1.shape) == 3 else image1
    gray_image2 = rgb2gray(image2) if len(image2.shape) == 3 else image2

    data_range = gray_image1.max() - gray_image1.min()

    score, difference_image = structural_similarity(
        gray_image1,
        gray_image2,
        full=True,
        data_range=data_range
    )

    print("Similarity of the images:", score)

    normalized_difference_image = (difference_image - np.min(difference_image)) / (
        np.max(difference_image) - np.min(difference_image)
    )

    return normalized_difference_image

def transfer_histogram(image1, image2):
    matched_image = match_histograms(image1, image2)
    return matched_image