import os
import fnmatch
import inspect
import argparse
import xml.etree.ElementTree as ET


def get_image(first_xml, second_xml):
    pass


def xml_comparator(first_xml, second_xml):
    first_root = None
    second_root = None

    try:
        try:
            first_tree = ET.parse(first_xml)
            first_root = first_tree.getroot()

        except FileNotFoundError:
            print('File ' + first_xml + ' not found.')

        try:
            second_tree = ET.parse(second_xml)
            second_root = second_tree.getroot()

        except FileNotFoundError:
            print('File ' + second_xml + ' not found.')

        for f_elm in first_root.findall('.//bndbox'):
            for s_elm in second_root.findall('.//bndbox'):
                if f_elm.find('xmin') != s_elm.find('xmin') or \
                        f_elm.find('ymin') != s_elm.find('ymin') or \
                        f_elm.find('xmax') != s_elm.find('xmax') or \
                        f_elm.find('ymax') != s_elm.find('ymax'):
                    get_image(first_xml, second_xml)

    except Exception:
        print('Unknown exception occurred.')


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def main(first_dir, second_dir):
    for root, dirs, files in os.walk(first_dir):
        for file in files:
            if file.endswith('.xml'):
                first_xml = os.path.join(root, file)
                founded = find('*' + file, second_dir)
                if len(founded) == 0:
                    print(file + ' from ' + first_dir + ' doesn\'t exist in ' + second_dir)
                    continue
                else:
                    second_xml = founded[0]
                    xml_comparator(first_xml, second_xml)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d1', '--dir1', dest='first_dir', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-d2', '--dir2', dest='second_dir', nargs='?', required=True,
                        default='Unknown')
    main(parser.parse_args().first_dir, parser.parse_args().second_dir)
    input('Press ENTER...')
