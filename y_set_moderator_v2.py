"""

Description:

    Set moderator name by parameter name or name from folder.


Parameters:

    -f (--folder): path to your folder
    -m (--moderator): moderator name

Usage:

    python y_set_moderator_v2.py [-f | --folder] 'your_folder_name'
                                 [-m | --moderator] 'moderator_name'

Version:

        1.1 (.xml only)
        1.2 if tag doesn't exist create it

"""


import os
import inspect
import argparse

try:
    from lxml import etree
except ImportError:
    print(end='')


def set_moderator(xml_file, root, moderator):
    try:
        tree = etree.parse(xml_file)
        tree_root = tree.getroot()

        if tree_root.find('./moderator') is None:
            moderator_tag = etree.Element('moderator')
            moderator_tag.text = 'Unknown'
            tree_root.insert(3, moderator_tag)

        if moderator != 'Unknown':
            tree_root.find('./moderator').text = moderator
            print('\'moderator\' tag set as ' + moderator + ' in ' + xml_file)
        else:
            if root.__contains__('moderation'):
                name = None
                while root.__contains__('moderation'):
                    name = os.path.basename(root)
                    root = os.path.dirname(root)

                name = name.split('_')[1]
                if name == 'vtl':
                    name = 'vitalik'
                tree_root.find('./moderator').text = name
                print('\'moderator\' tag set as ' + name + ' in ' + xml_file)

        etree.indent(tree_root, space='\t')

        tree.write(xml_file)

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred.')


def main(directory, moderator):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                set_moderator(os.path.join(root, file), root, moderator)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-m', '--moderator', dest='moderator', nargs='?',
                        default='Unknown')
    main(parser.parse_args().folder, parser.parse_args().moderator)
    input('Press ENTER...')
