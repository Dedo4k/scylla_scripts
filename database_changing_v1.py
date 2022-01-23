"""

Description:

        Changes database to new one.

Parameters:

        -f (--folder): path to your folder
        -nn (--new_name): new name to which old one should be changed

Usage:

        python database_changing_v1.py [-f | --folder] 'your_folder_name'
                                   [-nn | --new_name] 'new_name'

Version:

        1.1 (.xml extension only)

"""


import os
import argparse
import inspect
import xml.etree.ElementTree as ET


def change_database(xml_file, new_name):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for elm in root.findall('.//database'):
            elm.text = new_name
            tree.write(xml_file)
            print(
                new_name + ' was set as database in file ' + xml_file)
    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)


def main(directory, new_name):
    xml_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))

    for xml_file in xml_files:
        change_database(xml_file, new_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-nn', '--new_name', dest='new_name', default='new_name')
    main(parser.parse_args().folder, parser.parse_args().new_name)
    input('Press ENTER...')
