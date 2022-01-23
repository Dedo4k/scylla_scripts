"""

Description:

    Founds all files with same name as crop at 3 level and puts them into 'mistake' folder.

Parameters:

    -f (--folder): path to your folder

Usage:

    python find_by_crop_v1.py [-f | --folder] 'your_folder_name'

Version:

        1.1

"""


import os
import argparse
import inspect
import shutil


def find_all_files(file):
    extensions = ['.xml', '.json', '.jpg', '.jpeg', '.png']
    first_level = os.path.dirname(file)
    second_level = os.path.dirname(first_level)
    third_level = os.path.dirname(second_level)
    dir_name = os.path.join(third_level, 'mistake')
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    file_name = os.path.basename(file).split('_crop_')[0]
    for ext in extensions:
        try:
            f_file = os.path.join(third_level, file_name) + ext
            shutil.move(f_file, dir_name)
            print('File ' + f_file + ' moved to ' + dir_name)
        except shutil.SameFileError:
            print('File ' + f_file + 'already exists in ' + dir_name)
        except FileNotFoundError:
            print(end='')
        except Exception:
            print(end='')


def main(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                find_all_files(os.path.join(root, file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
