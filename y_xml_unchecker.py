import os
import inspect
import argparse
try:
    from lxml import etree
except ImportError:
    print(end='')


def xml_uncheck(xml_file):
    try:
        tree = etree.parse(xml_file)
        tree_root = tree.getroot()

        tree_root.attrib.pop('verified', None)

        etree.indent(tree_root, space='\t')

        tree.write(xml_file)

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred.')


def main(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xml'):
                xml_uncheck(os.path.join(root, file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
