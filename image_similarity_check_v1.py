import os
import argparse
import inspect
import cv2
import numpy as np
import shutil
from skimage.metrics import structural_similarity
from skimage.transform import resize
import tqdm

orb = cv2.ORB_create()


def copy_to_folder(file, root, index):
    dir_name = os.path.join(root, 'similar', str(index))
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    shutil.copy(file, dir_name)
    print('File ' + file + ' copied to ' + dir_name)


def move_to_folder(file, root, index):
    dir_name = os.path.join(root, 'similar', str(index))
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    shutil.move(file, dir_name)
    print('File ' + file + ' moved to ' + dir_name)


def count_similarity(img1, img2, region_distance):
    try:
        image1 = cv2.imread(img1)
        image2 = cv2.imread(img2)

        kp_a, desc_a = orb.detectAndCompute(image1, None)
        kp_b, desc_b = orb.detectAndCompute(image2, None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        matches = bf.match(desc_a, desc_b)

        similar_regions = [i for i in matches if i.distance < region_distance]
        if len(matches) == 0:
            return 0
        else:
            return len(similar_regions) / len(matches) * 100
    except cv2.error:
        print('cv2 error occurred. Files ' + img1 + ' ' + img2)
        return 0
    except FileNotFoundError:
        print('File not found. Files ' + img1 + ' ' + img2)
        return 0
    except Exception:
        print('Unknown exception occurred. Files ' + img1 + ' ' + img2)
        return 0


def structural_sim(img1, img2):
    image1 = cv2.imread(img1)
    image2 = cv2.imread(img2)
    image3 = resize(image2, (image1.shape()[0], image1.shape()[1]), anti_aliasing=True, preserve_range=True)
    sim, diff = structural_similarity(image1, image3, full=True)
    return sim


def main(directory, coverage, distance):
    all_files = []
    roots = []
    for root, dirs, files in os.walk(directory):
        roots.append(root)
        for file in files:
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                all_files.append(os.path.join(root, file))

    index = 0
    compared_files = []
    for file in tqdm.tqdm(all_files):
        compared_files.append(file)
        for c_file in all_files:
            if file != c_file and not compared_files.__contains__(c_file):
                file_image = file
                c_file_image = c_file
                similarity = count_similarity(file_image,
                                              c_file_image,
                                              distance)
                if similarity == 100:
                    similarity = structural_sim(file_image, c_file_image)

                print(file_image, c_file_image)
                if similarity >= coverage * 100.00:
                    move_to_folder(file_image, roots[0], index)
                    copy_to_folder(c_file_image, roots[0], index)
                    index += 1
                print('Similarity: ', f'{similarity:.{2}f}', '%')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-c', '--coverage', dest='coverage', nargs='?', default=0.95)
    parser.add_argument('-d', '--distance', dest='distance', nargs='?', default=50)
    main(parser.parse_args().folder, float(parser.parse_args().coverage), int(parser.parse_args().distance))
    input('Press ENTER...')
