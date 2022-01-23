"""

Description:

    Separate all files by moderator tag into corresponding folders.
    If moderator is unknown or tag doesn't exist makes 'unmoderated' folder into base folder.


Parameters:

    -f (--folder): path to your folder

Usage:

    python y_moderator_separator_v1.py [-f | --folder] 'your_folder_name'

Version:

        1.1 (.jpg, .jpeg, .png, .JPG, .JPEG, .PNG extensions only)

"""


import argparse
import inspect
import os
import shutil
try:
    from lxml import etree
except ImportError:
    print(end='')


def move_files_to_folder(xml_file, folder, root):
    extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    dir_name = os.path.join(root, folder)
    file_name = os.path.basename(xml_file)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    try:
        shutil.move(xml_file, dir_name)
        print('File ' + xml_file + ' moved to ' + dir_name)
    except shutil.Error:
        print(end='')

    for ext in extensions:
        try:
            c_file = xml_file.split('.')[0] + ext
            shutil.move(c_file, dir_name)
            print('File ' + c_file + ' moved to ' + dir_name)
        except FileNotFoundError:
            print(end='')
        except shutil.Error:
            print(end='')


def xml_process(xml_file, root):
    try:
        tree = etree.parse(xml_file)
        tree_root = tree.getroot()

        if tree_root.find('./moderator') is None or tree_root.find('./moderator').text == 'Unknown':
            move_files_to_folder(xml_file, 'unmoderated', root)
        else:
            move_files_to_folder(xml_file, tree_root.find('./moderator').text, root)

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred.')


def main(directory):
    roots = []
    for root, dirs, files in os.walk(directory):
        roots.append(root)
        for file in files:
            if file.endswith('.xml'):
                xml_process(os.path.join(root, file), roots[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
