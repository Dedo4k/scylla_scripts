from skimage.metrics import structural_similarity
from skimage.transform import resize
import cv2
import os
import argparse
import inspect
import shutil
import tqdm
import queue
from collections import deque


def copy_to_folder(file, root, index):
    dir_name = os.path.join(root, 'similar', index)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    shutil.copy(file, dir_name)
    print('File ' + file + ' copied to ' + dir_name)


# Works well with images of different dimensions
def orb_sim(img1, img2):
    # SIFT is no longer available in cv2 so using ORB
    try:
        orb = cv2.ORB_create()

        # detect keypoints and descriptors
        kp_a, desc_a = orb.detectAndCompute(img1, None)
        kp_b, desc_b = orb.detectAndCompute(img2, None)

        # define the bruteforce matcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # perform matches.
        matches = bf.match(desc_a, desc_b)
        # Look for similar regions with distance < 50. Goes from 0 to 100 so pick a number between.
        similar_regions = [i for i in matches if i.distance < 50]
        if len(matches) == 0:
            return 0
        elif len(similar_regions) == 1 and len(matches) == 1:
            return 0
        return len(similar_regions) / len(matches)
    except cv2.error:
        print('cv2 error occurred.')
        return 0


# Needs images to be same dimensions
def structural_sim(img1, img2):
    sim, diff = structural_similarity(img1, img2, full=True, multichannel=True)
    return sim


def check_sim(img1, img2):
    image1 = cv2.imread(img1)
    image2 = cv2.imread(img2)
    image3 = resize(image2, (image1.shape[0], image1.shape[1]), anti_aliasing=True, preserve_range=True)
    sim = structural_sim(image1, image3)
    return sim


# def check_sim(img1, img2):
#     img3 = resize(img2, (img1.shape[0], img1.shape[1]), anti_aliasing=True, preserve_range=True)
#     sim = structural_sim(img1, img3)
#     return sim


# def main(directory, coverage):
#     roots = []
#     images = []
#     for root, dirs, files in os.walk(directory):
#         roots.append(root)
#         for file in files:
#             if file.endswith('.jpg') or file.endswith('.jpeg'):
#                 file_path = os.path.join(root, file)
#                 images.append(file_path)
#                 # images.append([file_path, cv2.imread(file_path)])
#
#     checked = []
#     for image in tqdm.tqdm(images):
#         checked.append(image)
#         for c_image in [item for item in images if item not in checked]:
#             sim = check_sim(image, c_image)
#             if sim >= coverage:
#                 print()
#                 print(image, c_image)
#                 copy_to_folder(c_image, roots[0])
#                 print('SIM:', sim)


def main(directory, coverage):
    all_files = deque()
    roots = []
    for root, dirs, files in os.walk(directory):
        roots.append(root)
        for file in files:
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                file_path = os.path.join(root, file)
                all_files.append(file_path)
                # all_files.append([file_path, cv2.imread(file_path)])
    index = 0
    with tqdm.tqdm(total=len(all_files)) as p_bar:
        while len(all_files) != 0:
            file = all_files.pop()
            p_bar.update(1)
            c_files = all_files.copy()
            while len(c_files) != 0:
                c_file = c_files.pop()
                ssim = check_sim(file, c_file)
                if ssim >= coverage:
                    print()
                    print(file, c_file)
                    copy_to_folder(file, roots[0], index)
                    index += 1
                    print('SSIM:', ssim)
                    break

    # with tqdm.tqdm(total=len(all_files)) as p_bar:
    #     while len(all_files) != 0:
    #         file = all_files.pop()
    #         p_bar.update(1)
    #         c_files = all_files.copy()
    #         while len(c_files) != 0:
    #             c_file = c_files.pop()
    #             ssim = check_sim(file[1], c_file[1])
    #             if ssim >= coverage:
    #                 print()
    #                 print(file[0], c_file[0])
    #                 copy_to_folder(file[0], roots[0])
    #                 print('SSIM:', ssim)
    #                 break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-c', '--coverage', dest='coverage', nargs='?', default=0.8)
    main(parser.parse_args().folder, float(parser.parse_args().coverage))
    input('Press ENTER...')
