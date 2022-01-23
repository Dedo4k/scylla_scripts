"""

Description:

    Deletes all files if they are same:
        - If there are more or equal matches than mismatches

Parameters:

    -f (--folder): path to your folder
    -c (--coverage): crop coverage

Usage:

    python image_similarity_check_v3.py [-f | --folder] 'your_folder_name'
                                        [-c | --coverage] 'coverage'

Version:

    1.1 (.xml extension only)

"""

import os
import argparse
import inspect
import cv2
import re
import tqdm
import shutil
import lxml
import lxml.etree as ET
from collections import deque
from skimage.transform import resize
from skimage.metrics import structural_similarity


def process_xml_file(xml_file):
    cords = []
    try:
        tree = ET.parse(xml_file)
        tree_root = tree.getroot()

        for elm in tree_root.findall('.//bndbox'):
            cords.append({elm.find('./xmin').tag: elm.find('./xmin').text,
                          elm.find('./ymin').tag: elm.find('./ymin').text,
                          elm.find('./xmax').tag: elm.find('./xmax').text,
                          elm.find('./ymax').tag: elm.find('./ymax').text})

    except lxml.etree.Error:
        print('XML error occurred. File ' + xml_file)
    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)

    return cords


def get_crops_by_cords(xml_file, cords):
    crops = []
    extensions = ['.jpg', '.jpeg', '.png']

    image = None
    for ext in extensions:
        try:
            image = cv2.imread(xml_file.replace(r'.xml', ext))
            if image is not None:
                break
        except FileNotFoundError:
            print()

    for cord in cords:
        crops.append(image[int(cord['ymin']):int(cord['ymax']), int(cord['xmin']):int(cord['xmax'])])

    return crops


def check_crops(first_crop, second_crop, coverage):
    sim = check_sim(first_crop, second_crop)
    if sim >= coverage:
        return True
    else:
        return False


def structural_sim(img1, img2):
    sim, diff = structural_similarity(img1, img2, full=True, multichannel=True)
    return sim


def check_sim(img1, img2):
    img3 = resize(img2, (img1.shape[0], img1.shape[1]), anti_aliasing=True, preserve_range=True)
    sim = structural_sim(img1, img3)
    return sim


def delete_from_folder(file):
    file_types = ['.xml', '.json', '.jpg', '.jpeg', '.png']

    file_name = re.sub(r'.xml', '', file)
    for extension in file_types:
        try:
            d_file = file_name + extension
            os.remove(d_file)
            print('File ' + d_file + ' was removed.')
        except FileNotFoundError:
            print(end='')
        except Exception:
            print('Unknown exception occurred. File ' + file)


def copy_to_folder(file, root, index):
    file_types = ['.xml', '.json', '.jpg', '.jpeg', '.png']
    dir_path = os.path.join(root, 'same', str(index))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file = re.sub(r'.xml', '', file)
    for extension in file_types:
        try:
            c_file = file + extension
            shutil.copy(c_file, dir_path)
            print('File ' + c_file + ' copied to ' + dir_path)
        except FileNotFoundError:
            print(end='')
        except shutil.Error:
            print('File ' + file + ' already exists.')


def main(directory, coverage):
    first_file_name = None
    first_crop = None
    roots = []
    index = 0

    for root, dirs, files in os.walk(directory):
        roots.append(root)
        for file in tqdm.tqdm(files):
            if file.endswith('.jpg'):
                image_file = os.path.join(root, file)

                if first_crop is None:
                    first_file_name = image_file
                    first_crop = cv2.imread(image_file)
                    continue

                second_crop = cv2.imread(image_file)

                if check_crops(first_crop, second_crop, coverage):
                    # delete_from_folder(xml_file)
                    copy_to_folder(first_file_name, roots[0], index)
                    copy_to_folder(image_file, roots[0], index)
                    index += 1
                else:
                    first_file_name = image_file
                    first_crop = second_crop


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-c', '--coverage', dest='coverage', nargs='?', default=0.9)
    main(parser.parse_args().folder, float(parser.parse_args().coverage))
    input('Press ENTER...')
