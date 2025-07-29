
from setuptools import setup, find_packages
from pathlib import Path

# Load README as long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="astrodeb",
    version="0.1.1",  # <- bump the version
    description="Deblur astronomical images using Richardson-Lucy deconvolution and wavelet denoising.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SASA",
    author_email="sasa.flux@gmail.com",
    url="https://github.com/atharvaansingkar/Image-Deblurring",  # Optional
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
