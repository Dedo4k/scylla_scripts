"""

Description:

    Searches for files where the object area is less than the specified
    and puts them in './small' folder.
    If file has one object which area is > specified and < 0.1, puts it in './mixed' folder

Parameters:

    -f (--folder): path to your folder
    -o (--object_name): object name which must be checked
    -s (--scope): the area of the object must be smaller than this value relative to the image

Usage:

    python object_frame_separator_v2.py [-f | --folder] 'your_folder_name'
                                        [-o | --object_name] 'object_name'
                                        [-n | --scope] 'scope'

Version:

        1.1 (.xml, .json, .jpg, .jpeg, .png extensions only)
        1.2 (added 'any' object_name, checks all objects)

"""

import os
import argparse
import inspect
import re
import shutil
import xml.etree.ElementTree as ET


def copy_file_to_folder_by_name(xml_file, root, new_folder, name):
    file_types = ['.xml', '.json', '.jpg', '.jpeg', '.png']
    dir_path = os.path.join(root, os.path.join(new_folder, name))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file = re.sub(r'.xml', '', xml_file)
    for extension in file_types:
        try:
            c_file = file + extension
            shutil.copy(c_file, dir_path)
            print('File ' + c_file + ' copied to ' + dir_path)
        except FileNotFoundError:
            print(end='')
        except shutil.Error:
            print('File ' + xml_file + ' already exists.')


def count_area(frame_cords):
    return abs(
        (int(frame_cords['xmax']) - int(frame_cords['xmin'])) * (int(frame_cords['ymax']) - int(frame_cords['ymin'])))


def check_object_frames_and_separate(xml_file, root, object_name, scope):
    pas = 0
    not_pas = 0
    try:
        tree = ET.parse(xml_file)
        tree_root = tree.getroot()

        for elm in tree_root.findall('./object'):
            if elm.find('./name').text == object_name or object_name == 'any':
                bndbox = elm.find('./bndbox')
                area = count_area({bndbox.find('./xmin').tag: bndbox.find('./xmin').text,
                                   bndbox.find('./ymin').tag: bndbox.find('./ymin').text,
                                   bndbox.find('./xmax').tag: bndbox.find('./xmax').text,
                                   bndbox.find('./ymax').tag: bndbox.find('./ymax').text})
                print('Area: ', area, xml_file)
                if area < float(scope) * 1920 * 1080:
                    pas += 1
                elif float(scope) * 1920 * 1080 <= area < 0.1 * 1920 * 1080:
                    not_pas += 1

        if pas != 0 and not_pas == 0:
            copy_file_to_folder_by_name(xml_file, root, 'small', object_name)
        elif pas != 0 and not_pas == 1:
            copy_file_to_folder_by_name(xml_file, root, 'mixed', object_name)

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)


def main(directory, object_name, scope):
    xml_files = []
    roots = []

    for root, dirs, files in os.walk(directory):
        roots.append(root)
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))

    for xml_file in xml_files:
        check_object_frames_and_separate(xml_file, roots[0], object_name, scope)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-o', '--object_name', dest='object_name', nargs='?',
                        default='any')
    parser.add_argument('-s', '--scope', dest='scope', nargs='?',
                        default='0.02')
    main(parser.parse_args().folder, parser.parse_args().object_name, parser.parse_args().scope)
    input('Press ENTER...')
