# seam carve algorithm and code from Karthik Karanth's blog:
# https://karthikkaranth.me/blog/implementing-seam-carving-with-python/

import numba
from tqdm import trange
import numpy as np
from imageio import imread, imwrite
from scipy.ndimage.filters import convolve
from math import floor
import os
import warnings
warnings.filterwarnings('ignore')

def calc_energy(img):
    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    # This converts it from a 2D filter to a 3D filter, replicating the same
    # filter for each channel: R, G, B
    filter_du = np.stack([filter_du] * 3, axis=2)

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    # This converts it from a 2D filter to a 3D filter, replicating the same
    # filter for each channel: R, G, B
    filter_dv = np.stack([filter_dv] * 3, axis=2)

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    # We sum the energies in the red, green, and blue channels
    energy_map = convolved.sum(axis=2)

    return energy_map

@numba.jit
def minimum_seam(img):
    r, c, _ = img.shape
    energy_map = calc_energy(img)

    M = energy_map.copy()
    backtrack = np.zeros_like(M, dtype=np.int)

    for i in range(1, r):
        for j in range(0, c):
            # Handle the left edge of the image, to ensure we don't index -1
            if j == 0:
                idx = np.argmin(M[i - 1, j:j + 2])
                backtrack[i, j] = idx + j
                min_energy = M[i - 1, idx + j]
            else:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]

            M[i, j] += min_energy

    return M, backtrack

@numba.jit
def carve_column(img):
    r, c, _ = img.shape

    M, backtrack = minimum_seam(img)

    # Create a (r, c) matrix filled with the value True
    # We'll be removing all pixels from the image which
    # have False later
    mask = np.ones((r, c), dtype=np.bool)

    # Find the position of the smallest element in the
    # last row of M
    j = np.argmin(M[-1])

    for i in reversed(range(r)):
        # Mark the pixels for deletion
        mask[i, j] = False
        j = backtrack[i, j]

    # Since the image has 3 channels, we convert our
    # mask to 3D
    mask = np.stack([mask] * 3, axis=2)

    # Delete all the pixels marked False in the mask,
    # and resize it to the new image dimensions
    img = img[mask].reshape((r, c - 1, 3))

    return img

def crop_c(img, scale_c):
    r, c, _ = img.shape
    new_c = int(scale_c * c)

    for i in trange(c - new_c): # use range if you don't want to use tqdm
        img = carve_column(img)

    return img

def crop_r(img, scale_r):
    img = np.rot90(img, 1, (0, 1))
    img = crop_c(img, scale_r)
    img = np.rot90(img, 3, (0, 1))
    return img

def seam_carve(original_img_name, scale_r, scale_c):
    print("DEBUG: original_img_name:", original_img_name, flush=True)
    img_title, file_extension = original_img_name.split('.')
    carved_img_name = img_title + "_carved." + file_extension
    APP_ROOT = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    image_path = APP_ROOT + "/static/uploaded_images"
    print("DEBUG: image_path:", image_path, flush=True)

    img = imread(image_path + '/' + original_img_name)

    rounded_scale_c = floor(float(scale_c) * 10000) / 10000.0
    rounded_scale_r = floor(float(scale_r) * 10000) / 10000.0

    print("DEBUG: rounded scale_r: ", float(rounded_scale_r), flush=True)
    print("DEBUG: rounded scale_c: ", float(rounded_scale_c), flush=True)
    print("DEBUG: seam carving...", flush=True)
    out = crop_c(img, rounded_scale_c)
    out = crop_r(out, rounded_scale_r)
    print("DEBUG: carving done. carved_img_name:", carved_img_name, flush=True)
    imwrite(image_path + '/' + carved_img_name, out)
