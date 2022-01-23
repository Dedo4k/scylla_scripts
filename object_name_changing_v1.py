"""

Description:

    Changes old object names to new ones

Parameters:

    -f (--folder): path to your folder
    -on (--old_name): old object name which must be changed
    -nn (--new_name): new name to which old one should be changed

Usage:

    python object_name_changing_v1.py [-f | --folder] 'your_folder_name'
                                      [-on | --old_name] 'old_name'
                                      [-nn | --new_name] 'new_name'

Version:

        1.1 (.xml extension only)

"""


import os
import argparse
import inspect
import xml.etree.ElementTree as ET


def change_object_name(xml_file, old_name, new_name):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for elm in root.findall('./object/name'):
            if elm.text == old_name:
                elm.text = new_name
                tree.write(xml_file)
                print(
                    'Object name \'' + old_name + '\' in file ' + xml_file + ' replaced with ' +
                    '\'' + new_name + '\'')
    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)


def main(directory, old_name, new_name):
    xml_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))

    for xml_file in xml_files:
        change_object_name(xml_file, old_name, new_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-on', '--old_name', dest='old_name', nargs='?',
                        default='old_name')
    parser.add_argument('-nn', '--new_name', dest='new_name', nargs='?',
                        default='new_name')
    main(parser.parse_args().folder, parser.parse_args().old_name, parser.parse_args().new_name)
    input('Press ENTER...')
