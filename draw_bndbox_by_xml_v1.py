"""

Description:

    Draws bndboxes using xml file and puts them into 'drawn' folder

Parameters:

    -f (--folder): path to your folder

Usage:

    python draw_bndbox_by_json_v3.py [-f | --folder] 'your_folder_name'

Version:

        1.1 (.jpg, .jpeg, .png extensions only. Different colors for different objects)

"""

import os
import argparse
import inspect
import cv2
import xml.etree.ElementTree as ET


def save_image(image, file_name, root):
    dir_name = os.path.join(root, 'drawn')
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    c_file = dir_name + file_name.split(root)[1]
    cv2.imwrite(c_file, image)
    print('File ' + c_file + ' was created.')


def get_cords(xml_file):
    cords = []
    try:
        tree = ET.parse(xml_file)
        tree_root = tree.getroot()

        for elm in tree_root.findall('./object/bndbox'):
            cords.append([int(elm.find('xmin').text), int(elm.find('ymin').text), int(elm.find('xmax').text),
                          int(elm.find('ymax').text)])

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)

    return cords


def get_color(xml_file):
    color = []
    try:
        tree = ET.parse(xml_file)
        tree_root = tree.getroot()

        for elm in tree_root.findall('./object'):
            object_name = elm.find('name').text
            if object_name == 'person':
                color.append(tuple((0, 255, 0)))
            elif object_name == 'gun':
                color.append(tuple((0, 0, 255)))
            elif object_name == 'rifle':
                color.append(tuple((148, 0, 211)))
            else:
                color.append(tuple((255, 255, 255)))

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)

    return color


def draw_bndbox(xml_file, root):
    try:
        cords = get_cords(xml_file)
        color = get_color(xml_file)

        img = xml_file.replace('.xml', '.jpg')
        if not os.path.exists(img):
            img = xml_file.replace('.xml', '.jpeg')
            if not os.path.exists(img):
                img = xml_file.replace('.xml', '.png')

        image = cv2.imread(img)
        for elm, elm_color in zip(cords, color):
            cv2.rectangle(image,
                          (elm[0], elm[1]),
                          (elm[2], elm[3]),
                          elm_color,
                          thickness=3)

        save_image(image, img, root)
    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)


def main(directory):
    roots = []
    for root, dirs, files in os.walk(directory):
        roots.append(root)
        for file in files:
            if file.endswith('.xml'):
                draw_bndbox(os.path.join(root, file), root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
