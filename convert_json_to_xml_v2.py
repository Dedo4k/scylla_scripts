"""

Description:

    Converts json file with image into xml.

Parameters:

    -f (--folder): path to your folder

Usage:

    python convert_json_to_xml_v2.py [-f | --folder] 'your_folder_name'

Version:

        1.1 (.jpg only)
        1.2 (added .jpeg and .png extensions)

"""

import os
import argparse
import inspect
import json
import cv2
try:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                import cElementTree as etree
            except ImportError:
                try:
                    import elementtree.ElementTree as etree
                except ImportError:
                    print("Failed to import ElementTree from any known place")
from xml.etree.ElementTree import ElementTree


def get_cords(json_file):
    cords = []
    with open(json_file) as f:
        data = json.load(f)
    for elm in data['objects']:
        cords.append([elm['x'], elm['y'], elm['width'], elm['height']])
    return cords


def convert_json_to_xml(json_file, root):
    img = os.path.join(root, json_file.replace('.json', '.jpg'))
    ex = '.jpg'
    if not os.path.exists(img):
        img = os.path.join(root, json_file.replace('.json', '.jpeg'))
        ex = '.jpeg'
        if not os.path.exists(img):
            img = os.path.join(root, json_file.replace('.json', '.png'))
            ex = '.png'
            return

    image = cv2.imread(img)
    img_height, img_width, img_channels = image.shape

    with open(os.path.join(root, json_file)) as f:
        data = json.load(f)

    tree_root = etree.Element('annotation')

    folder = etree.SubElement(tree_root, 'folder')
    folder.text = os.path.basename(root)

    filename = etree.SubElement(tree_root, 'filename')
    filename.text = data['_id'] + ex

    file_path = etree.SubElement(tree_root, 'path')
    file_path.text = img

    source = etree.SubElement(tree_root, 'source')
    database = etree.SubElement(source, 'database')
    database.text = 'Unknown'

    size = etree.SubElement(tree_root, 'size')
    width = etree.SubElement(size, 'width')
    width.text = str(img_width)
    height = etree.SubElement(size, 'height')
    height.text = str(img_height)
    depth = etree.SubElement(size, 'depth')
    depth.text = str(img_channels)

    segmented = etree.SubElement(tree_root, 'segmented')
    segmented.text = str(0)

    cords = get_cords(os.path.join(root, json_file))
    for elm, elm_cords in zip(data['objects'], cords):
        obj = etree.SubElement(tree_root, 'object')
        name = etree.SubElement(obj, 'name')
        name.text = elm['label']
        pose = etree.SubElement(obj, 'pose')
        pose.text = 'Unspecified'
        truncated = etree.SubElement(obj, 'truncated')
        truncated.text = str(0)
        difficult = etree.SubElement(obj, 'difficult')
        difficult.text = str(0)
        bndbox = etree.SubElement(obj, 'bndbox')
        xmin = etree.SubElement(bndbox, 'xmin')
        xmin.text = str(int(elm_cords[0] * img_width))
        ymin = etree.SubElement(bndbox, 'ymin')
        ymin.text = str(int(elm_cords[1] * img_height))
        xmax = etree.SubElement(bndbox, 'xmax')
        xmax.text = str(int((elm_cords[0] + elm_cords[2]) * img_width))
        ymax = etree.SubElement(bndbox, 'ymax')
        ymax.text = str(int((elm_cords[1] + elm_cords[3]) * img_height))

    etree.indent(tree_root, space='\t')

    new_file = os.path.join(root, json_file).replace('.json', '.xml')
    ElementTree(tree_root).write(new_file)
    print('File ' + new_file + ' was created.')


def main(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                convert_json_to_xml(file, root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
