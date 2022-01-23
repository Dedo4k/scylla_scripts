"""

Description:

    Changes different tag values:
        1. Database tag;
        2. Segmented tag;
        3. Name tag;
        4. Pose tag;
        5. Truncated tag;
        6. Difficult tag;


Parameters:

    -f (--folder): path to your folder

Usage:

    python xml_changer_v1.py [-f | --folder] 'your_folder_name'

Version:

        1.1 (.xml only; database, segmented, name, pose, truncated, difficult tags only)

"""


import os
import argparse
import inspect
import xml.etree.ElementTree as ET


menu = 'Choose what you want to change:\n' \
       '[1] database tag\n' \
       '[2] segmented tag\n' \
       '[3] name tag\n' \
       '[4] pose tag\n' \
       '[5] trancated tag\n' \
       '[6] difficult tag\n'


def change_database(directory):
    while True:
        try:
            database = input('Enter new database value: ')
            break
        except ValueError:
            print('Unexpected input. Value must be string.')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                try:
                    xml_file = os.path.join(root, file)
                    tree = ET.parse(xml_file)
                    tree_root = tree.getroot()

                    tree_root.find('.//database').text = database

                    tree.write(xml_file)

                    print('Tag value has been changed in file ' + xml_file)
                except FileNotFoundError:
                    print('File ' + file + ' not found.')
                except Exception:
                    print('Unknown exception occurred.')


def change_segmented(directory):
    while True:
        try:
            segmented = input('Enter new segmented value: ')
            break
        except ValueError:
            print('Unexpected input. Value must be string.')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                try:
                    xml_file = os.path.join(root, file)
                    tree = ET.parse(xml_file)
                    tree_root = tree.getroot()

                    tree_root.find('./segmented').text = segmented

                    tree.write(xml_file)

                    print('Tag value has been changed in file ' + xml_file)
                except FileNotFoundError:
                    print('File ' + file + ' not found.')
                except Exception:
                    print('Unknown exception occurred.')


def change_name(directory):
    while True:
        try:
            old = input('Enter old object value: ')
            break
        except ValueError:
            print('Unexpected input. Value must be string.')

    while True:
        try:
            new = input('Enter new object value: ')
            break
        except ValueError:
            print('Unexpected input. Value must be string.')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                try:
                    xml_file = os.path.join(root, file)
                    tree = ET.parse(xml_file)
                    tree_root = tree.getroot()

                    for elm in tree_root.findall('.//name'):
                        if elm.text == old:
                            elm.text = new
                            print('Tag value has been changed in file ' + xml_file)

                    tree.write(xml_file)

                except FileNotFoundError:
                    print('File ' + file + ' not found.')
                except Exception:
                    print('Unknown exception occurred.')


def change_pose(directory):
    while True:
        try:
            pose = input('Enter new pose value: ')
            break
        except ValueError:
            print('Unexpected input. Value must be string.')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                try:
                    xml_file = os.path.join(root, file)
                    tree = ET.parse(xml_file)
                    tree_root = tree.getroot()

                    for elm in tree_root.findall('.//pose'):
                        elm.text = pose
                        print('Tag value has been changed in file ' + xml_file)

                    tree.write(xml_file)

                except FileNotFoundError:
                    print('File ' + file + ' not found.')
                except Exception:
                    print('Unknown exception occurred.')


def change_trancated(directory):
    while True:
        try:
            truncated = input('Enter new truncated value: ')
            break
        except ValueError:
            print('Unexpected input. Value must be string.')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                try:
                    xml_file = os.path.join(root, file)
                    tree = ET.parse(xml_file)
                    tree_root = tree.getroot()

                    for elm in tree_root.findall('.//truncated'):
                        elm.text = truncated
                        print('Tag value has been changed in file ' + xml_file)

                    tree.write(xml_file)

                except FileNotFoundError:
                    print('File ' + file + ' not found.')
                except Exception:
                    print('Unknown exception occurred.')


def change_difficult(directory):
    while True:
        try:
            difficult = input('Enter new difficult value: ')
            break
        except ValueError:
            print('Unexpected input. Value must be string.')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                try:
                    xml_file = os.path.join(root, file)
                    tree = ET.parse(xml_file)
                    tree_root = tree.getroot()

                    for elm in tree_root.findall('.//difficult'):
                        elm.text = difficult
                        print('Tag value has been changed in file ' + xml_file)

                    tree.write(xml_file)

                except FileNotFoundError:
                    print('File ' + file + ' not found.')
                except Exception:
                    print('Unknown exception occurred.')


def main(directory):
    while True:
        try:
            choice = int(input(menu))
            if choice == 1 or \
                    choice == 2 or \
                    choice == 3 or \
                    choice == 4 or \
                    choice == 5 or \
                    choice == 6:
                break
            else:
                raise ValueError()
        except ValueError:
            print('Unexpected input. Value must be one of the listed [1, 2, 3, 4, 5, 6].')

    if choice == 1:
        change_database(directory)
    elif choice == 2:
        change_segmented(directory)
    elif choice == 3:
        change_name(directory)
    elif choice == 4:
        change_pose(directory)
    elif choice == 5:
        change_trancated(directory)
    elif choice == 6:
        change_difficult(directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
