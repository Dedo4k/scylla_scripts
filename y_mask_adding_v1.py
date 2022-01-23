import os
import argparse
import cv2
import numpy as np
from glob import glob
from tqdm import tqdm
from skimage.util import random_noise


def apply_mask(file, mask_file):
    mask = None
    image = None
    f_name, ext = os.path.splitext(file)

    try:
        mask = cv2.imread(mask_file, cv2.IMREAD_GRAYSCALE)
    except Exception:
        print('Could not open the mask.', mask_file)

    try:
        image = cv2.imread(file)
    except Exception:
        print('Could not open the image.', file)

    mask = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA)

    noise = np.random.randint(0, 100, (image.shape[0], image.shape[1], 3), dtype='uint8')

    masked = cv2.bitwise_not(noise, image, mask=mask)

    cv2.imwrite(f_name + '_masked' + ext, masked)


def main(mask_file, folder):
    files = []
    extensions = ['.jpg', '.jpeg', '.png']
    for ext in extensions:
        files.extend([y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*') + ext) if y != mask_file])

    for file in tqdm(files):
        apply_mask(file, mask_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mask', dest='mask', nargs='?', required=True)
    parser.add_argument('-f', '--folder', dest='folder', nargs='?', required=True)
    main(parser.parse_args().mask, parser.parse_args().folder)
    input('Press ENTER...')
