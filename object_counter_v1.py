"""

Description:

    Counts number of objects in all xml files in your folder

Parameters:

    -f (--folder): path to your folder

Usage:

    python object_counter_v1.py [-f | --folder] 'your_folder_name'

Version:

        1.1 (.xml extension only)

"""

import os
import argparse
import inspect
import xml.etree.ElementTree as ET


def count_object(xml_file, dictionary):
    object_counter = 0
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for elm in root.findall('./object/name'):
            object_counter += 1
            if dictionary.__contains__(elm.text):
                dictionary[elm.text] = dictionary[elm.text] + 1
            else:
                dictionary.update({elm.text: 1})

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)
    return object_counter, dictionary


def main(directory):
    xml_files = []
    dictionary = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))

    object_counter = 0
    for file in xml_files:
        counter, dictionary = count_object(file, dictionary)
        object_counter += counter
    print('TOTAL NUMBER OF OBJECTS: ' + str(object_counter))
    for obj in dictionary:
        print(obj + ' objects: ' + str(dictionary[obj]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
