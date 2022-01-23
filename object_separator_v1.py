"""

Description:

    Distributes all files into folders depending on what objects are in the files

Parameters:

    -f (--folder): path to your folder

Usage:

    python object_separator_v1.py [-f | --folder] 'your_folder_name'

Version:

        1.1 (.xml, .json, .jpg, .jpeg, .png extensions only)

"""


import os
import argparse
import inspect
import re
import shutil
import xml.etree.ElementTree as ET


def copy_file_to_folder_by_name(xml_file, root, name):
    file_types = ['.xml', '.json', '.jpg', '.jpeg', '.png']
    dir_path = os.path.join(root, os.path.join('objects', name))
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


def transfer_file_to_folder_by_name(xml_file, root):
    objects = []
    try:
        tree = ET.parse(xml_file)
        tree_root = tree.getroot()

        for elm in tree_root.findall('./object/name'):
            if not objects.__contains__(elm.text):
                objects.append(elm.text)
                copy_file_to_folder_by_name(xml_file, root, elm.text)

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
        transfer_file_to_folder_by_name(file, roots[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
