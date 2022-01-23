"""

Description:

    Counts number of objects in all xml files in your folder

Parameters:

    -f (--folder): path to your folder

Usage:

    python object_counter_v1.py [-f | --folder] 'your_folder_name'

"""

import os
import argparse
import inspect
import xml.etree.ElementTree as ET


def check_file(xml_file):
    print()


def main(directory):
    xml_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))

    for xml_file in xml_files:
        check_file(xml_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
