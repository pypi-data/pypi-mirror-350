# astrodeb/deblur.py

import numpy as np
from skimage import restoration, img_as_float, color
from skimage.restoration import denoise_wavelet
from PIL import Image

def gaussian_psf(size=15, sigma=2):
    ax = np.arange(-size // 2 + 1., size // 2 + 1.)
    xx, yy = np.meshgrid(ax, ax)
    psf = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
    return psf / np.sum(psf)

def deblur_image(pil_image, psf_size=15, sigma=2, iterations=30):
    image_np = img_as_float(np.array(pil_image.convert("RGB")))
    gray_image = color.rgb2gray(image_np)

    psf = gaussian_psf(size=psf_size, sigma=sigma)
    deconvolved = restoration.richardson_lucy(gray_image, psf, num_iter=iterations)
    final_output = denoise_wavelet(deconvolved, method='BayesShrink', mode='soft', rescale_sigma=True)

    return Image.fromarray((final_output * 255).astype(np.uint8))
