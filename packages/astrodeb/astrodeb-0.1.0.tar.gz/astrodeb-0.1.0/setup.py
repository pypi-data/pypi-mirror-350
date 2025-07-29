# setup.py

from setuptools import setup, find_packages

setup(
    name="astrodeb",
    version="0.1.0",
    description="Deblur astronomical images using Richardson-Lucy deconvolution and wavelet denoising.",
    author="Atharva",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/astrodeb",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "Pillow",
        "scikit-image",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
