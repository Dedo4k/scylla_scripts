import os
import argparse
from glob import glob
try:
    from lxml import etree, Error
except ImportError:
    print(end='')


def insert_ethalon(file, ethalon):
    try:
        f_tree = None
        e_tree = None
        f_tree_root = None
        e_tree_root = None

        try:
            f_tree = etree.parse(file)
            f_tree_root = f_tree.getroot()
        except FileNotFoundError:
            print('File not found:', file)
        except Error:
            print('lxml error occurred. File', file)

        try:
            e_tree = etree.parse(ethalon)
            e_tree_root = e_tree.getroot()
        except FileNotFoundError:
            print('File not found:', ethalon)
        except Error:
            print('lxml error occurred. File', ethalon)

        for elm in e_tree_root.findall('./object'):
            f_tree_root.append(elm)

        f_tree.write(file)

        print('File', file, 'was updated.')

    except Exception:
        print('Unknown exception occurred. Files', file, ethalon)


def main(ethalon, folder):
    for file in [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.xml*'))]:
        insert_ethalon(file, ethalon)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ethalon', dest='ethalon', nargs='?', required=True)
    parser.add_argument('-f', '--folder', dest='folder', nargs='?', required=True)
    main(parser.parse_args().ethalon, parser.parse_args().folder)
    input('Press ENTER...')
