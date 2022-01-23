
"""

Description:

    Makes crops of image and puts them into 'crops' folder by object name.

Parameters:

    -f (--folder): path to your folder

Usage:

    python object_cropper_v1.py [-f | --folder] 'your_folder_name'

Version:

        1.1 (.jpg, .jpeg, .png extensions only)

"""

import argparse
import inspect
import os
import re
import shutil
import xml.etree.ElementTree as ET
from PIL import Image


def crop_object_by_cords(img, root, cords, index, object_name):
    crop_image = Image.open(img).crop((int(cords['xmin']), int(cords['ymin']), int(cords['xmax']), int(cords['ymax'])))
    lt = img.split('.', 2)
    dir_path = os.path.join(root, 'crops', object_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    c_file = lt[0] + '_crop_' + str(index) + '.' + lt[1]
    crop_image.save(os.path.join(dir_path, c_file))
    shutil.copy(c_file, dir_path)
    os.remove(c_file)


def crop_objects_from_file(xml_file, root):
    img_extensions = ['.jpg', '.jpeg', '.png']
    index = 0
    try:
        tree = ET.parse(xml_file)
        tree_root = tree.getroot()

        for elm in tree_root.findall('./object'):
            object_name = elm.find('./name').text
            bndbox = elm.find('./bndbox')
            file = re.sub(r'.xml', '', xml_file)
            index += 1
            for extension in img_extensions:
                try:
                    img = file + extension
                    crop_object_by_cords(img, root,
                                         {bndbox.find('./xmin').tag: bndbox.find('./xmin').text,
                                          bndbox.find('./ymin').tag: bndbox.find('./ymin').text,
                                          bndbox.find('./xmax').tag: bndbox.find('./xmax').text,
                                          bndbox.find('./ymax').tag: bndbox.find('./ymax').text}, index, object_name)
                    print('File ' + xml_file + ' ' + str(index) + ' crop(s).')
                except FileNotFoundError:
                    print(end='')
                except Exception:
                    print(end='')

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)


def main(directory):
    xml_files = []
    roots = []
    for root, dirs, files in os.walk(directory):
        roots.append(root)
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))

    for file in xml_files:
        crop_objects_from_file(file, roots[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
