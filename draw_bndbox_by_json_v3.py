"""

Description:

    Draws bndboxes using json file and puts them into 'drawn' folder

Parameters:

    -f (--folder): path to your folder

Usage:

    python draw_bndbox_by_json_v3.py [-f | --folder] 'your_folder_name'

Version:

        1.1 (.jpg only and one color)
        1.2 (added .jpeg and .png extensions)
        1.3 (added color depending on the name of the object)

"""

import os
import argparse
import inspect
import json
import cv2


def save_image(image, file_name, root):
    dir_name = os.path.join(root, 'drawn')
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    c_file = dir_name + file_name.split(root)[1]
    cv2.imwrite(c_file, image)
    print('File ' + c_file + ' was created.')


def get_cords(json_file):
    cords = []
    with open(json_file) as f:
        data = json.load(f)
    for elm in data['objects']:
        cords.append([elm['x'], elm['y'], elm['width'], elm['height']])
    return cords


def get_color(json_file):
    color = []
    with open(json_file) as f:
        data = json.load(f)
    for elm in data['objects']:
        object_name = elm['label']
        if object_name == 'person':
            color.append(tuple((0, 255, 0)))
        elif object_name == 'gun':
            color.append(tuple((0, 0, 255)))
        elif object_name == 'rifle':
            color.append(tuple((148, 0, 211)))
        else:
            color.append(tuple((255, 255, 255)))

    return color


def draw_bndbox(json_file, root):
    try:
        cords = get_cords(json_file)
        color = get_color(json_file)

        img = json_file.replace('.json', '.jpg')
        if not os.path.exists(img):
            img = json_file.replace('.json', '.jpeg')
            if not os.path.exists(img):
                img = json_file.replace('.json', '.png')

        image = cv2.imread(img)
        img_height, img_width, img_channels = image.shape
        for elm, elm_color in zip(cords, color):
            cv2.rectangle(image,
                          (int(elm[0] * img_width), int(elm[1] * img_height)),
                          (int((elm[0] + elm[2]) * img_width), int((elm[1] + elm[3]) * img_height)),
                          elm_color,
                          thickness=3)

        save_image(image, img, root)
    except json.JSONDecodeError:
        print('Json decode error occurred. File ' + json_file)
    except FileNotFoundError:
        print('File ' + json_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + json_file)


def main(directory):
    roots = []
    for root, dirs, files in os.walk(directory):
        roots.append(root)
        for file in files:
            if file.endswith('.json'):
                draw_bndbox(os.path.join(root, file), root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
