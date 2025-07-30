import matplotlib.pyplot as plt
import numpy as np

def plot_image(image, title="Image"):
    plt.figure(figsize=(12, 4))
    plt.imshow(np.clip(image, 0, 1), cmap='gray')
    plt.axis('off')
    plt.title(title)
    plt.gcf().canvas.manager.set_window_title(title)
    plt.show()

def plot_result(*args, title="Result"):
    number_images = len(args)
    fig, axis = plt.subplots(nrows=1, ncols=number_images, figsize=(5 * number_images, 4))
    plt.gcf().canvas.manager.set_window_title(title)

    names_lst = ['Image {}'.format(i) for i in range(1, number_images)]
    names_lst.append('Result')

    for ax, name, image in zip(axis, names_lst, args):
        ax.set_title(name)
        ax.imshow(np.clip(image, 0, 1), cmap='gray')
        ax.axis('off')

    fig.tight_layout()
    plt.show()

def plot_histogram(image):
    fig, axis = plt.subplots(nrows=1, ncols=3, figsize=(12, 4), sharex=True, sharey=True)
    color_lst = ['red', 'green', 'blue']
    for index, (ax, color) in enumerate(zip(axis, color_lst)):
        ax.set_title('{} histogram'.format(color.title()))
        ax.hist(image[:, :, index].ravel(), bins=256, color=color, alpha=0.8)
    fig.tight_layout()
    plt.show()