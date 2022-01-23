import os
import argparse
import inspect
import cv2
import numpy as np
import tqdm

try:
    from lxml import etree
except ImportError:
    print(end='')

img_ext = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']


def get_max_cords(f_cords, s_cords):
    if len(f_cords) != 0:
        max_cords = f_cords[0]
    elif len(s_cords) != 0:
        max_cords = s_cords[0]
    else:
        return None

    for cord in f_cords:
        if cord[0] < max_cords[0]:
            max_cords[0] = cord[0]
        if cord[1] < max_cords[1]:
            max_cords[1] = cord[1]
        if cord[2] > max_cords[2]:
            max_cords[2] = cord[2]
        if cord[3] > max_cords[3]:
            max_cords[3] = cord[3]

    for cord in s_cords:
        if cord[0] < max_cords[0]:
            max_cords[0] = cord[0]
        if cord[1] < max_cords[1]:
            max_cords[1] = cord[1]
        if cord[2] > max_cords[2]:
            max_cords[2] = cord[2]
        if cord[3] > max_cords[3]:
            max_cords[3] = cord[3]

    return max_cords


def get_cords(xml_file):
    cords = []
    try:
        tree = etree.parse(xml_file)
        tree_root = tree.getroot()

        for elm in tree_root.findall('./object/bndbox'):
            cords.append([int(elm.find('xmin').text), int(elm.find('ymin').text), int(elm.find('xmax').text),
                          int(elm.find('ymax').text)])

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)

    return cords


def get_moderator(xml_file):
    try:
        tree = etree.parse(xml_file)
        tree_root = tree.getroot()

        moderator = tree_root.find('./moderator')

        if moderator is not None:
            return moderator.text
        else:
            return None

    except FileNotFoundError:
        print('File ' + xml_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + xml_file)


def save_image(image, image_name, root):
    dir_name = os.path.join(os.path.dirname(root), 'result')
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    c_file = os.path.join(dir_name, os.path.basename(image_name))
    cv2.imwrite(c_file, image)
    # print('Image created.', image_name)


def process_xml(f_file, s_file, root):
    try:
        f_cords = get_cords(f_file)
        s_cords = get_cords(s_file)
        f_moderator = get_moderator(f_file)
        s_moderator = get_moderator(s_file)

        image_name = None
        for ext in img_ext:
            if os.path.exists(f_file.replace('.xml', ext)):
                image_name = f_file.replace('.xml', ext)
                break
            if os.path.exists(s_file.replace('.xml', ext)):
                image_name = s_file.replace('.xml', ext)
                break

        if image_name is None:
            print('Image does not exist for files', f_file, s_file)
            return

        image = cv2.imread(image_name)

        fu_cords = [x for x in f_cords if x not in f_cords or x not in s_cords]
        su_cords = [x for x in s_cords if x not in s_cords or x not in f_cords]

        ft_cords = []
        st_cords = []
        diff_flag = False

        try:
            for f_elm, s_elm in zip(fu_cords, su_cords):
                if f_elm[0] != s_elm[0] or f_elm[1] != s_elm[1] or f_elm[2] != s_elm[2] or f_elm[3] != s_elm[3]:
                    diff_flag = True
                    ft_cords.append(f_elm)
                    st_cords.append(s_elm)
                    cv2.rectangle(image,
                                  (f_elm[0], f_elm[1]),
                                  (f_elm[2], f_elm[3]),
                                  tuple((255, 0, 0)),
                                  thickness=1)
                    cv2.rectangle(image,
                                  (s_elm[0], s_elm[1]),
                                  (s_elm[2], s_elm[3]),
                                  tuple((0, 0, 255)),
                                  thickness=1)
        except Exception:
            print('Drawing box exception')

        if len(fu_cords) > len(su_cords):
            try:
                for i in range(len(su_cords), len(fu_cords)):
                    diff_flag = True
                    cv2.rectangle(image,
                                  (fu_cords[i][0], fu_cords[i][1]),
                                  (fu_cords[i][2], fu_cords[i][3]),
                                  tuple((255, 0, 0)),
                                  thickness=1)
                    ft_cords.append(fu_cords[i])
            except Exception:
                print('Index error 1')
        elif len(fu_cords) < len(su_cords):
            try:
                for i in range(len(fu_cords), len(su_cords)):
                    diff_flag = True
                    cv2.rectangle(image,
                                  (su_cords[i][0], su_cords[i][1]),
                                  (su_cords[i][2], su_cords[i][3]),
                                  tuple((0, 0, 255)),
                                  thickness=1)
                    st_cords.append(su_cords[i])
            except Exception:
                print('Index error 2')

        if diff_flag is False:
            return

        max_cords = get_max_cords(ft_cords, st_cords)

        if max_cords is None:
            return

        image = image[int(max_cords[1] / 1.05): int(max_cords[3] * 1.05),
                int(max_cords[0] / 1.05): int(max_cords[2] * 1.05)]

        height, width, channels = image.shape

        black = np.random.randint(0, 1, size=(40, width, channels), dtype=np.uint8)

        image = cv2.vconcat([black, image])

        cv2.putText(image, f_moderator, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                    1,
                    cv2.LINE_AA)
        cv2.putText(image, s_moderator, (width // 2, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255),
                    1,
                    cv2.LINE_AA)

        save_image(image, image_name, root)

    except Exception:
        print('Unknown exception occurred.', f_file, s_file)


def main(f_folder, s_folder):
    roots = []
    for root, dirs, files in os.walk(f_folder):
        roots.append(root)
        for file in tqdm.tqdm(files):
            if file.endswith('.xml'):
                f_file = os.path.join(root, file)
                if file not in os.listdir(s_folder):
                    print()
                    print(s_folder, 'does not exist file', file)
                    continue
                s_file = os.path.join(s_folder, file)
                process_xml(f_file, s_file, roots[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ff', '--first_folder', dest='f_folder', nargs='?', required=True)
    parser.add_argument('-sf', '--second_folder', dest='s_folder', nargs='?', required=True)
    main(parser.parse_args().f_folder, parser.parse_args().s_folder)
    input('Press ENTER...')
