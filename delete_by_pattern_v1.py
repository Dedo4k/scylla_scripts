"""

Description:

    Deletes files according to the pattern.
    1 - save
    0 - delete

Parameters:

    -f (--folder): path to your folder
    -p (--pattern): delete pattern

Usage:

    python delete_by_pattern_v1.py   [-f | --folder] 'your_folder_name'
                                     [-p | --pattern] 'pattern'


Version:

        1.1

"""


import os
import argparse
import inspect


def main(directory, pattern):
    counter = 0
    if pattern is None:
        return

    for root, dirs, files in os.walk(directory):
        for file in files:
            if counter == len(pattern):
                counter = 0

            counter += 1

            if pattern[counter - 1] == '1':
                continue
            elif pattern[counter - 1] == '0':
                file_to_remove = os.path.join(root, file)
                os.remove(file_to_remove)
                print('File ' + file_to_remove + ' was removed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-p', '--pattern', dest='pattern', nargs='?', default=110)
    main(parser.parse_args().folder, parser.parse_args().pattern)
    input('Press ENTER...')
