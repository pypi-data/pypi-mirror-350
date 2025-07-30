# PixFlow: Image Processing Toolkit

[![PyPI version](https://img.shields.io/pypi/v/pixflow.svg)](https://pypi.org/project/pixflow/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Simple, lightweight, and easy-to-use image processing toolkit in Python.  
Resize images, transfer histograms, and detect structural differences with just a few lines of code.

---

## 🖼️ Description

**PixFlow** is a Python package designed to simplify common image processing tasks, including:

- Image resizing
- Histogram matching between images
- Structural difference detection (SSIM)
- Image reading and saving
- Plotting images and histograms

Built on top of `scikit-image`, `matplotlib`, and `numpy`.

---

## 📦 Features

- 🔸 **Image reading and saving** — Supports formats like `.jpg`, `.png`, etc.
- 🔸 **Image resizing** — Resizes by relative proportion.
- 🔸 **Histogram matching** — Adjusts the tones of one image to match another.
- 🔸 **Structural difference detection (SSIM)** — Detects and visualizes structural differences between images.
- 🔸 **Plot utilities**:
  - Display single images
  - Compare multiple images side by side
  - Plot RGB histograms

---

## 🚀 Installation

Install from PyPI:

```bash
pip install pixflow
```

Or install locally from the repository:

```bash
git clone https://github.com/A-Chioquetta/pixflow.git
cd pixflow
pip install -e .
```

---

## 🔧 Dependencies

- numpy
- matplotlib
- scikit-image

These will be automatically installed with `pip install pixflow`.  
Or install manually with:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from pixflow import (
    read_image, save_image,
    resize_image, transfer_histogram, find_difference,
    plot_image, plot_result, plot_histogram
)

# Read images
image1 = read_image('flor1.jpg')
image2 = read_image('flor2.jpg')
image3 = read_image('flor1_alterada.jpg')

# Resize
resized = resize_image(image1, proportion=0.5)
plot_image(resized, title="Resized Image")

# Histogram matching
matched = transfer_histogram(image1, image2)
plot_result(image1, image2, matched, title="Histogram Matching")

# Structural difference (SSIM)
difference = find_difference(image1, image3)
plot_result(image1, image3, difference, title="Structural Difference")

# Histogram plot
plot_histogram(image1)

# Save resized image
save_image(resized, 'resized_image.jpg')
```

---

## 🗂️ Project Structure

```
pixflow/
├── pixflow/
│   ├── processing/
│   ├── utils/
│   └── __init__.py
├── examples/
├── tests/
├── README.md
├── setup.py
├── LICENSE.txt
└── requirements.txt
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE.txt).

---

## 🔗 Links

- PyPI: https://pypi.org/project/pixflow/
- GitHub: https://github.com/A-Chioquetta/pixflow