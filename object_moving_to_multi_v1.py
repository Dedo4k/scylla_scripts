"""

Description:

    Counts number of specified objects in xml files
    and if number is more than specified puts them into 'multi' folder

Parameters:

    -f (--folder): path to your folder
    -o (--object): object name to count
    -m (--minimum): minimum number of objects in the file

Usage:

    python object_moving_to_multi_v1.py [-f | --folder] 'your_folder_name'
                                        [-o | --object] 'object_name'
                                        [-m | --minimum] 'minimum_number'

Version:

        1.1 (.xml, .json, .jpg, .jpeg, .png extensions only)

"""

import os
import argparse
import inspect
import re
import shutil
import xml.etree.ElementTree as ET


def move_file_to_folder(xml_file, root, object_name):
    file_types = ['.xml', '.json', '.jpg', '.jpeg', '.png']
    dir_path = os.path.join(root, 'multi', object_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file = re.sub(r'.xml', '', xml_file)
    for extension in file_types:
        try:
            c_file = file + extension
            shutil.copy(c_file, dir_path)
            os.remove(c_file)
            print('File ' + c_file + ' copied to ' + dir_path)
        except FileNotFoundError:
            print(end='')
        except shutil.Error:
            print('File ' + xml_file + ' already exists.')


def object_counter(xml_file, root, object_name, minimum):
    object_counter = 0
    try:
        tree = ET.parse(xml_file)
        tree_root = tree.getroot()

        for elm in tree_root.findall('./object/name'):
            if elm.text == object_name:
                object_counter += 1

        if object_counter > minimum:
            move_file_to_folder(xml_file, root, object_name)

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)


def main(directory, object_name, minimum):
    roots = []
    for root, dirs, files in os.walk(directory):
        roots.append(root)
        for file in files:
            if file.endswith('.xml'):
                object_counter(os.path.join(root, file), roots[0], object_name, int(minimum))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-o', '--object', dest='object', nargs='?', default='person')
    parser.add_argument('-m', '--minimum', dest='minimum', nargs='?', default=5)
    main(parser.parse_args().folder, parser.parse_args().object, parser.parse_args().minimum)
    input('Press ENTER...')
