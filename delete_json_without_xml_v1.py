"""

Description:

    Deletes all json files without same xml files.

Parameters:

    -f (--folder): path to your folder

Usage:

    python delete_json_without_xml_v1.py [-f | --folder] 'your_folder_name'

Version:

        1.1

"""

import os
import argparse
import inspect
import re


def main(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json') and not files.__contains__(re.sub(r'.json', '', file) + '.xml'):
                os.remove(os.path.join(root, file))
                print('File ' + os.path.join(root, file) + ' is removed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
