from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pixflow",
    version="0.1.1",
    author="Alessandra Chioquetta",
    description="A simple image processing toolkit for resizing, histogram transfer, and difference detection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/A-Chioquetta/pixflow",  # Altere se quiser
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "scikit-image>=0.16.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
