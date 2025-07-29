# astrodeb

**astrodeb** is a lightweight Python package that restores blurred astronomical images using **Richardson–Lucy deconvolution** and **wavelet denoising**. It is ideal for astrophotography, scientific imaging, or any case where your images suffer from Gaussian blur and noise.

---

## ✨ Features

- Richardson–Lucy iterative deconvolution (with configurable PSF)
- Wavelet denoising using BayesShrink soft thresholding
- Works directly with standard `PIL.Image` inputs
- Easy to integrate into scientific or image-processing pipelines

---

## 📦 Installation

You can install it via [PyPI](https://pypi.org/project/astrodeb/):

```bash
pip install astrodeb
