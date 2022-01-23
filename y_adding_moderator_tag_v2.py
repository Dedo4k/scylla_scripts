"""

Description:

    Add moderator tag if not exists using path tag.


Parameters:

    -f (--folder): path to your folder

Usage:

    python y_adding_moderator_tag_v2.py [-f | --folder] 'your_folder_name'

Version:

        1.1 (.xml only)
        1.2 getting moderator from path

"""


import os
import inspect
import argparse
try:
    from lxml import etree
except ImportError:
    print(end='')


def xml_process(xml_file):
    try:
        tree = etree.parse(xml_file)
        tree_root = tree.getroot()

        if tree_root.find('./moderator') is None:
            moderator = etree.Element('moderator')
            moderator.text = 'Unknown'
            tree_root.insert(3, moderator)

        path = tree_root.find('./path')
        if path.text.__contains__('moderation_'):
            try:
                name = path.text.split('moderation_')[1].split('\\')[0]
                if name == 'vtl':
                    name = 'vitalik'
                tree_root.find('./moderator').text = name
                print('\'moderator\' tag set as ' + name + ' in ' + xml_file)
            except IndexError:
                print('Something with your path tag in ' + xml_file)

        etree.indent(tree_root, space='\t')

        tree.write(xml_file)

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred.')


def main(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                xml_process(os.path.join(root, file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
